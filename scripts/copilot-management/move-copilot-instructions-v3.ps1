# Move copilot-instructions.md files from .github/instructions/ to .github/ 
# Remove symlinks and copy the actual content

$baseDir = "C:\Users\$env:USERNAME\Code\asciimath"
$targetFile = "G:\My Drive\code\ai\tech-roadmap\.vscode-instructions.md"

# Get all repository directories
$repos = Get-ChildItem -Path $baseDir -Directory | Where-Object { $_.Name -ne ".github" }

Write-Host "Processing copilot-instructions.md files in $($repos.Count) repositories..."

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
            # Simply remove the old file and copy the target content to new location
            Remove-Item $instructionsFile -Force
            Copy-Item -Path $targetFile -Destination $newLocation -Force
            
            Write-Host "[${repoName}] - Moved and copied content" -ForegroundColor Green
            
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

# Special handling for energy repository - copy the content
$energyRepo = Join-Path $baseDir "energy"
$energyGithubDir = Join-Path $energyRepo ".github"
$energyTargetPath = Join-Path $energyGithubDir "copilot-instructions.md"

Write-Host "`nHandling energy repository..." -ForegroundColor Yellow

# Ensure .github directory exists
if (-not (Test-Path $energyGithubDir)) {
    New-Item -Path $energyGithubDir -ItemType Directory -Force | Out-Null
    Write-Host "[energy] - Created .github directory" -ForegroundColor Cyan
}

# Change to energy repository
Push-Location $energyRepo

try {
    # Copy the target file content
    Copy-Item -Path $targetFile -Destination $energyTargetPath -Force
    Write-Host "[energy] - Copied content from $targetFile" -ForegroundColor Green
    
} catch {
    Write-Host "[energy] - Error: $($_.Exception.Message)" -ForegroundColor Red
}

Pop-Location

Write-Host "`nCompleted processing copilot-instructions.md files!" -ForegroundColor Green
