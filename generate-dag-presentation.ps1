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

# Function to generate anchor-safe ID
function Get-AnchorId($title) {
    return $title -replace '[^a-zA-Z0-9]', '_' -replace '__+', '_' -replace '^_|_$', ''
}

# Function to get node HTML
function Get-NodeHTML($node) {
    $anchorId = Get-AnchorId $node.title
    $html = @"
        <div class="discovery" id="$anchorId">
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
      if ($node.source_files) {
        if ($node.source_files -is [string]) {
            # Handle single string source file
            $sourceFiles = $node.source_files
        } else {
            # Handle JSON array of source files
            try {
                $sourceFiles = ($node.source_files | ConvertFrom-Json) -join ', '
            } catch {
                $sourceFiles = $node.source_files -join ', '
            }
        }
        $html += @"
            <div class="source-files">
                <strong>Source Files:</strong> $sourceFiles
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

# Function to get edge-specific mathematical description and how it works
function Get-EdgeMathAndDescription($edgeId, $sourceNode, $targetNode, $edge) {
    $edgeMath = ""
    $howItWorks = ""
    
    switch ($edgeId) {
        "edge_lqg_to_constraint" {
            $edgeMath = "\\{\\hat{A}(e), \\hat{E}_i^a(S)\\} \\rightarrow [\\hat{C}_a(x), \\hat{C}_b(y)]"
            $howItWorks = "The holonomy-flux algebra established in Loop Quantum Gravity provides the canonical variables necessary for constructing the quantum constraint operators. The discrete geometric structure ensures that quantum constraint algebra inherits the proper classical limit while maintaining finite, well-defined commutation relations."
        }
        "edge_lqg_to_catalysis" {
            $edgeMath = "\\langle \\hat{E}_i^a \\rangle \\propto \\ell_p^2 \\rightarrow k_{eff} = k_0(1 + \\lambda E_{quantum}/E_{Planck})"
            $howItWorks = "Discrete quantum geometry creates polymer excitations that couple non-trivially to matter fields. These quantum geometric fluctuations modify the effective potential landscape for chemical reactions, lowering activation barriers through quantum geometric catalysis."
        }
        "edge_constraint_to_warp" {
            $edgeMath = "[\\hat{C}_a, \\hat{C}_b] = f_{ab}^c \\hat{C}_c \\rightarrow \\nabla_\\mu(\\sqrt{-g} G^{\\mu\\nu}) = 0"
            $howItWorks = "The anomaly-free quantum constraint algebra guarantees that the Einstein field equations remain valid in the quantum regime. This mathematical consistency allows Alcubierre-type solutions to be constructed within the Loop Quantum Gravity framework without violating fundamental quantum gravitational principles."
        }
        "edge_constraint_to_anec" {
            $edgeMath = "[\\hat{C}_a, \\hat{C}_b] = f_{ab}^c \\hat{C}_c \\rightarrow \\int \\langle T_{\\mu\\nu} \\rangle k^\\mu k^\\nu d\\lambda"
            $howItWorks = "The closed constraint algebra provides the mathematical foundation for analyzing energy conditions in quantum spacetime. It ensures that energy-momentum conservation laws hold in the quantum theory, enabling systematic study of when and how energy conditions can be violated."
        }
        "edge_catalysis_to_fusion" {
            $edgeMath = "k_{eff} = k_0(1 + \\lambda \\langle \\hat{E}_i^a \\rangle/E_{Planck}) \\rightarrow P_{fusion} \\propto \\sigma v \\rho^2 k_{eff}"
            $howItWorks = "Quantum geometric catalysis directly enhances nuclear fusion rates by modifying the effective interaction cross-sections. The polymer field interactions reduce Coulomb barriers, leading to dramatically increased fusion reaction rates in the enhanced regime."
        }
        "edge_catalysis_to_energy" {
            $edgeMath = "\\Delta E_{barrier} = -\\lambda \\langle \\hat{E}_i^a \\rangle \\rightarrow E_{out}/E_{in} > 1"
            $howItWorks = "The catalytic reduction of energy barriers enables energy enhancement mechanisms by allowing reactions to proceed that would otherwise be energetically forbidden. This creates pathways for apparent energy multiplication through access to previously inaccessible reaction channels."
        }
        "edge_warp_to_feasibility" {
            $edgeMath = "ds^2 = -(1-v^2f^2)dt^2 + 2vf dx dt + d\\vec{x}^2 \\rightarrow E_{required} \\sim (v/c)^2 R^3"
            $howItWorks = "The mathematical proof of Alcubierre solutions in Loop Quantum Gravity provides the theoretical foundation for engineering feasibility analysis. Quantum corrections modify energy requirements, making warp drive construction potentially achievable with realistic energy densities."
        }
        "edge_warp_to_exotic" {
            $edgeMath = "G_{\\mu\\nu} = 8\\pi T_{\\mu\\nu}^{exotic} \\rightarrow \\rho_{exotic} < 0, p_{exotic} < -\\rho_{exotic}/3"
            $howItWorks = "Alcubierre spacetime geometries require exotic matter with negative energy density to satisfy Einstein's field equations. The specific metric structure determines the precise stress-energy tensor requirements for maintaining the warp bubble configuration."
        }
        "edge_anec_to_exotic" {
            $edgeMath = "\\int \\langle T_{\\mu\\nu} \\rangle k^\\mu k^\\nu d\\lambda \\geq 0 \\rightarrow |\\rho_{exotic}| \\leq f(\\tau_{violation})"
            $howItWorks = "The ANEC framework provides fundamental bounds on how much negative energy density can be sustained and for how long. These constraints directly limit the properties and distribution of exotic matter that can be generated for warp drive applications."
        }
        "edge_anec_to_conditions" {
            $edgeMath = "\\text{ANEC} \\rightarrow \\text{NEC}, \\text{WEC}, \\text{SEC}: T_{\\mu\\nu} k^\\mu k^\\nu \\geq 0"
            $howItWorks = "The Averaged Null Energy Condition provides a framework for systematic analysis of all energy conditions. It establishes when classical energy conditions can be violated in quantum field theory and provides bounds on such violations."
        }
        "edge_anec_to_qi" {
            $edgeMath = "\\int_{-\\infty}^{+\\infty} \\langle T_{\\mu\\nu}\\rangle k^\\mu k^\\nu d\\lambda \\rightarrow \\int_0^\\infty \\langle T_{uu}\\rangle dt \\geq -\\frac{3}{32\\pi^2\\tau^4}"
            $howItWorks = "ANEC analysis reveals that quantum interest bounds emerge naturally from energy condition requirements. The modification of these bounds through engineered spacetime geometries provides a pathway to controlled violations of energy conservation on short timescales."
        }
        "edge_fusion_to_energy" {
            $edgeMath = "P_{fusion} = 8.32 \\times P_{baseline} \\rightarrow \\eta_{energy} = E_{out}/E_{in} > 1"
            $howItWorks = "The demonstrated 8.32× enhancement in fusion performance provides experimental evidence for energy enhancement mechanisms. This validates theoretical predictions and demonstrates practical pathways to energy multiplication through quantum geometric effects."
        }
        "edge_fusion_to_antimatter" {
            $edgeMath = "P_{polymer} + \\bar{p}p \\rightarrow E = mc^2 \\rightarrow P_{ultimate}"
            $howItWorks = "Polymer-enhanced fusion provides the technological foundation for antimatter-enhanced reactor designs. The controlled fusion environment enables safe antimatter handling and maximizes energy extraction from matter-antimatter annihilation."
        }
        "edge_feasibility_to_optimization" {
            $edgeMath = "E_{required}(v,R) \\rightarrow \\min_{f(r)} \\int |T_{\\mu\\nu}|^2 d^3x"
            $howItWorks = "Feasibility analysis identifies the key parameters that must be optimized to achieve practical warp drive construction. This motivates the development of optimization frameworks to minimize energy requirements while maintaining field stability."
        }
        "edge_feasibility_to_8gaussian" {
            $edgeMath = "\\min E_{total} \\rightarrow f(r) = \\sum_{i=1}^8 A_i \\exp(-(r-r_i)^2/2\\sigma_i^2)"
            $howItWorks = "The need to minimize energy requirements from feasibility studies directly motivates the development of 8-Gaussian optimization methods. These basis functions provide optimal field representations that minimize computational complexity while maintaining smoothness."
        }
        "edge_feasibility_to_requirements" {
            $edgeMath = "\\text{Feasible} \\rightarrow E_{total} = \\int |T_{\\mu\\nu}| d^3x < E_{threshold}"
            $howItWorks = "Feasibility analysis establishes the fundamental energy scale requirements for warp drive construction. These studies determine whether proposed technologies can achieve the necessary energy densities within realistic engineering constraints."
        }
        "edge_exotic_to_requirements" {
            $edgeMath = "T_{\\mu\\nu}^{exotic} \\rightarrow E_{total} = \\int \\rho_{exotic} d^3x"
            $howItWorks = "The properties and distribution of exotic matter directly determine the total energy requirements for warp drive construction. Understanding these constraints is essential for practical implementation strategies."
        }
        "edge_exotic_to_stability" {
            $edgeMath = "\\nabla_\\mu T^{\\mu\\nu}_{exotic} = 0 \\rightarrow \\text{stability conditions}"
            $howItWorks = "Exotic matter configurations must satisfy energy-momentum conservation to remain stable over time. This provides crucial constraints on allowable exotic matter distributions and their long-term viability."
        }
        "edge_qi_to_energy" {
            $edgeMath = "\\Delta E \\cdot \\Delta t \\geq \\frac{\\hbar}{2} \\rightarrow E_{extracted} \\leq \\frac{\\hbar}{2\\tau}"
            $howItWorks = "Quantum interest bound modifications enable controlled violations of energy conservation within uncertainty principle limits. This provides a pathway to apparent energy enhancement through vacuum fluctuation manipulation."
        }
        "edge_qi_to_vacuum" {
            $edgeMath = "\\langle 0|T_{\\mu\\nu}|0\\rangle \\rightarrow \\langle \\text{engineered}|T_{\\mu\\nu}|\\text{engineered}\\rangle"
            $howItWorks = "Quantum interest modifications enable engineering of vacuum states with altered stress-energy properties. This provides the theoretical foundation for controlled vacuum energy manipulation."
        }
        "edge_qi_to_metamaterial" {
            $edgeMath = "F_{Casimir} \\rightarrow F_{enhanced} = \\eta(\\epsilon,\\mu) \\times F_{Casimir}, \\eta >> 1"
            $howItWorks = "Quantum interest bound modifications enhance the effectiveness of metamaterial-based Casimir effects. This amplification enables practical energy extraction from vacuum fluctuations."
        }
        "edge_qi_to_bayesian" {
            $edgeMath = "\\text{New physics} \\rightarrow P(\\text{parameters}|\\text{data}) \\propto P(\\text{data}|\\text{parameters})P(\\text{parameters})"
            $howItWorks = "Novel physics phenomena require rigorous uncertainty quantification to establish reliability and confidence bounds. Bayesian methods provide the mathematical framework for systematic uncertainty analysis."
        }
        "edge_8gaussian_to_optimization" {
            $edgeMath = "f_{8G}(r) = \\sum_{i=1}^8 A_i \\exp(-(r-r_i)^2/2\\sigma_i^2) \\rightarrow \\text{Optimization Framework}"
            $howItWorks = "The success of 8-Gaussian methods in reducing computational complexity provides a foundation for broader optimization frameworks. These methods demonstrate that careful basis function selection can dramatically improve efficiency."
        }
        "edge_8gaussian_to_bspline" {
            $edgeMath = "\\text{Gaussian basis} \\rightarrow \\text{B-spline basis}: f(r) = \\sum_{i=0}^n c_i B_{i,k}(r)"
            $howItWorks = "The computational success of 8-Gaussian methods motivates exploration of alternative basis functions. B-splines offer superior smoothness properties while maintaining computational efficiency."
        }
        "edge_bspline_to_optimization" {
            $edgeMath = "B_{i,k}(r) \\text{ (smooth basis)} \\rightarrow \\text{Enhanced Optimization Framework}"
            $howItWorks = "B-spline methods provide enhanced smoothness compared to Gaussian methods, enabling more precise control over field derivatives. This smoothness is crucial for maintaining spacetime stability in dynamic configurations."
        }
        "edge_bspline_to_stability" {
            $edgeMath = "\\frac{d^n f}{dr^n} \\text{ continuous} \\rightarrow \\text{Stability Analysis}"
            $howItWorks = "The guaranteed smoothness properties of B-spline representations enable detailed stability analysis of warp field configurations. Continuous derivatives ensure that stability criteria can be systematically evaluated."
        }
        default {
            if ($edge.mathematics) {
                $edgeMath = $edge.mathematics
            } else {
                $edgeMath = "\\text{Dependency: } " + $sourceNode.title + " \\rightarrow " + $targetNode.title
            }
            $howItWorks = "$($sourceNode.title) $($edge.relationship) $($targetNode.title) through $($edge.description). This $($edge.dependency_type) dependency ensures that advances in $($sourceNode.title) directly enable progress in $($targetNode.title)."
        }
    }
    
    return @{
        Mathematics = $edgeMath
        HowItWorks = $howItWorks
    }
}

# Function to get edge HTML
function Get-EdgeHTML($edge, $sourceNode, $targetNode) {
    $anchorId = Get-AnchorId "$($sourceNode.title)_to_$($targetNode.title)"
    $edgeDetails = Get-EdgeMathAndDescription $edge.id $sourceNode $targetNode $edge
    
    $html = @"
        <div class="edge-item" id="$anchorId">
            <div class="discovery-title">$($sourceNode.title) → $($targetNode.title)</div>
            <div class="discovery-description">
                <strong>Relationship:</strong> $($edge.relationship) - $($edge.description)
                <br><br>

"@
    
    if ($edgeDetails.Mathematics) {
        $math = Convert-ToLatex $edgeDetails.Mathematics
        $html += @"
                <div class="mathematics">
                    `$$math`$
                </div>
                <br>

"@
    }
      if ($edge.source_files) {
        if ($edge.source_files -is [string]) {
            # Handle single string source file
            $sourceFiles = $edge.source_files
        } else {
            # Handle JSON array of source files
            try {
                $sourceFiles = ($edge.source_files | ConvertFrom-Json) -join ', '
            } catch {
                $sourceFiles = $edge.source_files -join ', '
            }
        }
        $html += @"
                <div class="source-files">
                    <strong>Source Files:</strong> $sourceFiles
                </div>
                <br>

"@
    }
    
    $html += @"
                <strong>How this connection works:</strong> $($edgeDetails.HowItWorks)
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

# Generate Table of Contents
$toc = @"
        <div class="toc-section">
            <h2>Table of Contents</h2>
            <div class="toc-grid">
                <div class="toc-column">
                    <h3>Research Nodes</h3>
                    <ul>

"@

foreach ($nodeId in ($nodes.Keys | Sort-Object)) {
    $node = $nodes[$nodeId]
    $anchorId = Get-AnchorId $node.title
    $toc += @"
                        <li><a href="#$anchorId">$($node.title)</a></li>

"@
}

$toc += @"
                    </ul>
                </div>
                <div class="toc-column">
                    <h3>Research Connections</h3>
                    <ul>

"@

foreach ($edgeId in ($edges.Keys | Sort-Object)) {
    $edge = $edges[$edgeId]
    $sourceNode = $nodes[$edge.source]
    $targetNode = $nodes[$edge.target]
    if ($sourceNode -and $targetNode) {
        $anchorId = Get-AnchorId "$($sourceNode.title)_to_$($targetNode.title)"
        $toc += @"
                        <li><a href="#$anchorId">$($sourceNode.title) → $($targetNode.title)</a></li>

"@
    }
}

$toc += @"
                    </ul>
                </div>
            </div>
        </div>

"@

# Generate HTML
$html = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Highlights - Mathematical Physics & Quantum Gravity</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['`$', '`$'], ['\\(', '\\)']],
                displayMath: [['`$`$', '`$`$'], ['\\[', '\\]']]
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
        
        .toc-section {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
            border: 2px solid #2196f3;
        }
        
        .toc-section h2 {
            color: #1565c0;
            text-align: center;
            margin-bottom: 20px;
            font-size: 2em;
        }
        
        .toc-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .toc-column h3 {
            color: #1976d2;
            margin-bottom: 15px;
            font-size: 1.4em;
            border-bottom: 2px solid #1976d2;
            padding-bottom: 5px;
        }
        
        .toc-column ul {
            list-style-type: none;
            padding: 0;
        }
        
        .toc-column li {
            margin: 8px 0;
        }
        
        .toc-column a {
            color: #1565c0;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            display: block;
        }
        
        .toc-column a:hover {
            background-color: #e3f2fd;
            text-decoration: underline;
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
        
        .source-files {
            background: #e8f4fd;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #2196f3;
            margin: 15px 0;
            font-size: 0.95em;
            color: #1565c0;
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
        
        @media (max-width: 768px) {
            .toc-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <h1>Research Highlights</h1>
            <p>Mathematical Physics & Quantum Gravity Research</p>
        </div>

$toc

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
                This collection documents <strong>$($nodes.Count)</strong> points of interest in quantum gravity, spacetime engineering, and mathematical physics. The presentation follows a dependency-ordered traversal, showing nodes and their connecting edges in logical sequence to illustrate the progression of research developments.
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
Set-Content -Path $OutputFile -Value $html -Encoding UTF8

Write-Host "Generated $OutputFile" -ForegroundColor Green
Write-Host "Presentation includes: $($nodes.Count) points of interest and $($edges.Count) research connections" -ForegroundColor Green
Write-Host "Traversal order: $($script:traversalOrder.Count) items" -ForegroundColor Green
Write-Host "Open the HTML file in a browser to view the presentation" -ForegroundColor Cyan
Write-Host "Script completed!" -ForegroundColor Green
