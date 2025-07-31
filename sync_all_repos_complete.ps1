#!/usr/bin/env pwsh
# Extended repository sync script for all repositories

$rootPath = "$home\Code\asciimath"

# Get all directories that contain .git folders
$allRepos = Get-ChildItem -Path $rootPath -Directory | Where-Object { 
    Test-Path (Join-Path $_.FullName ".git") 
} | Sort-Object Name

$successCount = 0
$errorCount = 0
$totalRepos = $allRepos.Count

Write-Host "=== Complete Repository Sync Report ===" -ForegroundColor Magenta
Write-Host "Found $totalRepos total repositories in workspace" -ForegroundColor White
Write-Host ""

foreach ($repo in $allRepos) {
    $repoName = $repo.Name
    $repoPath = $repo.FullName
    
    Write-Host "📁 Processing: $repoName" -ForegroundColor Cyan
    Push-Location $repoPath
    
    try {
        # Check if it's a valid git repository
        $branch = git branch --show-current 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "   ⚠️  Not a valid git repository" -ForegroundColor Yellow
            continue
        }
        
        # Check repository status
        $status = git status --porcelain 2>$null
        $isClean = $LASTEXITCODE -eq 0 -and [string]::IsNullOrEmpty($status)
        
        if ($isClean) {
            Write-Host "   ✅ Repository is clean (branch: $branch)" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Repository has changes (branch: $branch)" -ForegroundColor Yellow
        }
        
        # Check if we can push
        $pushOutput = git push origin $branch 2>&1
        if ($LASTEXITCODE -eq 0) {
            if ($pushOutput -match "Everything up-to-date") {
                Write-Host "   📤 Up to date" -ForegroundColor Gray
            } else {
                Write-Host "   📤 Successfully pushed" -ForegroundColor Green
            }
            $successCount++
        } else {
            Write-Host "   ❌ Push failed or no remote: $($pushOutput -join ' ')" -ForegroundColor Red
            $errorCount++
        }
        
    } catch {
        Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    } finally {
        Pop-Location
    }
    
    Write-Host ""
}

Write-Host "=== FINAL SUMMARY ===" -ForegroundColor Magenta
Write-Host "Total repositories found: $totalRepos" -ForegroundColor White
Write-Host "Successful operations: $successCount" -ForegroundColor Green
Write-Host "Failed operations: $errorCount" -ForegroundColor Red
Write-Host "Success rate: $([math]::Round(($successCount / $totalRepos) * 100, 1))%" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Repository synchronization complete!" -ForegroundColor Green
