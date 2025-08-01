# Get all subdirectories in current working directory
$subdirs = Get-ChildItem -Directory -Path "$home\Code\asciimath"

Write-Host "Repositories with commits in the past 12 hours:" -ForegroundColor Green
Write-Host ""

foreach ($dir in $subdirs) {
    # Check if directory contains a .git folder
    $gitDir = Join-Path $dir.FullName ".git"
    
    if (Test-Path $gitDir) {
        # Change to the repository directory
        Push-Location $dir.FullName
        
        try {
            # Use git log to check if there are any commits in the past 8 hours
            $hasRecentCommits = git log --since="12 hours ago" --oneline --quiet 2>$null
            
            if ($hasRecentCommits) {
                Write-Host $dir.Name -ForegroundColor Yellow
            }
        }
        catch {
            # Silently skip repositories with git errors
        }
        finally {
            # Return to original directory
            Pop-Location
        }
    }
}