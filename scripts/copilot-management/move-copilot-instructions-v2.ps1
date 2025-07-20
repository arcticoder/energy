# Move copilot-instructions.md files from .github/instructions/ to .github/ across all repositories
# Handle symlinks properly and create new symlink in energy repository

$baseDir = "C:\Users\$env:USERNAME\Code\asciimath"
$targetFile = "G:\My Drive\code\ai\tech-roadmap\.vscode-instructions.md"

# Get all repository directories
$repos = Get-ChildItem -Path $baseDir -Directory | Where-Object { $_.Name -ne ".github" }

Write-Host "Moving copilot-instructions.md files in $($repos.Count) repositories..."

foreach ($repo in $repos) {
    $repoPath = $repo.FullName
    $repoName = $repo.Name
    
    # Check if this is a git repository
    if (-not (Test-Path (Join-Path $repoPath ".git"))) {
        Write-Host "[${repoName}] - Not a git repository" -ForegroundColor Yellow
        continue
    }
    
    $instructionsDir = Join-Path $repoPath ".github\instructions"
    $instructionsFile = Join-Path $instructionsDir "copilot-instructions.md"
    $githubDir = Join-Path $repoPath ".github"
    $newLocation = Join-Path $githubDir "copilot-instructions.md"
    
    # Check if the source file exists
    if (Test-Path $instructionsFile) {
        Write-Host "[${repoName}] - Processing copilot-instructions.md" -ForegroundColor Green
        
        # Change to repository directory for git operations
        Push-Location $repoPath
        
        try {
            # Check if it's a symlink
            $item = Get-Item $instructionsFile
            if ($item.LinkType -eq "SymbolicLink") {
                Write-Host "[${repoName}] - Removing symlink and creating new one" -ForegroundColor Cyan
                
                # Remove the symlink from git tracking
                git rm ".github\instructions\copilot-instructions.md"
                
                # Create new symlink in .github directory
                New-Item -ItemType SymbolicLink -Path $newLocation -Target $targetFile -Force
                
                # Add new symlink location (but it will be ignored due to .gitignore)
                Write-Host "[${repoName}] - Created new symlink in .github/" -ForegroundColor Green
                
            } else {
                # It's a regular file, use git mv
                git mv ".github\instructions\copilot-instructions.md" ".github\copilot-instructions.md"
                Write-Host "[${repoName}] - Moved regular file" -ForegroundColor Green
            }
            
            # Check if instructions directory is now empty and remove it
            if (Test-Path $instructionsDir) {
                $dirContents = Get-ChildItem -Path $instructionsDir -Force
                if ($dirContents.Count -eq 0) {
                    Remove-Item -Path $instructionsDir -Force
                    Write-Host "[${repoName}] - Removed empty instructions directory" -ForegroundColor Cyan
                }
            }
            
        } catch {
            Write-Host "[${repoName}] - Error: $($_.Exception.Message)" -ForegroundColor Red
        }
        
        Pop-Location
    } else {
        Write-Host "[${repoName}] - No copilot-instructions.md found in instructions directory" -ForegroundColor Gray
    }
}

# Special handling for energy repository - create symlink
$energyRepo = Join-Path $baseDir "energy"
$energyGithubDir = Join-Path $energyRepo ".github"
$energySymlinkPath = Join-Path $energyGithubDir "copilot-instructions.md"

Write-Host "`nHandling energy repository..." -ForegroundColor Yellow

# Ensure .github directory exists
if (-not (Test-Path $energyGithubDir)) {
    New-Item -Path $energyGithubDir -ItemType Directory -Force | Out-Null
    Write-Host "[energy] - Created .github directory" -ForegroundColor Cyan
}

# Change to energy repository
Push-Location $energyRepo

try {
    # Remove existing file if it exists
    if (Test-Path $energySymlinkPath) {
        Remove-Item $energySymlinkPath -Force
        Write-Host "[energy] - Removed existing copilot-instructions.md" -ForegroundColor Cyan
    }
    
    # Try to create the symlink
    try {
        New-Item -ItemType SymbolicLink -Path $energySymlinkPath -Target $targetFile -Force
        Write-Host "[energy] - Created symlink to $targetFile" -ForegroundColor Green
    } catch {
        # If symlink creation fails, copy the file instead
        Write-Host "[energy] - Symlink creation failed, copying file instead" -ForegroundColor Yellow
        Copy-Item -Path $targetFile -Destination $energySymlinkPath -Force
        Write-Host "[energy] - Copied file from $targetFile" -ForegroundColor Green
    }
    
} catch {
    Write-Host "[energy] - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Pop-Location

Write-Host "`nMoving copilot-instructions.md files completed!" -ForegroundColor Green
