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
    # Run the Python script and capture output and exit code
    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = $venvPython
    $processInfo.Arguments = "tools/check_traffic_stats.py"
    $processInfo.RedirectStandardOutput = $true
    $processInfo.RedirectStandardError = $true
    $processInfo.UseShellExecute = $false
    $processInfo.CreateNoWindow = $true
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $processInfo
    $process.Start() | Out-Null
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    $exitCode = $process.ExitCode

    # Log the output
    "[$timestamp] Script output:" | Add-Content $LogPath
    $stdout | Add-Content $LogPath
    if ($stderr) {
        "[$timestamp] Script stderr:" | Add-Content $LogPath
        $stderr | Add-Content $LogPath
    }

    if ($exitCode -eq 0) {
        # Log completion
        $endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "[$endTimestamp] GitHub traffic stats collection completed successfully." | Add-Content $LogPath
    } else {
        $errorTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "[$errorTimestamp] ERROR: Python script exited with code $exitCode" | Add-Content $LogPath
    }
} catch {
    # Log any errors
    $errorTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$errorTimestamp] EXCEPTION: $($_.Exception.Message)" | Add-Content $LogPath
    if ($_.Exception.StackTrace) {
        "StackTrace: $($_.Exception.StackTrace)" | Add-Content $LogPath
    }
}

# Add separator
"----------------------------------------" | Add-Content $LogPath