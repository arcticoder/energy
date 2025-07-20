# PowerShell script to list all uncommitted changes across all repositories

$asciimathPath = "C:\Users\$env:USERNAME\Code\asciimath"

# Get all subdirectories in the asciimath folder
$repos = Get-ChildItem -Path $asciimathPath -Directory

Write-Host "Checking uncommitted changes in $($repos.Count) repositories..." -ForegroundColor Cyan

$reposWithChanges = @()
$totalChangedFiles = 0

foreach ($repo in $repos) {
    $repoPath = $repo.FullName
    
    Push-Location $repoPath
    try {
        # Check if this is a git repository
        $isGitRepo = Test-Path ".git"
        
        if ($isGitRepo) {
            # Get status of uncommitted changes
            $statusOutput = git status --porcelain 2>$null
            
            if ($statusOutput) {
                $changedFiles = $statusOutput | Measure-Object | Select-Object -ExpandProperty Count
                $totalChangedFiles += $changedFiles
                
                Write-Host "`n[$($repo.Name)] - $changedFiles changed files" -ForegroundColor Yellow
                
                # Parse and display changes by type
                $staged = @()
                $unstaged = @()
                $untracked = @()
                
                foreach ($line in $statusOutput) {
                    $status = $line.Substring(0,2)
                    $filename = $line.Substring(3)
                    
                    switch ($status[0]) {
                        'A' { $staged += "Added: $filename" }
                        'M' { $staged += "Modified: $filename" }
                        'D' { $staged += "Deleted: $filename" }
                        'R' { $staged += "Renamed: $filename" }
                        'C' { $staged += "Copied: $filename" }
                    }
                    
                    switch ($status[1]) {
                        'M' { $unstaged += "Modified: $filename" }
                        'D' { $unstaged += "Deleted: $filename" }
                    }
                    
                    if ($status -eq '??') {
                        $untracked += "Untracked: $filename"
                    }
                }
                
                if ($staged) {
                    Write-Host "  Staged changes:" -ForegroundColor Green
                    $staged | ForEach-Object { Write-Host "    $_" -ForegroundColor Green }
                }
                
                if ($unstaged) {
                    Write-Host "  Unstaged changes:" -ForegroundColor Red
                    $unstaged | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
                }
                
                if ($untracked) {
                    Write-Host "  Untracked files:" -ForegroundColor Magenta
                    $untracked | ForEach-Object { Write-Host "    $_" -ForegroundColor Magenta }
                }
                
                $reposWithChanges += $repo.Name
            }
        } else {
            Write-Host "[$($repo.Name)] - Not a git repository" -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "[$($repo.Name)] - Error checking status: $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

Write-Host "`n" -NoNewline
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "Total repositories with changes: $($reposWithChanges.Count)" -ForegroundColor Yellow
Write-Host "Total changed files: $totalChangedFiles" -ForegroundColor Yellow

if ($reposWithChanges.Count -gt 0) {
    Write-Host "`nRepositories with uncommitted changes:" -ForegroundColor Yellow
    $reposWithChanges | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
} else {
    Write-Host "`nAll repositories are clean." -ForegroundColor Green
}
