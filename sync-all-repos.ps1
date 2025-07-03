# PowerShell script to pull all present git repos and clone missing ones
# Update the $missingRepos hashtable with the correct git URLs for missing repos

$basePath = "C:\Users\sherri3\Code\asciimath"

$foldersToPull = @(
    "elemental-transmutator",
    "lorentz-violation-pipeline",
    "lqg-anec-framework",
    "negative-energy-generator",
    "polymer-fusion-framework",
    "su2-3nj-closedform",
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

$missingRepos = @{
    "lqg-volume-kernel-catalog" = "<GIT_URL_HERE>"
    "su2-3nj-generating-functional" = "<GIT_URL_HERE>"
    "su2-3nj-recurrences" = "<GIT_URL_HERE>"
}

# Pull for present folders
foreach ($folder in $foldersToPull) {
    $repoPath = Join-Path $basePath $folder
    if (Test-Path $repoPath) {
        Write-Host "Pulling in $repoPath..."
        Push-Location $repoPath
        git pull
        Pop-Location
    } else {
        Write-Host "$folder is missing, will be cloned if URL is provided."
    }
}

# Clone missing repos
foreach ($repo in $missingRepos.GetEnumerator()) {
    $repoPath = Join-Path $basePath $repo.Key
    if (-not (Test-Path $repoPath)) {
        if ($repo.Value -ne "<GIT_URL_HERE>") {
            Write-Host "Cloning $($repo.Key) from $($repo.Value)..."
            git clone $repo.Value $repoPath
        } else {
            Write-Host "No git URL provided for $($repo.Key), skipping."
        }
    }
}
