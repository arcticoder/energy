param(
    [string]$InputFile = "highlights-dag.ndjson",
    [string]$OutputFile = "highlights-dag.presentation.html"
)

# Function to convert Unicode math to LaTeX
function Convert-ToLatex($mathString) {
    if (-not $mathString) { return "" }
    
    # Convert Unicode symbols to LaTeX
    $latex = $mathString
    $latex = $latex -replace "μ", "\mu"
    $latex = $latex -replace "ν", "\nu"
    $latex = $latex -replace "ρ", "\rho"
    $latex = $latex -replace "σ", "\sigma"
    $latex = $latex -replace "≥", "\geq"
    $latex = $latex -replace "≤", "\leq"
    $latex = $latex -replace "∞", "\infty"
    $latex = $latex -replace "∫", "\int"
    $latex = $latex -replace "π", "\pi"
    $latex = $latex -replace "θ", "\theta"
    $latex = $latex -replace "λ", "\lambda"
    # Fix rendering issues
    $latex = $latex -replace "\\\\text", "\text"
    $latex = $latex -replace "\\\\rightarrow", "\rightarrow"
    $latex = $latex -replace "\\\\to", "\to"
    $latex = $latex -replace "\\\\Rightarrow", "\Rightarrow"
    
    return $latex
}

# Function to create GitHub links for source files
function Format-SourceFiles($sourceFiles) {
    if (-not $sourceFiles) { return "" }
    
    $baseUrl = "https://github.com/sherri3"
    $links = @()
    
    foreach ($file in $sourceFiles) {
        $repoName = $file.Split('/')[0]
        $filePath = $file -replace "^[^/]+/", ""
        $url = "$baseUrl/$repoName/blob/main/$filePath"
        $links += "<a href='$url' target='_blank' style='color: #007bff; text-decoration: none;'>$file</a>"
    }
    
    return $links -join ", "
}

Write-Host "Generating standalone HTML presentation from DAG..." -ForegroundColor Cyan

# Read and parse the NDJSON file
$dagLines = Get-Content $InputFile
$nodes = @{}
$edges = @{}

# Parse nodes and edges
foreach ($line in $dagLines) {
    $item = $line | ConvertFrom-Json
    if ($item.type -eq "edge") {
        $edges[$item.id] = $item
    } else {
        $nodes[$item.id] = $item
    }
}

Write-Host "Parsed $($nodes.Count) nodes and $($edges.Count) edges" -ForegroundColor Green

# Group nodes in logical order
$orderedNodes = $nodes.Values | Sort-Object { 
    # Sort by dependencies and importance
    if ($_.id -eq "constraint_algebra") { return 1 }
    if ($_.id -eq "anec_framework") { return 2 }
    if ($_.id -eq "warp_bubble_proof") { return 3 }
    if ($_.id -eq "exotic_matter_analysis") { return 4 }
    if ($_.id -eq "energy_conditions") { return 5 }
    return 10
}

# Start building HTML
$html = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Highlights - Mathematical Physics & Quantum Gravity</title>
    
    <!-- MathJax Configuration -->
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['`$', '`$']],
                displayMath: [['`$`$', '`$`$']],
                processEscapes: true,
                processEnvironments: true
            },
            options: {
                ignoreHtmlClass: "tex2jax_ignore",
                processHtmlClass: "tex2jax_process"
            }
        };
    </script>
    <script type="text/javascript" id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    
    <style>
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: white;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
      }
      .header {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: white;
        border-radius: 12px;
        margin-bottom: 40px;
      }
      .header h1 {
        font-size: 2.5em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      }
      .header p {
        font-size: 1.2em;
        margin: 15px 0 0 0;
        opacity: 0.9;
      }
      .discovery {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #007bff;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }
      .discovery:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
      }
      .discovery-title {
        font-size: 1.3em;
        font-weight: bold;
        color: #1a1a2e;
        margin-bottom: 10px;
      }
      .discovery-description {
        margin-bottom: 15px;
        line-height: 1.7;
      }
      .mathematics {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #007bff;
        overflow-x: auto;
        font-size: 0.9em;
        line-height: 1.4;
      }
      .mathematics .MathJax {
        font-size: 0.85em !important;
      }
      .MathJax_Display {
        font-size: 0.9em !important;
        overflow-x: auto;
        overflow-y: hidden;
      }
      .impact {
        font-style: italic;
        color: #28a745;
        background: #f8fff9;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid #28a745;
        margin-top: 15px;
      }
      .summary-section {
        margin: 50px 0;
        padding: 30px;
        background: #f8f9fa;
        border-radius: 12px;
      }
      .footer {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        background: #1a1a2e;
        color: white;
        border-radius: 12px;
      }
      .footer p {
        margin: 10px 0;
      }
    </style>
</head>
<body>
    <div class="container">        <div class="header">
            <h1>Research Highlights</h1>
            <p>Mathematical Physics & Quantum Gravity Discoveries</p>
        </div>

        <!-- Table of Contents -->
        <div class="summary-section">
            <h2 style="text-align: center; color: #1a1a2e; margin-bottom: 30px;">Table of Contents</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color: #007bff; margin-bottom: 15px;">Points of Interest</h3>
                    <ul style="list-style-type: none; padding: 0;">
"@

foreach ($node in $orderedNodes) {
    $anchorId = $node.id -replace "_", "-"
    $html += @"
                        <li style="margin: 8px 0;"><a href="#node-$anchorId" style="color: #007bff; text-decoration: none;">$($node.title)</a></li>
"@
}

$html += @"
                    </ul>
                </div>
                <div>
                    <h3 style="color: #28a745; margin-bottom: 15px;">Research Connections</h3>
                    <ul style="list-style-type: none; padding: 0;">
"@

foreach ($edge in $edges.Values) {
    $sourceNode = $nodes[$edge.source]
    $targetNode = $nodes[$edge.target]
    if ($sourceNode -and $targetNode) {
        $anchorId = $edge.id -replace "_", "-"
        $html += @"
                        <li style="margin: 8px 0; font-size: 0.9em;"><a href="#edge-$anchorId" style="color: #28a745; text-decoration: none;">$($sourceNode.title) → $($targetNode.title)</a></li>
"@
    }
}

$html += @"
                    </ul>
                </div>
            </div>
        </div>

"@

# Generate content for each discovery
foreach ($node in $orderedNodes) {
    $anchorId = $node.id -replace "_", "-"
    $html += @"
        <div class="discovery" id="node-$anchorId">
            <div class="discovery-title">$($node.title)</div>
            <div class="discovery-description">$($node.description)</div>

"@
    
    if ($node.mathematics) {
        $mathematics = Convert-ToLatex $node.mathematics
        $html += @"
            <div class="mathematics">
                `$`$$mathematics`$`$
            </div>

"@
    }
    
    if ($node.source_files) {
        $sourceLinks = Format-SourceFiles $node.source_files
        $html += @"
            <div style="margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 6px; font-size: 0.9em;">
                <strong>Source Files:</strong> $sourceLinks
            </div>

"@
    }
    
    if ($node.impact) {
        $html += @"
            <div class="impact">
                $($node.impact)
            </div>

"@
    }
    
    $html += @"
        </div>

"@
}

# Add connections analysis
$html += @"
        <div class="summary-section">
            <h2 style="text-align: center; color: #1a1a2e; margin-bottom: 30px;">Research Connections and Dependencies</h2>
            
"@

foreach ($edge in $edges.Values) {
    $sourceNode = $nodes[$edge.source]
    $targetNode = $nodes[$edge.target]
    if ($sourceNode -and $targetNode) {
        $anchorId = $edge.id -replace "_", "-"
        $relationshipText = if ($edge.relationship -match '\$.*\$') { 
            # Already has LaTeX delimiters
            $edge.relationship 
        } else { 
            # Wrap in LaTeX delimiters
            "`$$($edge.relationship)`$" 
        }
        
        $html += @"
            <div class="discovery" id="edge-$anchorId">
                <div class="discovery-title">$($sourceNode.title) → $($targetNode.title)</div>
                <div class="discovery-description">
                    <strong>Relationship:</strong> $relationshipText - $($edge.description)
"@
        
        if ($edge.mathematics) {
            $mathematics = Convert-ToLatex $edge.mathematics
            $html += @"
                    <div class="mathematics">
                        `$`$$mathematics`$`$
                    </div>
"@
        }
        
        $html += @"
                    <br><br>
                    <strong>How this connection works:</strong> $($sourceNode.title) $relationshipText $($targetNode.title) because $($edge.description). This dependency is essential for understanding how $($sourceNode.impact) directly influences $($targetNode.impact).
                </div>
            </div>

"@
    }
}

$html += @"
        </div>

"@

# Add summary section
$html += @"
        <div class="summary-section">
            <h2>Research Overview</h2>
            <p style="font-size: 1.1em; margin: 20px 0;">
                This collection documents <strong>$($nodes.Count)</strong> theoretical developments in quantum gravity, spacetime engineering, and mathematical physics. Each discovery builds upon previous work through a network of mathematical dependencies and theoretical constraints.
            </p>
        </div>

        <div class="footer">
            <p><strong>Data Sources:</strong></p>
            <p><strong>DAG Structure:</strong> highlights-dag.ndjson | 
               <strong>Documentation Index:</strong> documentation-index.ndjson | 
               <strong>Uncertainty Analysis:</strong> UQ-TODO.ndjson</p>
            <p style="margin-top: 20px;">
                <em>Generated automatically from research highlights database</em>
            </p>
        </div>
    </div>
</body>
</html>
"@

# Write the HTML file
$html | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "Generated $OutputFile" -ForegroundColor Green
Write-Host "Presentation includes: $($nodes.Count) discoveries and research connections" -ForegroundColor Yellow
Write-Host "Open the HTML file in a browser to view the presentation" -ForegroundColor Cyan
Write-Host "Script completed!" -ForegroundColor Green
