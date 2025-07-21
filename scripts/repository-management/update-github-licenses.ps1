# PowerShell script to update GitHub license metadata for all energy repositories

# Repository list
$repos = @(
    "energy",
    "elemental-transmutator",
    "lorentz-violation-pipeline", 
    "lqg-anec-framework",
    "lqg-volume-kernel-catalog",
    "polymer-fusion-framework", 
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
    "warp-lqg-midisuperspace",
    "warp-mock-data-generator",
    "warp-sensitivity-analysis",
    "warp-signature-workflow",
    "warp-solver-equations",
    "warp-solver-validation"
)

Write-Host "Updating GitHub license metadata for all repositories..." -ForegroundColor Green

foreach ($repo in $repos) {
    Write-Host "Updating license for arcticoder/$repo" -ForegroundColor Cyan
    
    # Update repository license
    $result = gh api repos/arcticoder/$repo --method PATCH --field license_template=unlicense 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Updated license for $repo" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Could not update license for $repo (may need manual update)" -ForegroundColor Yellow
    }
}

Write-Host "`n🎉 Finished updating GitHub license metadata!" -ForegroundColor Green