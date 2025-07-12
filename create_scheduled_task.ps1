# Create Windows Scheduled Task for GitHub Traffic Stats
# Run this script as Administrator (elevated PowerShell)

$TaskName = "GitHub-Traffic-Stats-Daily"
$TaskDescription = "Daily GitHub traffic statistics collection and chart generation"
$ScriptPath = "C:\Users\echo_\Code\asciimath\energy\run_traffic_stats.ps1"
$WorkingDirectory = "C:\Users\echo_\Code\asciimath\energy"

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

try {
    # Remove existing task if it exists
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Write-Host "🗑️  Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create the action (what to run)
    $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`"" -WorkingDirectory $WorkingDirectory

    # Create the trigger (when to run - daily at 11:56 PM)
    $Trigger = New-ScheduledTaskTrigger -Daily -At "23:56"

    # Create task settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    # Create the principal (run as current user)
    $Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

    # Register the scheduled task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description $TaskDescription

    Write-Host "✅ Scheduled task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host "📅 Task will run daily at 11:56 PM" -ForegroundColor Cyan
    Write-Host "📁 Working directory: $WorkingDirectory" -ForegroundColor Cyan
    Write-Host "📄 Script: $ScriptPath" -ForegroundColor Cyan
    Write-Host "📝 Logs will be saved to: $WorkingDirectory\traffic_stats_log.txt" -ForegroundColor Cyan
    
    # Show task details
    Write-Host "`n📋 Task Details:" -ForegroundColor Magenta
    Get-ScheduledTask -TaskName $TaskName | Format-Table -AutoSize
    
    # Test the task
    Write-Host "🧪 Would you like to test the task now? (Y/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "🚀 Starting task..." -ForegroundColor Green
        Start-ScheduledTask -TaskName $TaskName
        Write-Host "✅ Task started! Check the log file for output." -ForegroundColor Green
    }

} catch {
    Write-Host "❌ Error creating scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Setup complete! Your GitHub traffic stats will be automatically updated every night at 11:56 PM." -ForegroundColor Green
Write-Host "📊 View results at: file:///C:/Users/echo_/Code/asciimath/energy/traffic_stats_chart.html" -ForegroundColor Cyan
