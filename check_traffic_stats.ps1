# GitHub Traffic Stats Checker for arcticoder repositories
# This script checks traffic stats for all repositories in the past week

$repos = @(
    "energy",
    "artificial-gravity-field-generator", 
    "casimir-anti-stiction-metasurface-coatings",
    "casimir-environmental-enclosure-platform",
    "casimir-nanopositioning-platform",
    "casimir-tunable-permittivity-stacks",
    "casimir-ultra-smooth-fabrication-platform",
    "elemental-transmutator",
    "enhanced-simulation-hardware-abstraction-framework",
    "lqg-anec-framework",
    "lqg-cosmological-constant-predictor",
    "lqg-volume-kernel-catalog",
    "lqg-first-principles-fine-structure-constant",
    "lqg-first-principles-gravitational-constant",
    "lqg-ftl-metric-engineering",
    "lqg-polymer-field-generator",
    "lqg-positive-matter-assembler",
    "lqg-volume-quantization-controller",
    "lorentz-violation-pipeline",
    "negative-energy-generator",
    "polymer-fusion-framework",
    "polymerized-lqg-matter-transporter",
    "polymerized-lqg-replicator-recycler",
    "su2-3nj-closedform",
    "su2-3nj-generating-functional",
    "su2-3nj-recurrences",
    "su2-3nj-uniform-closed-form",
    "su2-node-matrix-elements",
    "unified-gut-polymerization",
    "unified-lqg",
    "unified-lqg-qft",
    "warp-bubble-assemble-expressions",
    "warp-bubble-connection-curvature",
    "warp-bubble-coordinate-spec",
    "warp-bubble-einstein-equations",
    "warp-bubble-exotic-matter-density",
    "warp-bubble-metric-ansatz",
    "warp-bubble-mvp-simulator",
    "warp-bubble-optimizer",
    "warp-bubble-parameter-constraints",
    "warp-bubble-qft",
    "warp-bubble-shape-catalog",
    "warp-convergence-analysis",
    "warp-curvature-analysis",
    "warp-discretization",
    "warp-field-coils",
    "warp-lqg-midisuperspace",
    "warp-mock-data-generator",
    "warp-sensitivity-analysis",
    "warp-signature-workflow",
    "warp-solver-equations",
    "warp-spacetime-stability-controller"
)

Write-Host "=== GitHub Traffic Stats for arcticoder repositories (Past Week) ===" -ForegroundColor Cyan
Write-Host "Date Range: Past 14 days (GitHub's available range)" -ForegroundColor Gray
Write-Host ""

$totalViews = 0
$totalUniqeViews = 0
$totalClones = 0
$totalUniqueClones = 0

foreach ($repo in $repos) {
    Write-Host "Repository: arcticoder/$repo" -ForegroundColor Yellow
    Write-Host ("-" * 60)
    
    # Get views traffic
    try {
        $viewsOutput = gh api repos/arcticoder/$repo/traffic/views 2>$null
        if ($viewsOutput) {
            $views = $viewsOutput | ConvertFrom-Json
            Write-Host "📈 Views:" -ForegroundColor Green
            Write-Host "   Total: $($views.count), Unique: $($views.uniques)"
            $totalViews += $views.count
            $totalUniqeViews += $views.uniques
            
            if ($views.views -and $views.views.Count -gt 0) {
                $recentViews = $views.views | Sort-Object timestamp -Descending | Select-Object -First 7
                foreach ($day in $recentViews) {
                    $date = ([DateTime]$day.timestamp).ToString("MMM dd")
                    if ($day.count -gt 0) {
                        Write-Host "   $date : $($day.count) views ($($day.uniques) unique)" -ForegroundColor White
                    }
                }
            }
        }
    } catch {
        Write-Host "📈 Views: Access denied or repository not found" -ForegroundColor Red
    }
    
    # Get clones traffic  
    try {
        $clonesOutput = gh api repos/arcticoder/$repo/traffic/clones 2>$null
        if ($clonesOutput) {
            $clones = $clonesOutput | ConvertFrom-Json
            Write-Host "📦 Clones:" -ForegroundColor Blue
            Write-Host "   Total: $($clones.count), Unique: $($clones.uniques)"
            $totalClones += $clones.count
            $totalUniqueClones += $clones.uniques
            
            if ($clones.clones -and $clones.clones.Count -gt 0) {
                $recentClones = $clones.clones | Sort-Object timestamp -Descending | Select-Object -First 7
                foreach ($day in $recentClones) {
                    $date = ([DateTime]$day.timestamp).ToString("MMM dd")
                    if ($day.count -gt 0) {
                        Write-Host "   $date : $($day.count) clones ($($day.uniques) unique)" -ForegroundColor White
                    }
                }
            }
        }
    } catch {
        Write-Host "📦 Clones: Access denied or repository not found" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host "=== SUMMARY ===" -ForegroundColor Cyan
Write-Host "Total Views: $totalViews (Unique: $totalUniqeViews)" -ForegroundColor Green
Write-Host "Total Clones: $totalClones (Unique: $totalUniqueClones)" -ForegroundColor Blue
Write-Host "Repositories Checked: $($repos.Count)" -ForegroundColor White
