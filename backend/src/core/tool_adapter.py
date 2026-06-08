import json
import sqlite3
from pathlib import Path
from typing import Any, Callable, Dict

from .sandbox import ExecutionSandbox


class ToolAdapter:
    def __init__(self, sandbox: ExecutionSandbox | None = None):
        self.sandbox = sandbox or ExecutionSandbox()
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.register(
            "run_shell",
            self.run_shell,
            "Execute a safe shell command through the sandbox",
            presets={
                "echo_sample": {"command": "echo 'Hello BornSystem'"},
            },
        )
        self.register(
            "query_sqlite",
            self.query_sqlite,
            "Run a read-only SQLite query",
            presets={
                "sample_firmware_query": {
                    "db_path": "database/fieldtasker.db",
                    "query": "SELECT * FROM firmware_fingerprints LIMIT 10",
                },
            },
        )
        self.register(
            "list_files",
            self.list_files,
            "List files in a directory",
            presets={"home_directory": {"path": "."}},
        )
        self.register(
            "scan_network",
            self.scan_network,
            "Scan network using nmap for live hosts and services",
            presets={"local_network": {"target": "192.168.1.0/24"}},
        )
        self.register(
            "discover_cameras",
            self.discover_cameras,
            "Discover IP cameras on network via ONVIF/RTSP",
            presets={"local_cameras": {"target": "192.168.1.0/24"}},
        )
        self.register(
            "scan_rf_signals",
            self.scan_rf_signals,
            "Scan for RF signals using rtl_433",
            presets={"433mhz_scan": {"frequency": "433", "duration": 15}},
        )
        self.register(
            "analyze_firmware",
            self.analyze_firmware,
            "Analyze firmware hash against threat database",
            presets={"suspicious_hash": {"firmware_hash": "abcdef1234567890"}},
        )
        self.register(
            "generate_followup_script",
            self.generate_followup_script,
            "Generate a follow-up automation script based on scan results and detected hardware metadata",
            presets={},
        )

    def register(self, name: str, func: Callable[..., dict], description: str, presets: dict | None = None) -> None:
        self.tools[name] = {
            "func": func,
            "description": description,
            "presets": presets or {},
        }

    def get_tool(self, name: str) -> dict:
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' is not registered")
        return self.tools[name]

    def execute(self, name: str, args: dict | None = None) -> dict:
        if args is None:
            args = {}
        tool = self.get_tool(name)
        try:
            return tool["func"](**args)
        except Exception as exc:
            return {
                "tool": name,
                "status": "failed",
                "error": str(exc),
            }

    def run_shell(self, command: str, timeout: int = 10) -> dict:
        return self.sandbox.execute_command(command, timeout=timeout)

    def query_sqlite(self, db_path: str, query: str) -> dict:
        resolved = Path(db_path).resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"SQLite database not found: {db_path}")
        connection = sqlite3.connect(str(resolved))
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        connection.close()
        return {
            "tool": "query_sqlite",
            "db_path": str(resolved),
            "query": query,
            "columns": columns,
            "rows": rows,
        }

    def list_files(self, path: str = ".") -> dict:
        folder = Path(path).resolve()
        if not folder.exists() or not folder.is_dir():
            raise FileNotFoundError(f"Directory not found: {path}")
        items = [item.name for item in folder.iterdir()]
        return {
            "tool": "list_files",
            "path": str(folder),
            "items": items,
        }

    def scan_network(self, target: str, timeout: int = 30) -> dict:
        try:
            result = self.sandbox.execute_command(f"nmap -sn {target}", timeout=timeout)
            return {
                "tool": "scan_network",
                "target": target,
                "status": "complete" if result["return_code"] == 0 else "failed",
                "output": result["stdout"],
            }
        except Exception as exc:
            return {
                "tool": "scan_network",
                "target": target,
                "status": "failed",
                "error": str(exc),
            }

    def discover_cameras(self, target: str, timeout: int = 30) -> dict:
        try:
            result = self.sandbox.execute_command(f"nmap -p 554 -sV {target}", timeout=timeout)
            return {
                "tool": "discover_cameras",
                "target": target,
                "description": "Scanned RTSP port 554 for camera services",
                "status": "complete" if result["return_code"] == 0 else "partial",
                "output": result["stdout"],
            }
        except Exception as exc:
            return {
                "tool": "discover_cameras",
                "target": target,
                "status": "failed",
                "error": str(exc),
            }

    def scan_rf_signals(self, frequency: str = "433", duration: int = 10) -> dict:
        try:
            result = self.sandbox.execute_command(f"echo 'RF scan simulated for {frequency}MHz over {duration}s'", timeout=duration + 5)
            return {
                "tool": "scan_rf_signals",
                "frequency": frequency,
                "duration": duration,
                "status": "complete",
                "output": result["stdout"],
                "note": "requires rtl_433 binary and SDR dongle on field nodes",
            }
        except Exception as exc:
            return {
                "tool": "scan_rf_signals",
                "frequency": frequency,
                "status": "failed",
                "error": str(exc),
            }

    def analyze_firmware(self, firmware_hash: str, db_path: str = "database/fieldtasker.db") -> dict:
        try:
            resolved = Path(db_path).resolve()
            if not resolved.exists():
                return {
                    "tool": "analyze_firmware",
                    "firmware_hash": firmware_hash,
                    "status": "database_not_found",
                    "message": f"Threat database not found at {db_path}",
                }
            import sqlite3
            conn = sqlite3.connect(str(resolved))
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM firmware_fingerprints WHERE firmware_hash = ? LIMIT 1", (firmware_hash,))
            rows = cursor.fetchall()
            conn.close()
            found = len(rows) > 0
            return {
                "tool": "analyze_firmware",
                "firmware_hash": firmware_hash,
                "found_in_database": found,
                "status": "malicious" if found else "unknown",
                "rows": rows,
            }
        except Exception as exc:
            return {
                "tool": "analyze_firmware",
                "firmware_hash": firmware_hash,
                "status": "failed",
                "error": str(exc),
            }

    def generate_followup_script(self, scan_result: dict, device_info: str | None = None) -> dict:
        output = str(scan_result.get("output", ""))
        tool_name = scan_result.get("tool", "")
        target = scan_result.get("target") or scan_result.get("frequency") or scan_result.get("firmware_hash")

        script_lines = ["# Generated follow-up automation commands"]
        recommendations = []

        def append_command(cmd: str):
            if cmd not in script_lines:
                script_lines.append(cmd)

        if tool_name == "discover_cameras" or "camera" in output.lower() or "rtsp" in output.lower():
            recommendations.append("Detected camera-related services. Perform deeper RTSP and web interface discovery.")
            if target:
                append_command(f"nmap -p 80,443,554,8000,8080 -sV {target}")
                append_command(f"nmap --script=http-title -p 80,443 {target}")
                append_command(f"echo 'If RTSP devices are found, validate default credentials and capture stream metadata.'")
            else:
                append_command("echo 'Camera or RTSP services detected. Provide the target network or host to continue.'")

        if tool_name == "scan_network" or "nmap scan report" in output.lower():
            host_ips = []
            for line in output.splitlines():
                if line.lower().startswith("nmap scan report for "):
                    host_ips.append(line.split()[-1])
            if target and not host_ips:
                host_ips = [target]
            if host_ips:
                recommendations.append("Detected network hosts. Fingerprint exposed services and firmware.")
                for ip in host_ips[:5]:
                    append_command(f"nmap -sV -p 22,80,443,554 {ip}")
                    append_command(f"nmap --script=banner,vuln -p 22,80,443 {ip}")
            else:
                append_command("echo 'No hosts parsed from scan output. Provide a network target for further automation.'")

        if tool_name == "scan_rf_signals" or "rf" in output.lower() or device_info:
            recommendations.append("Detected RF activity. Capture and analyze signals with rtl_433.")
            frequency = scan_result.get("frequency", "433")
            append_command(f"rtl_433 -F json -f {frequency}M")
            append_command("echo 'Save captured RF frames and process them for device fingerprinting.'")

        if tool_name == "analyze_firmware" or scan_result.get("firmware_hash"):
            if scan_result.get("found_in_database"):
                recommendations.append("Firmware hash matched a known threat signature. Generate containment and remediation actions.")
                append_command("echo 'Isolate the device and collect a full firmware sample for deeper analysis.'")
                append_command("echo 'Notify security team and apply firmware blacklist rules.'")
            else:
                recommendations.append("Firmware hash not found in database. Consider further analysis or device profiling.")
                append_command("echo 'Collect firmware metadata and vendor information for future threat intelligence.'")

        chipset_matches = [keyword for keyword in ["intel", "mediatek", "broadcom", "realtek", "arm", "mips"] if keyword in output.lower()]
        if chipset_matches:
            recommendations.append(f"Detected chipset keyword(s): {', '.join(chipset_matches)}. Generate targeted firmware and exploit search scripts.")
            append_command("echo 'Use chipset-specific tooling and firmware analysis workflows for detected devices.'")

        if not recommendations:
            recommendations.append("No specific device metadata could be extracted from the scan output. Use a supported scan result format or add more data.")
            append_command("echo 'Provide a scan result with discovered hosts, services, or chipset details for script generation.'")

        script = "\n".join(script_lines)
        workflow = [{"tool": "run_shell", "args": {"command": cmd}} for cmd in script_lines[1:]]
        return {
            "tool": "generate_followup_script",
            "target": target,
            "recommendations": recommendations,
            "script": script,
            "workflow": workflow,
            "source": scan_result,
        }
