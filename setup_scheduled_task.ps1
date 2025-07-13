# Setup Scheduled Task for ASCIIMath File Catalog System
# This script creates a Windows 11 scheduled task to run the file catalog system daily at 11:49 PM

param(
    [switch]$Remove,
    [switch]$Force
)

$TaskName = "ASCIIMath-File-Catalog"
$TaskDescription = "Daily scan of ASCIIMath project files to maintain file catalog"
$ScriptPath = Join-Path $PSScriptRoot "catalog_files.py"
$LogPath = Join-Path $PSScriptRoot "catalog_task.log"

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Remove existing task if requested
if ($Remove) {
    Write-Host "Removing scheduled task '$TaskName'..." -ForegroundColor Yellow
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-Host "Task '$TaskName' removed successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "Task '$TaskName' not found or could not be removed: $($_.Exception.Message)" -ForegroundColor Red
    }
    exit
}

# Check administrator privileges
if (-not (Test-Administrator)) {
    Write-Host "ERROR: This script must be run as Administrator to create scheduled tasks." -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Verify Python script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Python script not found at: $ScriptPath" -ForegroundColor Red
    exit 1
}

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask -and -not $Force) {
    Write-Host "Task '$TaskName' already exists!" -ForegroundColor Yellow
    Write-Host "Use -Force to recreate or -Remove to delete the existing task." -ForegroundColor Cyan
    exit 1
}

if ($ExistingTask) {
    Write-Host "Removing existing task '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Write-Host "Creating scheduled task '$TaskName'..." -ForegroundColor Cyan

try {
    # Create task action - run Python script
    $Action = New-ScheduledTaskAction -Execute "python" -Argument "`"$ScriptPath`"" -WorkingDirectory (Split-Path $ScriptPath)
    
    # Create task trigger - daily at 11:49 PM
    $Trigger = New-ScheduledTaskTrigger -Daily -At "11:49 PM"
    
    # Create task settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
    
    # Create task principal - run as current user
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
    
    # Register the scheduled task
    Register-ScheduledTask -TaskName $TaskName -Description $TaskDescription -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal
    
    Write-Host "✅ Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName" -ForegroundColor White
    Write-Host "  Schedule: Daily at 11:49 PM" -ForegroundColor White
    Write-Host "  Script: $ScriptPath" -ForegroundColor White
    Write-Host "  User: $env:USERNAME" -ForegroundColor White
    Write-Host ""
    Write-Host "Management Commands:" -ForegroundColor Cyan
    Write-Host "  View task: Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
    Write-Host "  Run now: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
    Write-Host "  Remove task: .\setup_scheduled_task.ps1 -Remove" -ForegroundColor Gray
    Write-Host "  View logs: Get-Content '$LogPath'" -ForegroundColor Gray
    
    # Test run the task
    Write-Host ""
    $TestRun = Read-Host "Would you like to test run the task now? (y/N)"
    if ($TestRun -eq 'y' -or $TestRun -eq 'Y') {
        Write-Host "Running task now..." -ForegroundColor Yellow
        Start-ScheduledTask -TaskName $TaskName
        Start-Sleep -Seconds 3
        
        # Check task status
        $TaskInfo = Get-ScheduledTask -TaskName $TaskName
        Write-Host "Task Status: $($TaskInfo.State)" -ForegroundColor $(if($TaskInfo.State -eq 'Ready') {'Green'} else {'Yellow'})
    }
}
catch {
    Write-Host "❌ Error creating scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Setup complete! The file catalog will run automatically every night at 11:49 PM." -ForegroundColor Green
