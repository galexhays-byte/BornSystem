import shlex
import subprocess
from pathlib import Path


class ExecutionSandbox:
    FORBIDDEN_PATTERNS = [
        "rm -rf",
        "shutdown",
        "reboot",
        "poweroff",
        "format ",
        "dd if=",
        "mkfs",
        ":(){|:};:",
        "sudo",
        "curl http://",
        "curl https://",
        "wget http://",
        "wget https://",
    ]

    ALLOWED_COMMANDS = {
        "echo",
        "ls",
        "dir",
        "find",
        "python",
        "python3",
        "git",
        "nmap",
        "masscan",
        "sqlite3",
        "curl",
        "wget",
        "grep",
        "cat",
        "ping",
        "head",
        "tail",
        "awk",
        "sed",
        "uname",
        "tr",
        "sort",
        "uniq",
        "docker",
        "docker-compose",
    }

    def __init__(self, root_dir: str | Path | None = None):
        self.root_dir = Path(root_dir or Path.cwd()).resolve()

    def validate_command(self, command: str) -> None:
        normalized = command.lower()
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in normalized:
                raise ValueError(f"Command contains forbidden pattern: {pattern}")

        if "&&" in command or "||" in command or ";" in command or "|" in command:
            raise ValueError("Command chaining is not allowed in sandboxed execution")

        tokens = shlex.split(command)
        if not tokens:
            raise ValueError("No command provided")

        if tokens[0] not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command '{tokens[0]}' is not allowed in sandbox")

        for token in tokens:
            if token.startswith("/"):
                try:
                    resolved = Path(token).resolve()
                    if self.root_dir not in resolved.parents and resolved != self.root_dir:
                        raise ValueError("Absolute paths outside the sandbox root are forbidden")
                except Exception:
                    raise ValueError("Invalid token in command")

    def execute_command(self, command: str, timeout: int = 10) -> dict:
        self.validate_command(command)
        tokens = shlex.split(command)

        process = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(self.root_dir),
        )

        return {
            "command": command,
            "return_code": process.returncode,
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip(),
        }
