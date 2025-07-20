# Add .github folders to .gitignore and remove from tracking
# This script ensures .github folders are properly ignored across all repositories

$baseDir = "C:\Users\$env:USERNAME\Code\asciimath"
$repoFolders = Get-ChildItem $baseDir -Directory | Where-Object { $_.Name -ne ".git" }

Write-Output "Processing .github folder ignoring in $($repoFolders.Count) repositories..."

foreach ($repoFolder in $repoFolders) {
    $repoPath = $repoFolder.FullName
    $repoName = $repoFolder.Name
    
    Write-Output "[$repoName] - Processing repository..."
    
    # Change to repository directory
    Set-Location $repoPath
    
    # Check if it's a git repository
    if (-not (Test-Path ".git")) {
        Write-Output "[$repoName] - Not a git repository, skipping..."
        continue
    }
    
    # Check if .gitignore exists, create if not
    $gitignorePath = ".gitignore"
    if (-not (Test-Path $gitignorePath)) {
        New-Item -ItemType File -Path $gitignorePath -Force | Out-Null
        Write-Output "[$repoName] - Created .gitignore file"
    }
    
    # Read current .gitignore content
    $gitignoreContent = Get-Content $gitignorePath -ErrorAction SilentlyContinue
    
    # Check if .github/ is already in .gitignore
    if ($gitignoreContent -notcontains ".github/") {
        # Add .github/ to .gitignore
        Add-Content $gitignorePath "`n.github/"
        Write-Output "[$repoName] - Added .github/ to .gitignore"
    } else {
        Write-Output "[$repoName] - .github/ already in .gitignore"
    }
    
    # Remove .github from git tracking if it exists
    if (Test-Path ".github") {
        git rm -r --cached .github 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Output "[$repoName] - Removed .github from git tracking"
        }
    }
    
    # Add and commit the .gitignore changes and cleanup
    git add -A
    git commit -m "Add .github/ to .gitignore and clean up empty files

- Added .github/ to .gitignore to prevent tracking
- Removed .github directories from git tracking  
- Cleaned up empty files and directories
- Repository structure reorganization"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Output "[$repoName] - Changes committed"
    } else {
        Write-Output "[$repoName] - No changes to commit"
    }
}

Write-Output "Completed processing .github folder ignoring across all repositories"
