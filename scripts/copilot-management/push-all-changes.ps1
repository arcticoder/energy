# Push all committed changes across all repositories

$baseDir = "C:\Users\$env:USERNAME\Code\asciimath"
$repoFolders = Get-ChildItem $baseDir -Directory | Where-Object { $_.Name -ne ".git" }

Write-Output "Pushing changes in $($repoFolders.Count) repositories..."

$reposPushed = 0
$reposWithErrors = @()

foreach ($repoFolder in $repoFolders) {
    $repoPath = $repoFolder.FullName
    $repoName = $repoFolder.Name
    
    # Change to repository directory
    Set-Location $repoPath
    
    # Check if it's a git repository
    if (-not (Test-Path ".git")) {
        continue
    }
    
    # Check for unpushed commits
    $unpushedCommits = git log --oneline origin/main..HEAD 2>$null
    
    if ($unpushedCommits) {
        Write-Output "[$repoName] - Pushing $($unpushedCommits.Count) commits..."
        
        # Push to origin
        git push origin main 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Output "[$repoName] - Successfully pushed"
            $reposPushed++
        } else {
            Write-Output "[$repoName] - Error pushing changes"
            $reposWithErrors += $repoName
        }
    } else {
        Write-Output "[$repoName] - No unpushed commits"
    }
}

Write-Output "`nSummary:"
Write-Output "Repositories pushed: $reposPushed"

if ($reposWithErrors.Count -gt 0) {
    Write-Output "Repositories with push errors: $($reposWithErrors.Count)"
    $reposWithErrors | ForEach-Object { Write-Output "  - $_" }
} else {
    Write-Output "All repositories pushed successfully"
}
