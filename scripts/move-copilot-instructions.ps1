# Move copilot-instructions.md files from .github/instructions/ to .github/ across all repositories
# and create symlink in energy repository

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
    
    # Check if the source file exists
    if (Test-Path $instructionsFile) {
        Write-Host "[${repoName}] - Moving copilot-instructions.md" -ForegroundColor Green
        
        # Change to repository directory for git operations
        Push-Location $repoPath
        
        try {
            # Use git mv to preserve history
            git mv ".github\instructions\copilot-instructions.md" ".github\copilot-instructions.md"
            
            # Check if instructions directory is now empty and remove it
            if ((Get-ChildItem -Path $instructionsDir -Force | Measure-Object).Count -eq 0) {
                Remove-Item -Path $instructionsDir -Force
                Write-Host "[${repoName}] - Removed empty instructions directory" -ForegroundColor Cyan
            }
            
        } catch {
            Write-Host "[${repoName}] - Error moving file: $($_.Exception.Message)" -ForegroundColor Red
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

Write-Host "`nCreating symlink in energy repository..." -ForegroundColor Yellow

# Change to energy repository
Push-Location $energyRepo

try {
    # Remove existing file if it exists
    if (Test-Path $energySymlinkPath) {
        Remove-Item $energySymlinkPath -Force
        Write-Host "[energy] - Removed existing copilot-instructions.md" -ForegroundColor Cyan
    }
    
    # Create the symlink
    New-Item -ItemType SymbolicLink -Path $energySymlinkPath -Target $targetFile -Force
    Write-Host "[energy] - Created symlink to $targetFile" -ForegroundColor Green
    
} catch {
    Write-Host "[energy] - Error creating symlink: $($_.Exception.Message)" -ForegroundColor Red
}

Pop-Location

Write-Host "`nMoving copilot-instructions.md files completed!" -ForegroundColor Green
