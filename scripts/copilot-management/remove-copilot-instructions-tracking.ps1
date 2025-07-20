# PowerShell script to remove git tracking from copilot-instructions.md symlinks

$asciimathPath = "C:\Users\$env:USERNAME\Code\asciimath"

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
        } else {
            Write-Host "  Not tracked by git" -ForegroundColor Yellow
        }
        
        # Add to .gitignore to prevent future tracking
        $gitignorePath = ".gitignore"
        $ignoreEntry = ".github/instructions/copilot-instructions.md"
        
        if (Test-Path $gitignorePath) {
            $gitignoreContent = Get-Content $gitignorePath -Raw
            if ($gitignoreContent -notmatch [regex]::Escape($ignoreEntry)) {
                Add-Content -Path $gitignorePath -Value "`n$ignoreEntry"
                Write-Host "  Added to .gitignore" -ForegroundColor Green
            } else {
                Write-Host "  Already in .gitignore" -ForegroundColor Gray
            }
        } else {
            Set-Content -Path $gitignorePath -Value $ignoreEntry
            Write-Host "  Created .gitignore with entry" -ForegroundColor Green
        }
        
        # Commit the changes
        $hasChanges = git status --porcelain 2>$null
        if ($hasChanges) {
            git add .gitignore 2>$null
            git commit -m "Add copilot-instructions.md to .gitignore and remove from tracking" 2>$null
            git push 2>$null
            Write-Host "  Changes committed and pushed" -ForegroundColor Green
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
