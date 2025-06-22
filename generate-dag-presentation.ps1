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
    
    return $latex
}

# Function to get node HTML
function Get-NodeHTML($node) {
    $html = @"
        <div class="discovery">
            <div class="discovery-title">$($node.title)</div>
            <div class="discovery-description">$($node.description)</div>

"@
    
    if ($node.mathematics) {
        $math = Convert-ToLatex $node.mathematics
        $html += @"
            <div class="mathematics">
                `$$math`$
            </div>

"@
    }
    
    if ($node.code) {
        $html += @"
            <div class="code-block">
                <pre><code>$($node.code)</code></pre>
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
    return $html
}

# Function to get edge HTML
function Get-EdgeHTML($edge, $sourceNode, $targetNode) {
    $html = @"
        <div class="edge-item">
            <div class="discovery-title">$($sourceNode.title) → $($targetNode.title)</div>
            <div class="discovery-description">
                <strong>Relationship:</strong> $($edge.relationship) - $($edge.description)
                <br><br>

"@
    
    if ($edge.mathematics) {
        $math = Convert-ToLatex $edge.mathematics
        $html += @"
                <div class="mathematics">
                    `$$math`$
                </div>
                <br>

"@
    }
    
    $html += @"
                <strong>How this connection works:</strong> $($sourceNode.title) $($edge.relationship) $($targetNode.title) because $($edge.description). This dependency is essential for understanding how $($sourceNode.impact) directly influences $($targetNode.impact).
            </div>
        </div>

"@
    return $html
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

# Build adjacency lists for traversal
$outgoing = @{}
$incoming = @{}
foreach ($edge in $edges.Values) {
    if (-not $outgoing[$edge.source]) { $outgoing[$edge.source] = @() }
    if (-not $incoming[$edge.target]) { $incoming[$edge.target] = @() }
    $outgoing[$edge.source] += $edge
    $incoming[$edge.target] += $edge
}

# Find root nodes (nodes with no predecessors)
$rootNodes = @()
foreach ($nodeId in $nodes.Keys) {
    if (-not $incoming[$nodeId] -or $incoming[$nodeId].Count -eq 0) {
        $rootNodes += $nodeId
    }
}

Write-Host "Found $($rootNodes.Count) root nodes: $($rootNodes -join ', ')" -ForegroundColor Green

# Generate HTML
$html = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Highlights - DAG Presentation</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            },
            svg: {
                fontCache: 'global'
            }
        };
    </script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
            border-radius: 15px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            padding: 30px 0;
            border-bottom: 3px solid #3498db;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
        }
        
        .discovery {
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 6px solid #3498db;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .discovery:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .discovery-title {
            font-size: 1.8em;
            font-weight: bold;
            color: #1a1a2e;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        .discovery-description {
            font-size: 1.1em;
            margin-bottom: 20px;
            line-height: 1.9;
            text-align: justify;
        }
        
        .mathematics {
            background: #f8f9fa;
            padding: 25px;
            margin: 20px 0;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            font-size: 1.2em !important;
            text-align: center;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .mathematics .MathJax {
            font-size: 1.3em !important;
        }
        
        .code-block {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            overflow-x: auto;
            border: 1px solid #34495e;
        }
        
        .code-block pre {
            margin: 0;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            line-height: 1.4;
        }
        
        .impact {
            background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            margin-top: 20px;
            font-weight: 500;
            font-style: italic;
        }
        
        .edge-item {
            margin-bottom: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-left: 6px solid #f39c12;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }
        
        .edge-section {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px solid #e74c3c;
        }
        
        .summary-section {
            background: linear-gradient(135deg, #ddd6fe 0%, #e0e7ff 100%);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
            text-align: center;
            border: 2px solid #8b5cf6;
        }
        
        .summary-section h2 {
            color: #5b21b6;
            margin-bottom: 20px;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #6c757d;
            border-top: 2px solid #dee2e6;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        strong {
            color: #2c3e50;
        }
        
        .section-header {
            font-size: 2em;
            color: #1a1a2e;
            text-align: center;
            margin: 40px 0 30px 0;
            padding: 20px;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border-radius: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
    </style>
</head>

<body>
    <div class="container">        <div class="header">
            <h1>Research Highlights</h1>
            <p>Mathematical Physics & Quantum Gravity DAG Traversal</p>
        </div>

"@

# Traverse the DAG starting from root nodes
$visited = @{}
$script:traversalOrder = @()

function Traverse-DAG($nodeId, $depth = 0) {
    if ($visited[$nodeId]) { return }
    $visited[$nodeId] = $true
    $item = New-Object PSObject -Property @{ NodeId = $nodeId; Depth = $depth }
    $script:traversalOrder += $item
    
    Write-Host "Traversing node: $nodeId (depth: $depth)" -ForegroundColor Yellow
    
    # Add outgoing edges and their targets
    if ($outgoing[$nodeId]) {
        foreach ($edge in $outgoing[$nodeId]) {
            Write-Host "  Following edge: $($edge.id) -> $($edge.target)" -ForegroundColor Cyan
            $edgeItem = New-Object PSObject -Property @{ EdgeId = $edge.id; Depth = ($depth + 1) }
            $script:traversalOrder += $edgeItem
            if (-not $visited[$edge.target]) {
                Traverse-DAG $edge.target ($depth + 2)
            }
        }
    }
}

# Start traversal from root nodes
foreach ($rootNode in $rootNodes) {
    Traverse-DAG $rootNode
}

# Generate HTML based on traversal order
foreach ($item in $script:traversalOrder) {
    if ($item.NodeId) {
        $node = $nodes[$item.NodeId]
        if ($node) {
            $html += Get-NodeHTML $node
        }
    } elseif ($item.EdgeId) {
        $edge = $edges[$item.EdgeId]
        if ($edge) {
            $sourceNode = $nodes[$edge.source]
            $targetNode = $nodes[$edge.target]
            if ($sourceNode -and $targetNode) {
                $html += Get-EdgeHTML $edge $sourceNode $targetNode
            }
        }
    }
}

$html += @"
        <div class="summary-section">
            <h2>Research Overview</h2>
            <p style="font-size: 1.1em; margin: 20px 0;">
                This collection documents <strong>$($nodes.Count)</strong> points of interest in quantum gravity, spacetime engineering, and mathematical physics. The presentation follows DAG traversal order, showing nodes and their connecting edges in dependency sequence.
            </p>
        </div>

        <div class="footer">
            <p><strong>Data Sources:</strong></p>
            <p><strong>DAG Structure:</strong> highlights-dag.ndjson | 
               <strong>Documentation Index:</strong> documentation-index.ndjson | 
               <strong>Uncertainty Analysis:</strong> UQ-TODO.ndjson</p>
            <p style="margin-top: 20px;">
                <em>Generated automatically from research highlights database with DAG traversal</em>
            </p>
        </div>
    </div>
</body>
</html>
"@

# Write the HTML file
Set-Content -Path $OutputFile -Value $html -Encoding UTF8

Write-Host "Generated $OutputFile" -ForegroundColor Green
Write-Host "Presentation includes: $($nodes.Count) points of interest and $($edges.Count) research connections" -ForegroundColor Green
Write-Host "Traversal order: $($script:traversalOrder.Count) items" -ForegroundColor Green
Write-Host "Open the HTML file in a browser to view the presentation" -ForegroundColor Cyan
Write-Host "Script completed!" -ForegroundColor Green
