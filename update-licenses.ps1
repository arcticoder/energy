# PowerShell script to add Unlicense to all energy repositories

$unlicenseText = @"
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize laws, the author or authors
of this software dedicate any and all interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"@

# Repository list
$repos = @(
    "lqg-volume-kernel-catalog",
    "polymer-fusion-framework", 
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

$targetDirectory = "C:\Users\sherri3\Code\asciimath"
Set-Location $targetDirectory

Write-Host "Adding Unlicense to remaining repositories..." -ForegroundColor Green

foreach ($repo in $repos) {
    if (Test-Path $repo) {
        $licensePath = Join-Path $repo "LICENSE"
        Write-Host "Adding LICENSE to $repo" -ForegroundColor Cyan
        Set-Content -Path $licensePath -Value $unlicenseText -Encoding UTF8
        Write-Host "  ✓ Added LICENSE to $repo" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Repository $repo not found" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Finished adding Unlicense to all repositories!" -ForegroundColor Green