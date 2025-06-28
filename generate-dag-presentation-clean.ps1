param(
    [string]$InputFile = "highlights-dag.ndjson",
    [string]$OutputFile = "index.html"
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
    
    $baseUrl = "https://github.com/arcticoder"
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

# Implement cycle-aware traversal for potentially cyclic graphs
function Get-RobustTraversalOrder($nodes, $edges) {
    Write-Host "Building graph and checking for cycles..." -ForegroundColor Yellow
    
    # Build adjacency list from successors
    $adjacencyList = @{}
    $inDegree = @{}
    $visited = @{}
    $processed = @{}
    
    # Initialize
    foreach ($nodeId in $nodes.Keys) {
        $adjacencyList[$nodeId] = @()
        $inDegree[$nodeId] = 0
        $visited[$nodeId] = $false
        $processed[$nodeId] = $false
    }
    
    # Build graph from node successors
    foreach ($node in $nodes.Values) {
        if ($node.successors) {
            foreach ($successor in $node.successors) {
                if ($nodes.ContainsKey($successor)) {
                    $adjacencyList[$node.id] += $successor
                    $inDegree[$successor]++
                }
            }
        }
    }
    
    Write-Host "Graph built. In-degrees: $($inDegree.Values -join ', ')" -ForegroundColor Cyan
    
    # Cycle detection using DFS
    function Has-Cycle($nodeId, $recursionStack) {
        $visited[$nodeId] = $true
        $recursionStack[$nodeId] = $true
        
        foreach ($neighbor in $adjacencyList[$nodeId]) {
            if (-not $visited[$neighbor]) {
                if (Has-Cycle $neighbor $recursionStack) {
                    return $true
                }
            } elseif ($recursionStack[$neighbor]) {
                Write-Host "Cycle detected: $nodeId -> $neighbor" -ForegroundColor Red
                return $true
            }
        }
        
        $recursionStack[$nodeId] = $false
        return $false
    }
    
    # Check for cycles
    $hasCycles = $false
    $recursionStack = @{}
    foreach ($nodeId in $nodes.Keys) {
        $recursionStack[$nodeId] = $false
    }
    
    foreach ($nodeId in $nodes.Keys) {
        if (-not $visited[$nodeId]) {
            if (Has-Cycle $nodeId $recursionStack) {
                $hasCycles = $true
            }
        }
    }
    
    if ($hasCycles) {
        Write-Host "Graph contains cycles - using modified topological sort" -ForegroundColor Yellow
    } else {
        Write-Host "Graph is acyclic - using standard topological sort" -ForegroundColor Green
    }
    
    # Modified Kahn's algorithm that handles cycles
    $queue = @()
    $result = @()
    $currentInDegree = $inDegree.Clone()
    
    # Find all nodes with no incoming edges
    foreach ($nodeId in $currentInDegree.Keys) {
        if ($currentInDegree[$nodeId] -eq 0) {
            $queue += $nodeId
        }
    }
    
    # Process nodes
    $iterations = 0
    $maxIterations = $nodes.Count * 2  # Safety valve
    
    while ($queue.Count -gt 0 -and $iterations -lt $maxIterations) {
        $current = $queue[0]
        $queue = $queue[1..($queue.Count-1)]
        $result += $current
        
        # For each neighbor of current node
        foreach ($neighbor in $adjacencyList[$current]) {
            $currentInDegree[$neighbor]--
            if ($currentInDegree[$neighbor] -eq 0) {
                $queue += $neighbor
            }
        }
        $iterations++
    }
    
    # If we still have unprocessed nodes, add them in order of dependencies
    $remaining = $nodes.Keys | Where-Object { $_ -notin $result }
    if ($remaining.Count -gt 0) {
        Write-Host "Adding remaining nodes due to cycles: $($remaining -join ', ')" -ForegroundColor Yellow
        # Sort remaining by in-degree (fewer dependencies first)
        $remaining = $remaining | Sort-Object { $inDegree[$_] }
        $result += $remaining
    }
    
    Write-Host "Traversal order determined: $($result.Count) nodes" -ForegroundColor Green
    return $result
}

# Get traversal order
$traversalOrder = Get-RobustTraversalOrder $nodes $edges
Write-Host "DAG traversal order: $($traversalOrder.Count) nodes" -ForegroundColor Yellow

# Create traversal sequence mixing nodes and edges
$traversalSequence = @()
$processedNodes = @{}

for ($i = 0; $i -lt $traversalOrder.Count; $i++) {
    $currentNodeId = $traversalOrder[$i]
    
    # Only add node if not already processed
    if (-not $processedNodes.ContainsKey($currentNodeId)) {
        $traversalSequence += @{ type = "node"; id = $currentNodeId }
        $processedNodes[$currentNodeId] = $true
        
        # Add edges from this node to subsequent nodes in traversal order
        $currentNode = $nodes[$currentNodeId]
        if ($currentNode.successors) {
            foreach ($successorId in $currentNode.successors) {
                # Find the edge connecting current to successor
                $connectingEdge = $edges.Values | Where-Object { $_.source -eq $currentNodeId -and $_.target -eq $successorId }
                if ($connectingEdge) {
                    $traversalSequence += @{ type = "edge"; id = $connectingEdge.id }
                }
            }
        }
    }
}

Write-Host "Generated traversal sequence with $($traversalSequence.Count) items" -ForegroundColor Green

# Debug output
Write-Host "First 10 traversal items:" -ForegroundColor Cyan
for ($i = 0; $i -lt [Math]::Min(10, $traversalSequence.Count); $i++) {
    $item = $traversalSequence[$i]
    if ($item.type -eq "node") {
        Write-Host "  Node: $($nodes[$item.id].title)" -ForegroundColor Blue
    } else {
        $edge = $edges[$item.id]
        $sourceTitle = $nodes[$edge.source].title
        $targetTitle = $nodes[$edge.target].title
        Write-Host "  Edge: $sourceTitle -> $targetTitle" -ForegroundColor Green
    }
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
      }      .mathematics {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #007bff;
        overflow-x: auto;
        font-size: 1.1em;
        line-height: 1.4;
      }
      .mathematics .MathJax {
        font-size: 1.2em !important;
      }
      .MathJax_Display {
        font-size: 1.3em !important;
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
            <p>Mathematical Physics & Quantum Gravity Points of Interest</p>
        </div>        <!-- Table of Contents -->
        <div class="summary-section">
            <h2 style="text-align: center; color: #1a1a2e; margin-bottom: 30px;">Table of Contents</h2>
            <ul style="list-style-type: none; padding: 0;">
"@

# Add table of contents in traversal order
foreach ($item in $traversalSequence) {
    if ($item.type -eq "node") {
        $node = $nodes[$item.id]
        $anchorId = $node.id -replace "_", "-"
        $html += @"
                <li style="margin: 8px 0;"><a href="#node-$anchorId" style="color: #007bff; text-decoration: none;">$($node.title)</a></li>
"@
    } elseif ($item.type -eq "edge") {
        $edge = $edges[$item.id]
        $sourceNode = $nodes[$edge.source]
        $targetNode = $nodes[$edge.target]
        if ($sourceNode -and $targetNode) {
            $anchorId = $edge.id -replace "_", "-"
            $html += @"
                <li style="margin: 8px 0; margin-left: 20px; font-size: 0.9em;"><a href="#edge-$anchorId" style="color: #28a745; text-decoration: none;">&rarr; $($sourceNode.title) &rarr; $($targetNode.title)</a></li>
"@
        }
    }
}

$html += @"
            </ul>
        </div>

"@

# Generate content in traversal order
foreach ($item in $traversalSequence) {
    if ($item.type -eq "node") {
        $node = $nodes[$item.id]
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
        
        if ($node.code_example) {
            $codeExample = $node.code_example -replace "`n", "&#10;"
            $html += @"
            <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #28a745;">
                <strong>Code Example:</strong>
                <pre style="background: #ffffff; padding: 10px; border-radius: 4px; overflow-x: auto; margin: 10px 0 0 0; border: 1px solid #dee2e6;"><code>$codeExample</code></pre>
            </div>

"@
        }
        
        if ($node.glossary) {
            $glossaryHtml = "<ul style='margin: 5px 0; padding-left: 20px;'>"
            foreach ($term in $node.glossary.PSObject.Properties) {
                $glossaryHtml += "<li><strong>`$$($term.Name)`$</strong>: $($term.Value)</li>"
            }
            $glossaryHtml += "</ul>"
            $html += @"
            <div style="margin: 15px 0; padding: 15px; background: #f0f8ff; border-radius: 8px; border-left: 4px solid #007bff;">
                <strong>Glossary:</strong>
                $glossaryHtml
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
    } elseif ($item.type -eq "edge") {
        $edge = $edges[$item.id]
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
            <div class="discovery" id="edge-$anchorId" style="border-left: 5px solid #28a745;">
                <div class="discovery-title">$($sourceNode.title) &rarr; <a href="#node-$($targetNode.id -replace "_", "-")" style="color: #007bff; text-decoration: none;">$($targetNode.title)</a></div>
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
            
            # Use relationship_explanation if available, otherwise construct explanation
            $explanation = if ($edge.relationship_explanation) {
                $edge.relationship_explanation
            } else {
                "$($sourceNode.title) $relationshipText $($targetNode.title) because $($edge.description)."
            }
            
            $html += @"
                    <br><br>
                    <strong>How this connection works:</strong> $explanation
                </div>
            </div>

"@
        }
    }
}

# Add summary section
$html += @"
        <div class="summary-section">
            <h2>Research Overview</h2>
            <p style="font-size: 1.1em; margin: 20px 0;">
                This collection documents <strong>$($nodes.Count)</strong> theoretical points of interest in quantum gravity, spacetime engineering, and mathematical physics. Each development builds upon previous work through a network of mathematical dependencies and theoretical constraints, presented in DAG traversal order showing the logical flow of research development.
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

# Write the HTML file with proper UTF-8 encoding
[System.IO.File]::WriteAllText($OutputFile, $html, [System.Text.Encoding]::UTF8)

Write-Host "Generated $OutputFile" -ForegroundColor Green
Write-Host "Presentation includes: $($nodes.Count) points of interest and research connections" -ForegroundColor Yellow
Write-Host "Open index.html in a browser to view the presentation" -ForegroundColor Cyan
Write-Host "Script completed!" -ForegroundColor Green
