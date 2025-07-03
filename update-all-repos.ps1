# PowerShell script to fetch and pull all repositories in the asciimath directory
# This script will update all energy-related repositories

# Set target directory using current username
$currentUser = $env:USERNAME
$targetDirectory = "C:\Users\$currentUser\Code\asciimath"

# Get list of all subdirectories (repositories)
$repos = Get-ChildItem -Path $targetDirectory -Directory | Where-Object { $_.Name -ne "energy" }

Write-Host "Starting git fetch and pull for all repositories in $targetDirectory..." -ForegroundColor Green
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
        Write-Host "  ⚠️  Skipping $repoName - not a git repository" -ForegroundColor Orange
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
            Write-Host "  ⚠️  Fetch completed with warnings: $fetchResult" -ForegroundColor Orange
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
            Write-Host "  ⚠️  Repository has uncommitted changes:" -ForegroundColor Orange
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

Write-Host "`n🎉 Update completed!" -ForegroundColor Green
Write-Host "📊 Results Summary:" -ForegroundColor Cyan
Write-Host "  ✓ Successfully updated: $successCount repositories" -ForegroundColor Green
Write-Host "  ❌ Failed to update: $failCount repositories" -ForegroundColor Red
Write-Host "  ⚠️  Skipped (not git repos): $skippedCount directories" -ForegroundColor Orange
Write-Host "  📁 Total processed: $($repos.Count) directories" -ForegroundColor Cyan

if ($failCount -gt 0) {
    Write-Host "`n⚠️  Some repositories failed to update. Check the output above for details." -ForegroundColor Orange
} else {
    Write-Host "`n🎉 All repositories are now up to date!" -ForegroundColor Green
}
