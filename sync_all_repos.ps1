#!/usr/bin/env pwsh
# Comprehensive repository sync script

$rootPath = "C:\Users\sherri3\Code\asciimath"

$repos = @(
    "artificial-gravity-field-generator",
    "energy", 
    "unified-lqg",
    "warp-field-coils", 
    "lqg-positive-matter-assembler",
    "warp-sensitivity-analysis",
    "warp-convergence-analysis",
    "negative-energy-generator",
    "polymer-fusion-framework",
    "warp-bubble-optimizer",
    "lqg-anec-framework",
    "medical-tractor-array"
)

$successCount = 0
$totalRepos = $repos.Count

Write-Host "=== Repository Sync Report ===" -ForegroundColor Magenta
Write-Host "Processing $totalRepos key repositories..." -ForegroundColor White
Write-Host ""

foreach ($repo in $repos) {
    $repoPath = Join-Path $rootPath $repo
    
    if (Test-Path $repoPath) {
        Write-Host "📁 Processing: $repo" -ForegroundColor Cyan
        Push-Location $repoPath
        
        try {
            # Check repository status
            $status = git status --porcelain 2>$null
            $isClean = $LASTEXITCODE -eq 0 -and [string]::IsNullOrEmpty($status)
            
            if ($isClean) {
                Write-Host "   ✅ Repository is clean" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️  Repository has changes" -ForegroundColor Yellow
            }
            
            # Attempt push
            $pushOutput = git push origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                if ($pushOutput -match "Everything up-to-date") {
                    Write-Host "   📤 Up to date" -ForegroundColor Gray
                } else {
                    Write-Host "   📤 Successfully pushed" -ForegroundColor Green
                }
                $successCount++
            } else {
                Write-Host "   ❌ Push failed: $pushOutput" -ForegroundColor Red
            }
            
        } catch {
            Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        } finally {
            Pop-Location
        }
        
        Write-Host ""
    } else {
        Write-Host "📁 $repo - Directory not found" -ForegroundColor Red
        Write-Host ""
    }
}

Write-Host "=== SUMMARY ===" -ForegroundColor Magenta
Write-Host "Repositories processed: $totalRepos" -ForegroundColor White
Write-Host "Successful operations: $successCount" -ForegroundColor Green
Write-Host "Success rate: $([math]::Round(($successCount / $totalRepos) * 100, 1))%" -ForegroundColor Cyan
