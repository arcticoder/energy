# PowerShell script to commit and push traffic analytics changes
Set-Location "C:\Users\echo_\Code\asciimath\energy"

Write-Host "Current directory: $(Get-Location)"
Write-Host "Git status:"
git status

Write-Host "Adding files to staging..."
git add tools/traffic_stats_history.ndjson
git add tools/check_traffic_stats.py  
git add tools/traffic_chart_template.html
git add tools/traffic_stats_chart.html
git add tools/traffic_slope_history.json

if ($LASTEXITCODE -eq 0) {
    Write-Host "Files added successfully"
} else {
    Write-Host "Warning: Some files may not exist or have no changes"
}

Write-Host "Checking if there are changes to commit..."
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Changes detected, committing..."
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Enhanced traffic analytics system - $timestamp

- Extended historical data from 15 to 18+ days using preserved traffic_stats_history.ndjson
- Implemented daily commit tracking instead of 30-day totals for granular analysis  
- Added Hide All/Show All buttons to chart interface for improved user experience
- Updated chart labels from 'Recent Commits (30d)' to 'Daily Commits' for accuracy
- Enhanced template with JavaScript functions for comprehensive dataset control

System now provides richer insights with extended historical data and daily commit granularity."

    git commit -m $commitMessage
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Changes committed successfully"
        Write-Host "Pushing to remote repository..."
        git push
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Changes pushed successfully!"
        } else {
            Write-Host "Push failed - may need manual intervention"
        }
    } else {
        Write-Host "Commit failed"
    }
} else {
    Write-Host "No changes to commit"
}

Write-Host "Script completed"
