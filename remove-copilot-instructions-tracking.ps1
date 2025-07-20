# PowerShell script to remove git tracking from copilot-instructions.md symlinks

$asciimathPath = "C:\Users\echo_\Code\asciimath"

# Get all subdirectories in the asciimath folder
$repos = Get-ChildItem -Path $asciimathPath -Directory

Write-Host "Removing git tracking from copilot-instructions.md in $($repos.Count) repositories..."

foreach ($repo in $repos) {
    $repoPath = $repo.FullName
    $symlinkPath = ".github\instructions\copilot-instructions.md"
    
    Write-Host "Processing: $($repo.Name)"
    
    Push-Location $repoPath
    try {
        # Check if the symlink exists and is tracked by git
        $isTracked = git ls-files $symlinkPath 2>$null
        
        if ($isTracked) {
            # Remove from git tracking but keep the file
            git rm --cached $symlinkPath 2>$null
            Write-Host "  Removed from git tracking" -ForegroundColor Green
            
            # Commit the change
            git add .gitignore 2>$null  # In case .gitignore is updated
            git commit -m "Remove git tracking from copilot-instructions.md symlink" 2>$null
            git push 2>$null
            Write-Host "  Changes committed and pushed" -ForegroundColor Green
        } else {
            Write-Host "  Not tracked by git" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  Error or not a git repository: $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

Write-Host "Git tracking removal completed!"
