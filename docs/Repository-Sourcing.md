# Repository Sourcing Guide

This document captures the core external repositories, firmware sources, and tooling inventory needed for BornSystem and FieldTasker.

## Purpose

- Track download sources for required field tools and firmware.
- Separate required core assets from optional or legacy items.
- Provide a clean reference for repo sourcing, cloud storage layout, and staging.

## Required Core Sources

### Cloud / Storage Repositories
- `rtl_433` from GitHub
- `ESP32 Marauder` firmware
- `Proxmark3 Iceman` fork
- `Mayhem` firmware for HackRF / PortaPack H2

### Linux ARM64 Tools for Field Nodes
- `nmap` and custom NSE scripts
- `rtl_433` for RF discovery
- `URH` (Universal Radio Hacker) for signal analysis
- `GQRX` (optional GUI SDR client)
- `SDR#` (Windows GUI, optional legacy)

### Firmware Repositories
- `firmware/rfid_tools/proxmark3/`
- `firmware/rfid_tools/chameleon_ultra/`
- `firmware/rfid_tools/icopyx/`
- `firmware/rf_tools/portapack_h2/`
- `firmware/rf_tools/pandwarf/`
- `firmware/mcu_tools/lilygo_tembed/`
- `firmware/mcu_tools/esp32_marauder/`

## Optional / Advanced Sources

- SDR software packages for advanced RF analysis such as `GQRX` and `SDR#`
- Extra firmware or payload sources for low-frequency devices and custom MCUs
- Additional node tooling for Bluetooth and NFC fingerprinting

## Storage Layout Recommendations

The cloud repository should support:

- `binaries/linux-arm64/network_tools/`
- `binaries/linux-arm64/rf_tools/`
- `firmware/rfid_tools/`
- `firmware/rf_tools/`
- `firmware/mcu_tools/`

## Repository Index References

These GitHub catalogs are useful sources for finding additional tools and AI agents to include in the BornSystem ecosystem:

- `https://github.com/BlackArch/blackarch` — BlackArch Linux archive for offensive security and penetration testing tool packages.
- `https://github.com/EvanThomasLuke/Awesome-AI-Hacking-Agents/blob/main/README.md` — curated list of AI hacking and automation agent frameworks.

Use these references to identify candidate tools and agent integrations for `storage/binaries/`, `storage/scripts/`, and the automation engine.

## AI Automation & Chatbot Sources

### AI Automation Architectures
- Kali MCP Server approach
  - Use an MCP bridge to connect LLMs and Kali tools safely.
  - Preferred path for autonomous orchestration and multi-tool workflows.
- ShellGPT / sgpt
  - Use CLI-based AI tool integration for on-demand code generation and script writing.
  - Good for generating automation without full autonomous execution.
- tgpt
  - API-free CLI automation for rapid local testing.
  - Useful when API key management is undesirable.

### Recommended Repositories and Install Sources
- `kalilinux/kali-rolling` Docker image
- `https://raw.githubusercontent.com/aandrew-me/tgpt/main/install` for tgpt installation
- `FastMCP` / `FastAPI`-based MCP server templates

### Safe Execution Patterns
- Containerize all AI script execution with Docker
- Do not execute LLM-generated commands directly on the host machine
- Limit destructive operations with hardcoded guardrails
- Route AI tool execution through a service layer (FastAPI or custom sandbox)

## On-Demand Automation Chatbot Sources

This section captures the chatbot architecture and tool integration strategy from your notes.

### Core components
- LLM router / orchestration layer
  - LangChain / LangGraph / Autogen
- Code interpreter / tool bridge
  - Python `subprocess` wrappers for safe command execution
  - Database inspectors such as SQLAlchemy for schema discovery
- Device discovery and inventory
  - `psutil` for system stats
  - `subprocess` for OS CLI tools and network utilities
  - `mDNS` / `ZeroConf` for local device detection

### Example tool bindings to source
- `execute_bash_command` wrapper for isolated command execution
- `query_local_sqlite` for local database inspection
- FastAPI service endpoint for chatbot tool invocation

### Deployment notes
- Wrap the chatbot backend in Docker Compose for isolation
- Use a frontend UI via Streamlit, Chainlit, or a simple SPA
- Protect API keys and database credentials with least-privilege access
- Block destructive commands like `rm -rf /`

## Camera & IP Camera Scanning Sources

### Camera discovery and RTSP tools
- `Angry IP Scanner`
- `Advanced IP Scanner`
- `ONVIF Device Manager`
- `Fing`
- `Nmap`
- `Masscan`
- `Cameradar`
- `Wireshark`
- `scapy`

### Recommended source material
- ONVIF Device Manager documentation and device URL pattern references
- `iSpy Connect Camera Database` for RTSP templates
- Camera brand RTSP patterns:
  - Amcrest: `rtsp://<user>:<pass>@<IP>:554/cam/realmonitor?channel=1&subtype=0`
  - Axis: `rtsp://<user>:<pass>@<IP>/axis-media/media.amp`
  - Dahua: `rtsp://<user>:<pass>@<IP>:554/cam/realmonitor?channel=1&subtype=0`
  - D-Link: `rtsp://<IP>:554/live1.sdp`
  - Hikvision: `rtsp://<user>:<pass>@<IP>:554/Streaming/Channels/101`
  - Reolink: `rtsp://<user>:<pass>@<IP>:554/h264Preview_01_main`

### Example automation script sources
- Python `scapy` ARP scanner for subnet device discovery
- shell or Python scripts to automate port scans and RTSP validation

## Cybersecurity Tool Sources

### BlackArch / Offensive Security Catalogs
- `https://github.com/BlackArch/blackarch` — use as the primary index for offensive security packages and tool categories.
- `https://github.com/EvanThomasLuke/Awesome-AI-Hacking-Agents/blob/main/README.md` — curated list of AI hacking agents and automation frameworks.

### High-priority tool references
- `Nmap` — https://github.com/nmap/nmap
- `Masscan` — https://github.com/robertdavidgraham/masscan
- `Metasploit Framework` — https://github.com/rapid7/metasploit-framework
- `Hydra` — https://github.com/vanhauser-thc/thc-hydra
- `sqlmap` — https://github.com/sqlmapproject/sqlmap
- `Burp Suite Community` — https://portswigger.net/burp (commercial/official)
- `Cameradar` — https://github.com/Ullaakut/cameradar
- `Wireshark` — https://github.com/wireshark/wireshark
- `Suricata` — https://github.com/OISF/suricata
- `Snort` — https://www.snort.org/
- `Zeek` — https://github.com/zeek/zeek
- `Hashcat` — https://github.com/hashcat/hashcat
- `John the Ripper` — https://github.com/openwall/john
- `Bettercap` — https://github.com/bettercap/bettercap
- `Gobuster` — https://github.com/OJ/gobuster
- `Amass` — https://github.com/OWASP/Amass
- `Dirbuster` / `Dirb` — https://github.com/v0re/dirb

### RF / IoT / firmware tool sources
- `rtl_433` — https://github.com/merbanan/rtl_433
- `ESP32 Marauder` firmware — https://github.com/justcallmekoko/ESP32Marauder
- `Proxmark3 Iceman` — https://github.com/Proxmark/proxmark3 or forked Iceman variations
- `Mayhem` firmware for HackRF / PortaPack — https://github.com/erikarn/Mayhem
- `GQRX` — https://github.com/csete/gqrx
- `URH` — https://github.com/jopohl/urh

### AI automation / agent sources
- `tgpt` — https://github.com/aandrew-me/tgpt
- `ShellGPT` — https://github.com/sagelga/gpt-shell
- `FastMCP` / `MCP server` templates — search GitHub for `FastMCP` or `MCP server` examples
- `LangChain` / `Autogen` / `Autogpt` — use for orchestration of agentic automation

### GitHub search discovered repositories
- `0x4m4/hexstrike-ai` — HexStrike AI MCP Agents, an advanced MCP server for autonomous pentesting tool orchestration.
- `digitranslab/allama` — AI security automation platform with visual workflows and integrations for threat detection and response.
- `nathangtg/agent-hub` — AI orchestration hub built on MCP for toolchain automation and security workflows.
- `Threat-Vector-Security/guardian-agent` — security-first AI agent orchestration with sandboxing and tool approvals.
- `Muhammad-Qasim-Munir/skillguard` — prompt injection and agent security scanner for safe automation.

### Recommended packaging strategy
- Use BlackArch package names when possible for Linux/OFFSEC tooling
- For tools without official packages, stage binaries or install manifests in `storage/binaries/`
- Keep the source URL and package name documented in a `tool-manifest.md` or `storage/manifest.txt`

## Tooling Inventory Categories

### Core
- `nmap`
- `tshark`
- `masscan`
- `rtl_433`
- `rclone`
- `bluetoothctl`
- `tcpdump`
- `scapy`

### Optional / Advanced
- `URH`
- `GQRX`
- `SDR#`
- `Cameradar`
- `ONVIF Device Manager`

### Legacy / Cross-Platform Notes
- Avoid Termux as a final design target.
- Prefer standalone field controller applications.
- Use Docker or isolated containers for ephemeral processing when possible.
- Keep field node execution abstracted behind the same API regardless of local or remote device.

## Next Steps

1. Collect exact GitHub URLs for each repository and firmware source.
2. Add these URLs to the `storage/` manifest and cloud object storage documentation.
3. Create a `Firmware-Repository.md` and `Cloud/Storage-Structure.md` if needed.
4. Add a `docs/Repository-Sourcing.md` summary to the project docs index.
