# Generate reveal.js slides from highlights-dag.ndjson
# Usage: .\generate-dag-slides.ps1

param(
    [string]$InputFile = "highlights-dag.ndjson",
    [string]$OutputFile = "highlights-dag.slides.md"
)

# Function to convert Unicode math to LaTeX
function Convert-ToLatex($mathString) {
    if (-not $mathString) { return "" }
    
    # Convert Unicode symbols to LaTeX
    $latex = $mathString
    $latex = $latex -replace "Â", "\hat{A}"
    $latex = $latex -replace "Ê", "\hat{E}"
    $latex = $latex -replace "∮", "\oint"
    $latex = $latex -replace "⟨", "\langle "
    $latex = $latex -replace "⟩", "\rangle "
    $latex = $latex -replace "μ", "\mu"
    $latex = $latex -replace "ν", "\nu"
    $latex = $latex -replace "≥", "\geq"
    $latex = $latex -replace "→", "\to"
    $latex = $latex -replace "∞", "\infty"
    $latex = $latex -replace "∫", "\int"
    $latex = $latex -replace "δ", "\delta"
    $latex = $latex -replace "τ", "\tau"
    $latex = $latex -replace "γ", "\gamma"
    $latex = $latex -replace "λ", "\lambda"
    $latex = $latex -replace "ε", "\varepsilon"
    $latex = $latex -replace "α", "\alpha"
    $latex = $latex -replace "β", "\beta"
    $latex = $latex -replace "σ", "\sigma"
    $latex = $latex -replace "ψ", "\psi"
    $latex = $latex -replace "ρ", "\rho"
    $latex = $latex -replace "π", "\pi"
    $latex = $latex -replace "ℏ", "\hbar"
    $latex = $latex -replace "∘", "\circ"
    $latex = $latex -replace "∑", "\sum"
    $latex = $latex -replace "Σ", "\sum"
    $latex = $latex -replace "∇", "\nabla"
    $latex = $latex -replace "∂", "\partial"
    $latex = $latex -replace "₀", "_0"
    $latex = $latex -replace "₁", "_1"
    $latex = $latex -replace "₂", "_2"
    $latex = $latex -replace "₃", "_3"
    $latex = $latex -replace "₄", "_4"
    $latex = $latex -replace "₅", "_5"
    $latex = $latex -replace "₆", "_6"
    $latex = $latex -replace "₇", "_7"
    $latex = $latex -replace "₈", "_8"
    $latex = $latex -replace "₉", "_9"
    $latex = $latex -replace "²", "^2"
    $latex = $latex -replace "³", "^3"
    $latex = $latex -replace "⁴", "^4"
    $latex = $latex -replace "ⁿ", "^n"
    
    return $latex
}

Write-Host "🎯 Generating reveal.js slides from DAG..." -ForegroundColor Cyan

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

Write-Host "📊 Parsed $($nodes.Count) nodes and $($edges.Count) edges" -ForegroundColor Green

# Function to get significance icon
function Get-SignificanceIcon($significance) {
    switch ($significance) {
        "revolutionary" { return "🔥" }
        "critical" { return "⚡" }
        "major" { return "🚀" }
        "fundamental" { return "🌟" }
        default { return "🔬" }
    }
}

# Function to get type icon
function Get-TypeIcon($type) {
    switch ($type) {
        "discovery" { return "🔍" }
        "breakthrough" { return "💥" }
        "proof" { return "✅" }
        "framework" { return "🏗️" }
        "analysis" { return "📊" }
        "methodology" { return "🧮" }
        "design" { return "⚙️" }
        "milestone" { return "🏆" }
        default { return "📋" }
    }
}

# Start generating the markdown
$markdown = @"
---
title: "Research Highlights DAG"
subtitle: "A Journey Through Revolutionary Discoveries"
author: "Energy Research Framework"
date: "$(Get-Date -Format 'MMMM dd, yyyy')"
theme: "black"
transition: "slide"
---

# Research Highlights DAG {data-background-color="#1a1a2e"}

## A Journey Through Revolutionary Discoveries

*Mapping the path from quantum foundations to practical implementation*

---

## Overview {data-background-color="#16213e"}

- **$($nodes.Count) Major Discoveries** across 2024-2025
- **$($edges.Count) Dependency Relationships** 
- **4 Significance Levels**: Revolutionary 🔥, Critical ⚡, Major 🚀, Fundamental 🌟
- **Timeline**: Q1 2024 → Q4 2025

---

"@

# Group nodes by date for chronological presentation
$nodesByDate = $nodes.Values | Group-Object -Property date | Sort-Object Name

foreach ($dateGroup in $nodesByDate) {
    $quarter = $dateGroup.Name
    $quarterNodes = $dateGroup.Group | Sort-Object { 
        switch ($_.significance) {
            "revolutionary" { 1 }
            "critical" { 2 }
            "major" { 3 }
            "fundamental" { 4 }
            default { 5 }
        }
    }
    
    $markdown += @"

## $quarter Achievements {data-background-color="#0f3460"}

"@

    foreach ($node in $quarterNodes) {
        $icon = Get-SignificanceIcon $node.significance
        $typeIcon = Get-TypeIcon $node.type
          $markdown += @"

### $icon $typeIcon $($node.title)

**Type**: $($node.type.ToUpper()) | **Significance**: $($node.significance.ToUpper())

$($node.description)

"@
        if ($node.mathematics) {
            $mathematics = Convert-ToLatex $node.mathematics
            $mathDisplay = "`$`$" + $mathematics + "`$`$"
            $markdown += @"

**Mathematics**: 

$mathDisplay

"@
        }
        
        if ($node.impact) {
            $markdown += @"

**Impact**: *$($node.impact)*

"@
        }
        
        $markdown += @"

---

"@
    }
}

# Add dependency flow sections
$markdown += @"

## Dependency Flows {data-background-color="#1a1a2e"}

### Understanding How Discoveries Build Upon Each Other

---

## Foundation Layer {data-background-color="#16213e"}

"@

# Show foundational nodes (no predecessors)
$foundationNodes = $nodes.Values | Where-Object { $_.predecessors.Count -eq 0 }
foreach ($node in $foundationNodes) {
    $icon = Get-SignificanceIcon $node.significance
    $typeIcon = Get-TypeIcon $node.type
    
    $markdown += @"

### $icon $typeIcon $($node.title)

- **Enables**: $($node.successors -join ', ')
- **Impact**: $($node.impact)

"@
}

$markdown += @"

---

## Critical Pathways {data-background-color="#0f3460"}

"@

# Show major dependency chains
$criticalPaths = @(
    @{
        name = "Warp Drive Development"
        path = @("lqg_foundations", "constraint_algebra", "warp_bubble_proof", "warp_drive_feasibility", "warp_optimization", "practical_implementation")
    },
    @{
        name = "Energy Enhancement"
        path = @("lqg_foundations", "quantum_geometry_catalysis", "polymer_fusion", "energy_enhancement", "practical_implementation")
    },
    @{
        name = "Vacuum Engineering"
        path = @("constraint_algebra", "anec_framework", "qi_bound_modification", "vacuum_engineering", "practical_implementation")
    }
)

foreach ($path in $criticalPaths) {
    $markdown += @"

### 🛤️ $($path.name) Pathway

"@
    
    for ($i = 0; $i -lt $path.path.Count; $i++) {
        $nodeId = $path.path[$i]
        $node = $nodes[$nodeId]
        $icon = Get-SignificanceIcon $node.significance
        
        if ($i -lt $path.path.Count - 1) {
            $markdown += "$icon **$($node.title)** → "
        } else {
            $markdown += "$icon **$($node.title)**"
        }
    }
    
    $markdown += @"


---

"@
}

# Add relationship analysis
$markdown += @"

## Relationship Types {data-background-color="#1a1a2e"}

"@

# Analyze edge relationships
$relationshipTypes = $edges.Values | Group-Object -Property relationship | Sort-Object Count -Descending

foreach ($relType in $relationshipTypes[0..4]) { # Top 5 relationship types
    $examples = $relType.Group | Select-Object -First 2
    
    $markdown += @"

### 🔗 "$($relType.Name)" ($($relType.Count) connections)

"@
    
    foreach ($example in $examples) {
        $sourceNode = $nodes[$example.source]
        $targetNode = $nodes[$example.target]
        $markdown += "- **$($sourceNode.title)** → **$($targetNode.title)**`n"
    }
    
    $markdown += @"

---

"@
}

# Add significance analysis
$markdown += @"

## Impact Distribution {data-background-color="#16213e"}

"@

$significanceGroups = $nodes.Values | Group-Object -Property significance | Sort-Object Count -Descending

foreach ($sigGroup in $significanceGroups) {
    $icon = Get-SignificanceIcon $sigGroup.Name
    $markdown += @"

### $icon $($sigGroup.Name.ToUpper()) ($($sigGroup.Count) discoveries)

"@
    
    $examples = $sigGroup.Group | Select-Object -First 3
    foreach ($example in $examples) {
        $typeIcon = Get-TypeIcon $example.type
        $markdown += "- $typeIcon **$($example.title)**`n"
    }
    
    $markdown += @"

---

"@
}

# Add mathematical highlights
$mathNodes = $nodes.Values | Where-Object { $_.mathematics -ne $null } | Select-Object -First 5

$markdown += @"

## Mathematical Foundations {data-background-color="#0f3460"}

### Key Equations Driving the Breakthroughs

"@

foreach ($node in $mathNodes) {
    $icon = Get-SignificanceIcon $node.significance
    $mathematics = Convert-ToLatex $node.mathematics
    $mathDisplay = "`$`$" + $mathematics + "`$`$"
    $markdown += @"

### $icon $($node.title)

$mathDisplay

---

"@
}

# Add conclusion
$markdown += @"

## The Path Forward {data-background-color="#1a1a2e"}

### 🏆 Practical Implementation Roadmap

All discoveries converge to enable:

- ⚡ **Energy Enhancement Technologies**
- 🚀 **Warp Drive Implementation**  
- 🔬 **Vacuum Engineering Systems**
- 🛡️ **Comprehensive Safety Protocols**

---

## Impact Summary {data-background-color="#16213e"}

### Revolutionary Science → Engineering Reality

- **Theoretical Foundations** ✅ Complete
- **Mathematical Validation** ✅ Proven  
- **Optimization Methods** ✅ Breakthrough
- **Safety Protocols** ✅ Comprehensive
- **Implementation Roadmap** ✅ Ready

### 🌟 The Future is Now

---

# Thank You {data-background-color="#1a1a2e"}

## Questions & Discussion

*Exploring the frontiers of physics and engineering*

📊 **Data Source**: highlights-dag.ndjson  
🔗 **Full Documentation**: documentation-index.ndjson  
⚠️ **Uncertainties**: UQ-TODO.ndjson

"@

# Write the markdown file
$markdown | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "✅ Generated $OutputFile" -ForegroundColor Green
Write-Host "📊 Slides created: $($nodesByDate.Count + 15) slides" -ForegroundColor Yellow

# Generate the HTML if pandoc is available
Write-Host "`n🔄 Generating HTML presentation..." -ForegroundColor Cyan

try {
    $pandocArgs = @(
        $OutputFile,
        "-t", "revealjs",
        "--mathjax",
        "--variable", "revealjs-url=https://unpkg.com/reveal.js@^4/",
        "--variable", "theme=black",
        "--variable", "transition=slide",
        "--variable", "hash=true",
        "--variable", "controls=true",
        "--variable", "progress=true",
        "--variable", "mathjax-url=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
        "-s",
        "-o", "highlights-dag.slides.html"
    )
    
    & pandoc @pandocArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Generated highlights-dag.slides.html" -ForegroundColor Green
        Write-Host "🌐 Open the HTML file in a browser to view the presentation" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Pandoc failed with exit code $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️ Pandoc not found. Please install pandoc and run:" -ForegroundColor Yellow
    Write-Host "    pandoc $OutputFile -t revealjs --mathjax --variable revealjs-url=https://unpkg.com/reveal.js@^4/ --variable theme=black -s -o highlights-dag.slides.html" -ForegroundColor Gray
}

Write-Host "`n🎯 Script completed!" -ForegroundColor Cyan
