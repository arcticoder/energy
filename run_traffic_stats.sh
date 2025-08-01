#!/bin/bash

# Set variables
SCRIPT_DIR="$HOME/Code/asciimath/energy"
PS_SCRIPT="$SCRIPT_DIR/run_traffic_stats.ps1"
LOG_FILE="$SCRIPT_DIR/wrapper_debug.log"

# Change to script directory
cd "$SCRIPT_DIR"

# Get timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Log start
echo "[$timestamp] Running PowerShell script..." >> "$LOG_FILE"
echo "Current directory: $(pwd)" >> "$LOG_FILE"
echo "PowerShell script path: $PS_SCRIPT" >> "$LOG_FILE"

# Run the PowerShell script with full paths and error output
/usr/bin/pwsh "$PS_SCRIPT" >> "$LOG_FILE" 2>&1

# Log completion with exit code
exit_code=$?
end_timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$end_timestamp] PowerShell script completed with exit code: $exit_code" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"