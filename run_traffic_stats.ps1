# GitHub Traffic Stats Scheduled Task Script
# Runs the Python traffic analytics script and logs output

param(
    [string]$LogPath = "$HOME/Code/asciimath/energy/traffic_stats_log.txt"
)

# Set working directory (use forward slashes for Linux)
Set-Location "$HOME/Code/asciimath/energy"

# Use venv Python
$venvPython = "$HOME/Code/asciimath/energy/venv/bin/python"

# Get timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Log start
"[$timestamp] Starting GitHub traffic stats collection..." | Add-Content $LogPath

try {
    # Run the Python script and capture output
    $output = & $venvPython tools/check_traffic_stats.py 2>&1
    
    # Log the output
    "[$timestamp] Script output:" | Add-Content $LogPath
    $output | Add-Content $LogPath
    
    # Log completion
    $endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$endTimestamp] GitHub traffic stats collection completed successfully." | Add-Content $LogPath
    
} catch {
    # Log any errors
    $errorTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$errorTimestamp] ERROR: $($_.Exception.Message)" | Add-Content $LogPath
}

# Add separator
"----------------------------------------" | Add-Content $LogPath