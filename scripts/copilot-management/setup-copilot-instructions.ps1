# PowerShell script to create copilot-instructions.md symlinks in all repositories

$asciimathPath = "C:\Users\$env:USERNAME\Code\asciimath"
$targetFile = "E:\My Drive\code\ai\tech-roadmap\.vscode-instructions.md"

# Get all subdirectories in the asciimath folder
$repos = Get-ChildItem -Path $asciimathPath -Directory

Write-Host "Setting up copilot-instructions.md symlinks in $($repos.Count) repositories..."

foreach ($repo in $repos) {
    $repoPath = $repo.FullName
    $githubPath = Join-Path $repoPath ".github"
    $instructionsPath = Join-Path $githubPath "instructions"
    $symlinkPath = Join-Path $instructionsPath "copilot-instructions.md"
    
    Write-Host "Processing: $($repo.Name)"
    
    # Create .github directory if it doesn't exist
    if (!(Test-Path $githubPath)) {
        New-Item -Path $githubPath -ItemType Directory -Force | Out-Null
        Write-Host "  Created .github directory"
    }
    
    # Create instructions directory if it doesn't exist
    if (!(Test-Path $instructionsPath)) {
        New-Item -Path $instructionsPath -ItemType Directory -Force | Out-Null
        Write-Host "  Created instructions directory"
    }
    
    # Remove existing symlink if it exists
    if (Test-Path $symlinkPath) {
        Remove-Item $symlinkPath -Force
        Write-Host "  Removed existing symlink"
    }
    
    # Create the symlink
    try {
        New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $targetFile -Force | Out-Null
        Write-Host "  Created symlink successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "  Failed to create symlink: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Setup completed!"
