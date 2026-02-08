Linux LLM Agent
===============

Overview
--------

The **Linux LLM Agent** is an automated remediation agent designed for monitoring and maintaining Linux-based sandbox and GPU-accelerated nodes. Its goal is to reduce manual operational effort by automating common system checks, identifying failures, and applying corrective actions.
The agent integrates with an LLM (currently GPT-5 via TRAPI) to suggest Linux shell commands to resolve detected issues. It then executes these commands and verifies if the problem has been resolved. If automated LLM remediation fails, the agent falls back to predefined custom remediation steps.

Key Features
------------

1.  **GPU Health Checks**
    *   Detects whether NVIDIA GPUs are present and accessible.
        
    *   Uses a combination of `nvidia-smi` and custom GPU scripts (`/etc/azmonsandbox/custom_checks/check_gpu`) to detect hardware or driver issues.
        
    *   Automatically installs or reinstalls the latest compatible NVIDIA driver if GPU issues are detected.
        
    *   Avoids dangerous operations like reboots or shutdowns unless explicitly required.
        
2.  **Ubuntu Package Repository Checks**
    *   Runs `apt-get update` and parses output for common failure indicators (e.g., missing GPG keys, malformed sources, hash sum mismatches).
        
    *   If issues are detected, passes the error messages to the LLM for remediation suggestions.
        
    *   Falls back to custom commands or fixes if LLM output fails to resolve the issue.
        
3.  **Ansible Status Checks**
    *   Monitors the health of Ansible runs using custom scripts (`/etc/azmonsandbox/custom_checks/check_ansible_status.sh`).
        
    *   If failures are detected, captures recent logs and sends them to the LLM for remediation commands.
        
    *   Executes safe commands only (skipping reboots/shutdowns) and logs all actions.
        
4.  **TRAPI Integration**
    *   Communicates with a GPT-5-based model via TRAPI to suggest commands for detected issues.
        
    *   The agent ensures that commands are safe to run, modifies them if necessary, and executes them automatically.
        
5.  **Custom Remediation Fallbacks**
    *   If LLM-suggested commands fail, the agent uses built-in logic for GPU, APT, and Ansible issues to try alternative remediation steps.
        
    *   This includes installing the latest NVIDIA driver, running `apt --fix-broken install`, or applying predefined Ansible fixes.
        
6.  **Logging & Auditing**
    *   All actions, including executed commands and their output, are logged to `/var/log/linux_llm_agent/main.log`.
        
    *   Helps track remediation attempts, success/failure, and provides an audit trail for operations teams.


How It Works
------------

1.  **Detection Phase**
    *   The agent runs a series of checks:
        *   GPU health (via `nvidia-smi` and custom scripts)
            
        *   Ubuntu package repository (`apt-get update`)
            
        *   Ansible operational status
            
2.  **LLM Remediation Phase**
    *   If an issue is detected, the agent queries TRAPI with a structured prompt:
        
        > “You are an assistant that only outputs shell commands to fix Linux issues. No explanations. Do not offer reboot or shutdown commands. For NVIDIA driver issues, suggest installing the latest driver version.”
        
    *   TRAPI returns a suggested sequence of shell commands.
        
3.  **Execution Phase**
    *   The agent parses and executes the LLM-suggested commands safely:
        *   Skips dangerous commands (reboots, shutdowns)
            
        *   Prepends `DEBIAN_FRONTEND=noninteractive` to `apt` commands
            
        *   Executes commands via Python’s `subprocess` module (or the Go binary equivalent)
            
    *   Logs all command outputs.
        
4.  **Verification Phase**
    *   After execution, the agent reruns the initial checks to verify whether the problem is resolved.
        
    *   If the issue persists, the agent falls back to **custom remediation logic**:
        *   Installs the latest NVIDIA driver
            
        *   Fixes broken APT dependencies
            
        *   Reinstalls or repairs Ansible
            
5.  **Repeat / Continuous Monitoring**
    *   The agent can be run periodically or triggered by automated alerts to maintain system health continuously.

Configuration
-------------

*   `DRY_RUN` (bool) – Set to `True` to print commands without executing them.
    
*   `LOG_DIR` – Directory for logs, default `/var/log/linux_llm_agent`.
    
*   `gpu_script` – Custom GPU check script path: `/etc/azmonsandbox/custom_checks/check_gpu`.
    
*   TRAPI endpoint is configured in `trapi_client.py`.
    

* * *

Notes
-----

*   The agent **avoids dangerous operations** such as reboots and shutdowns.
    
*   Works currently on Ubuntu Linux versions, NVIDIA GPU nodes, and a properly configured TRAPI endpoint.
    
*   Still under active development; improvements may include:
    *   Additional check types
        
    *   Smarter fallback logic
        
    *   Integration with monitoring dashboards
        

* * *

Logging
-------

*   Main log file: `/var/log/linux_llm_agent/main.log`
    
*   Logs include:
    *   Detected issues
        
    *   Commands executed
        
    *   Command outputs
        
    *   Success/failure status

