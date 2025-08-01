# List git commits from the past 30 minutes across all asciimath repositories
# Shows only the full file paths that were changed
#
# USAGE EXAMPLES:
#   .\list_recent_commits.ps1                    # Show all commit details and files from past 30 minutes
#   .\list_recent_commits.ps1 -Minutes 60       # Show commits from past 60 minutes
#   .\list_recent_commits.ps1 -FilesOnly         # Show only file paths, no commit details
#   .\list_recent_commits.ps1 -Minutes 120 -FilesOnly  # Show only files from past 2 hours

param(
    [int]$Minutes = 30,
    [switch]$FilesOnly
)

# Get the base directory
$BaseDir = "C:\Users\$env:USERNAME\Code\asciimath"

# Calculate the time threshold
$TimeThreshold = (Get-Date).AddMinutes(-$Minutes)
$GitTimeFormat = $TimeThreshold.ToString("yyyy-MM-dd HH:mm:ss")

if (-not $FilesOnly) {
    Write-Host "Scanning for commits in the past $Minutes minutes (since $GitTimeFormat)..." -ForegroundColor Green
    Write-Host "Base directory: $BaseDir" -ForegroundColor Yellow
    Write-Host ""
}

# Get all subdirectories that contain .git folders
$GitRepos = Get-ChildItem -Path $BaseDir -Directory | Where-Object { 
    Test-Path (Join-Path $_.FullName ".git") 
}

$TotalChangedFiles = 0
$AllChangedFiles = @()

foreach ($Repo in $GitRepos) {
    $RepoPath = $Repo.FullName
    $RepoName = $Repo.Name
    
    # Change to repository directory
    Push-Location $RepoPath
    
    try {
        # Get commits from the past X minutes with file names
        $RecentCommits = git log --since="$GitTimeFormat" --name-only --pretty=format:"COMMIT_START:%H:%ci:%s" 2>$null
        
        if ($RecentCommits) {
            if (-not $FilesOnly) {
                Write-Host "Repository: $RepoName" -ForegroundColor Cyan
                Write-Host "Location: $RepoPath" -ForegroundColor Gray
            }
            
            $CurrentCommit = $null
            $CommitFiles = @()
            
            foreach ($Line in $RecentCommits) {
                if ($Line -match "^COMMIT_START:(.+):(.+):(.+)$") {
                    # Process previous commit if exists
                    if ($CurrentCommit -and $CommitFiles.Count -gt 0) {
                        if (-not $FilesOnly) {
                            Write-Host "  Commit: $($CurrentCommit.Hash)" -ForegroundColor White
                            Write-Host "  Date: $($CurrentCommit.Date)" -ForegroundColor Gray
                            Write-Host "  Message: $($CurrentCommit.Message)" -ForegroundColor Gray
                            Write-Host ""
                        }
                        
                        foreach ($File in $CommitFiles) {
                            if ($File.Trim()) {
                                $FullPath = Join-Path $RepoPath $File
                                if ($FilesOnly) {
                                    Write-Host $FullPath
                                } else {
                                    Write-Host $FullPath -ForegroundColor Green
                                }
                                $AllChangedFiles += $FullPath
                                $TotalChangedFiles++
                            }
                        }
                        
                        if (-not $FilesOnly) {
                            Write-Host ""
                        }
                    }
                    
                    # Start new commit
                    $CurrentCommit = @{
                        Hash = $Matches[1]
                        Date = $Matches[2]
                        Message = $Matches[3]
                    }
                    $CommitFiles = @()
                } elseif ($Line.Trim() -and $CurrentCommit) {
                    # Add file to current commit
                    $CommitFiles += $Line.Trim()
                }
            }
            
            # Process the last commit
            if ($CurrentCommit -and $CommitFiles.Count -gt 0) {
                if (-not $FilesOnly) {
                    Write-Host "  Commit: $($CurrentCommit.Hash)" -ForegroundColor White
                    Write-Host "  Date: $($CurrentCommit.Date)" -ForegroundColor Gray
                    Write-Host "  Message: $($CurrentCommit.Message)" -ForegroundColor Gray
                    Write-Host ""
                }
                
                foreach ($File in $CommitFiles) {
                    if ($File.Trim()) {
                        $FullPath = Join-Path $RepoPath $File
                        if ($FilesOnly) {
                            Write-Host $FullPath
                        } else {
                            Write-Host $FullPath -ForegroundColor Green
                        }
                        $AllChangedFiles += $FullPath
                        $TotalChangedFiles++
                    }
                }
                
                if (-not $FilesOnly) {
                    Write-Host ""
                }
            }
        }
    }
    catch {
        if (-not $FilesOnly) {
            Write-Host "Error processing repository $RepoName : $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    finally {
        Pop-Location
    }
}

if (-not $FilesOnly) {
    Write-Host "Scan complete. Total files changed in the past $Minutes minutes: $TotalChangedFiles" -ForegroundColor Yellow
}
