# PowerShell script to sync changes from energy repository to all other repositories
# This script will push energy repository changes and pull them into other repositories

# Set target directory using current username
$currentUser = $env:USERNAME
$targetDirectory = "C:\Users\$currentUser\Code\asciimath"
$energyRepoPath = "$targetDirectory\energy"

# First, ensure energy repository changes are committed and pushed
Write-Host "Syncing changes from energy repository to all other repositories..." -ForegroundColor Green
Write-Host "Step 1: Processing energy repository..." -ForegroundColor Cyan

Push-Location $energyRepoPath
try {
    # First, fetch latest changes from energy repository
    Write-Host "  🔄 Fetching latest changes from energy repository..." -ForegroundColor Cyan
    $fetchResult = git fetch --all 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Fetch successful" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Fetch completed with warnings: $fetchResult" -ForegroundColor DarkYellow
    }
    
    # Check current branch
    $currentBranch = git branch --show-current 2>$null
    if (-not $currentBranch) {
        $currentBranch = "main"  # fallback
    }
    
    # Pull latest changes if behind
    $behind = git rev-list HEAD..origin/$currentBranch --count 2>$null
    if ($behind -and $behind -gt 0) {
        Write-Host "  📥 Energy repository is $behind commits behind, pulling changes..." -ForegroundColor Cyan
        $pullResult = git pull origin $currentBranch 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Pull successful - updated $behind commits" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Pull failed: $pullResult" -ForegroundColor Red
        }
    } else {
        Write-Host "  ✓ Energy repository is up to date with remote" -ForegroundColor Green
    }
    
    # Check if there are uncommitted changes in energy repo
    $energyStatus = git status --porcelain 2>$null
    if ($energyStatus) {
        Write-Host "  📝 Found uncommitted changes in energy repository, committing..." -ForegroundColor Yellow
        git add . 2>$null
        $commitMessage = "Auto-sync: Updated energy repository - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git commit -m $commitMessage 2>$null
        Write-Host "  ✓ Committed changes to energy repository" -ForegroundColor Green
    }
    
    # Push energy repository changes
    Write-Host "  📤 Pushing energy repository changes..." -ForegroundColor Cyan
    $pushResult = git push 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Successfully pushed energy repository changes" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Push completed with warnings: $pushResult" -ForegroundColor DarkYellow
    }
} catch {
    Write-Host "  ❌ Error processing energy repository: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    Pop-Location
}

# Get list of all subdirectories (repositories) excluding energy
$repos = Get-ChildItem -Path $targetDirectory -Directory | Where-Object { $_.Name -ne "energy" }

Write-Host "`nStep 2: Updating all other repositories with latest changes..." -ForegroundColor Cyan
Write-Host "Found $($repos.Count) repositories to update" -ForegroundColor Cyan

$successCount = 0
$failCount = 0
$skippedCount = 0

foreach ($repo in $repos) {
    $repoName = $repo.Name
    $repoPath = $repo.FullName
    
    Write-Host "`nProcessing repository: $repoName" -ForegroundColor Yellow
    
    # Check if this is a git repository
    if (-not (Test-Path (Join-Path $repoPath ".git"))) {
        Write-Host "  ⚠️  Skipping $repoName - not a git repository" -ForegroundColor DarkYellow
        $skippedCount++
        continue
    }
    
    # Navigate to repo directory
    Push-Location $repoPath
    
    try {
        # Add safe directory configuration to prevent git ownership issues
        Write-Host "  📁 Adding safe directory configuration..." -ForegroundColor Cyan
        git config --global --add safe.directory $repoPath.Replace('\', '/') 2>$null
        
        # Fetch latest changes
        Write-Host "  🔄 Fetching latest changes..." -ForegroundColor Cyan
        $fetchResult = git fetch --all 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Fetch successful" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Fetch completed with warnings: $fetchResult" -ForegroundColor DarkYellow
        }
        
        # Check current branch
        $currentBranch = git branch --show-current 2>$null
        if (-not $currentBranch) {
            $currentBranch = "main"  # fallback
        }
        
        Write-Host "  📋 Current branch: $currentBranch" -ForegroundColor Cyan
        
        # Check if there are any changes to pull
        $status = git status --porcelain 2>$null
        $behind = git rev-list HEAD..origin/$currentBranch --count 2>$null
        
        if ($behind -and $behind -gt 0) {
            Write-Host "  📥 Repository is $behind commits behind, pulling changes..." -ForegroundColor Cyan
            $pullResult = git pull origin $currentBranch 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ Pull successful - updated $behind commits" -ForegroundColor Green
            } else {
                Write-Host "  ❌ Pull failed: $pullResult" -ForegroundColor Red
                $failCount++
                continue
            }
        } else {
            Write-Host "  ✓ Repository is up to date" -ForegroundColor Green
        }
        
        # Check for uncommitted changes
        if ($status) {
            Write-Host "  ⚠️  Repository has uncommitted changes:" -ForegroundColor DarkYellow
            git status --short
        }
        
        $successCount++
        
    } catch {
        Write-Host "  ❌ Error updating $repoName`: $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
    } finally {
        # Return to original directory
        Pop-Location
    }
}

Write-Host "`n🎉 Synchronization completed!" -ForegroundColor Green
Write-Host "📊 Sync Results Summary:" -ForegroundColor Cyan
Write-Host "  ✓ Energy repository: Pulled latest changes, committed local changes, and pushed" -ForegroundColor Green
Write-Host "  ✓ Successfully updated: $successCount repositories" -ForegroundColor Green
Write-Host "  ❌ Failed to update: $failCount repositories" -ForegroundColor Red
Write-Host "  ⚠️  Skipped (not git repos): $skippedCount directories" -ForegroundColor DarkYellow
Write-Host "  📁 Total processed: $($repos.Count) directories" -ForegroundColor Cyan

if ($failCount -gt 0) {
    Write-Host "`n⚠️  Some repositories failed to update. Check the output above for details." -ForegroundColor DarkYellow
} else {
    Write-Host "`n🎉 All repositories are now synchronized with energy repository changes!" -ForegroundColor Green
}
