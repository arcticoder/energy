# PowerShell script to clone all repositories from the "energy" GitHub stars list
# and set up each repo with proper git config and workspace file

# Repository list extracted from https://github.com/stars/arcticoder/lists/energy
$repos = @(
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

# Git configuration
$gitUserName = "arcticoder"
$gitUserEmail = "arcticoder@users.noreply.github.com"

# Set target directory
$targetDirectory = "C:\Users\echo_\Code\asciimath"

# Ensure target directory exists
if (-not (Test-Path $targetDirectory)) {
    Write-Host "Creating target directory: $targetDirectory" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $targetDirectory -Force
}

# Change to target directory
Write-Host "Changing to target directory: $targetDirectory" -ForegroundColor Cyan
Set-Location $targetDirectory

Write-Host "Starting to clone and setup $($repos.Count) repositories from the energy list..." -ForegroundColor Green

foreach ($repo in $repos) {
    Write-Host "`nProcessing repository: $repo" -ForegroundColor Yellow
    
    # Check if repo directory already exists
    if (Test-Path $repo) {
        Write-Host "  Directory $repo already exists, skipping clone..." -ForegroundColor Orange
    } else {
        # Clone the repository
        Write-Host "  Cloning $repo..." -ForegroundColor Cyan
        $cloneResult = git clone "https://github.com/arcticoder/$repo.git" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Successfully cloned $repo" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Failed to clone $repo`: $cloneResult" -ForegroundColor Red
            continue
        }
    }
    
    # Navigate to repo directory
    Push-Location $repo
    
    try {
        # Set local git user configuration
        Write-Host "  Setting git user configuration..." -ForegroundColor Cyan
        git config user.name $gitUserName
        git config user.email $gitUserEmail
        Write-Host "  ✓ Git config set for $repo" -ForegroundColor Green
          # Check if .code-workspace file exists
        $workspaceFile = "$repo.code-workspace"
        if (-not (Test-Path $workspaceFile)) {
            Write-Host "  Creating $workspaceFile..." -ForegroundColor Cyan
            
            # Create basic workspace configuration
            $workspaceContent = @{
                folders = @(
                    @{
                        name = $repo
                        path = "."
                    }
                )
                settings = @{
                    "files.exclude" = @{
                        "**/.git" = $true
                        "**/node_modules" = $true
                        "**/__pycache__" = $true
                        "**/.pytest_cache" = $true
                        "**/venv" = $true
                        "**/.venv" = $true
                    }
                }
                extensions = @{
                    recommendations = @(
                        "ms-python.python",
                        "ms-vscode.cpptools",
                        "james-yu.latex-workshop"
                    )
                }
            }
            
            $workspaceJson = $workspaceContent | ConvertTo-Json -Depth 4
            Set-Content -Path $workspaceFile -Value $workspaceJson -Encoding UTF8
            
            # Add and commit the workspace file
            git add $workspaceFile
            $commitResult = git commit -m "Add VSCode workspace configuration" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ Created and committed $workspaceFile" -ForegroundColor Green
            } else {
                Write-Host "  ✓ Created $workspaceFile (no commit needed - $commitResult)" -ForegroundColor Green
            }
        } else {
            Write-Host "  $workspaceFile already exists" -ForegroundColor Orange
        }
        
    } catch {
        Write-Host "  ✗ Error setting up $repo`: $($_.Exception.Message)" -ForegroundColor Red
    } finally {
        # Return to parent directory
        Pop-Location
    }
}

Write-Host "`n🎉 Finished processing all repositories!" -ForegroundColor Green
Write-Host "Total repositories processed: $($repos.Count)" -ForegroundColor Green
