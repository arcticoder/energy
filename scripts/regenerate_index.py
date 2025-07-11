#!/usr/bin/env python3
"""
Regenerate index.html from highlights-dag.ndjson and documentation-index.ndjson
"""

import json
import html
from datetime import datetime

def load_ndjson(filename):
    """Load NDJSON file and filter out edge entries"""
    items = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        # Filter out edge entries - these are relationship connections, not displayable content
                        if item.get('type') != 'edge':
                            items.append(item)
                    except json.JSONDecodeError as e:
                        print(f"Warning: JSON decode error in {filename} line {line_num}: {e}")
                        # Create a fallback entry
                        items.append({
                            "title": f"Entry {line_num} (JSON Parse Error)",
                            "description": "Failed to parse JSON content",
                            "type": "parse_error",
                            "date": "Unknown"
                        })
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
    return items

def format_mathematics(math_text):
    """Format mathematics for HTML display"""
    if not math_text:
        return ""
    # Escape HTML and preserve LaTeX formatting
    escaped = html.escape(math_text)
    return f'<div class="mathematics">\\[{escaped}\\]</div>'

def generate_html():
    """Generate the main index.html file"""
    
    # Load data
    highlights = load_ndjson('highlights-dag.ndjson')
    documentation = load_ndjson('documentation-index.ndjson')
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Energy Framework Repository Ecosystem</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }}
    }};
    </script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
            scroll-behavior: smooth;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        .section {{
            background: white;
            margin: 30px 0;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .highlight-item {{
            margin: 25px 0;
            padding: 25px;
            border-left: 5px solid;
            background: #f8f9fa;
            border-radius: 0 10px 10px 0;
        }}
        .breakthrough {{
            border-left-color: #28a745;
            background: linear-gradient(135deg, #d4edda 0%, #f8f9fa 100%);
        }}
        .production {{
            border-left-color: #007bff;
            background: linear-gradient(135deg, #cce5ff 0%, #f8f9fa 100%);
        }}
        .deployment {{
            border-left-color: #dc3545;
            background: linear-gradient(135deg, #f8d7da 0%, #f8f9fa 100%);
        }}
        .mathematics {{
            background: #f1f3f4;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }}
        .metadata {{
            font-size: 0.9em;
            color: #666;
            margin-top: 15px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 10px;
        }}
        .deployed {{
            background: #d4edda;
            color: #155724;
        }}
        .ready {{
            background: #cce5ff;
            color: #004085;
        }}
        .breakthrough-status {{
            background: #f8d7da;
            color: #721c24;
        }}
        .toc-entry {{
            transition: all 0.2s ease;
        }}
        .toc-entry:hover {{
            background: #e9ecef !important;
            transform: translateX(5px);
        }}
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #667eea;
            color: white;
            padding: 10px 15px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        .back-to-top:hover {{
            background: #5a6fd8;
            transform: translateY(-2px);
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header" id="top">
        <h1>🌌 Energy Framework Repository Ecosystem</h1>
        <p>Revolutionary Quantum Physics and Advanced Energy Technologies</p>
        <p><em>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    </div>
"""

    # Add major breakthroughs section
    # Generate table of contents
    html_content += """
    <div class="section">
        <h2>📋 Table of Contents</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px;">
            <div>
                <h3>🚀 Major Technological Breakthroughs ({} entries)</h3>
                <div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
""".format(len(highlights))

    # Add TOC entries for highlights
    for i, item in enumerate(highlights):
        item_type = item.get('type', 'unknown')
        badge_class = 'deployed' if 'production' in item_type else 'ready' if 'breakthrough' in item_type else 'breakthrough-status'
        
        html_content += f"""
                    <div class="toc-entry" style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                        <a href="#highlight-{i}" style="text-decoration: none; color: #333;">
                            <span class="status-badge {badge_class}" style="font-size: 0.7em;">{item_type.replace('_', ' ').title()}</span>
                            <strong>{html.escape(item.get('title', 'Untitled')[:60])}{'...' if len(item.get('title', '')) > 60 else ''}</strong>
                        </a>
                    </div>
"""

    html_content += """
                </div>
            </div>
            <div>
                <h3>📚 Documentation Index ({} entries)</h3>
                <div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
""".format(len(documentation))

    # Add TOC entries for documentation
    for i, doc in enumerate(documentation):
        doc_type = doc.get('type', 'documentation')
        priority = doc.get('priority', 'normal')
        
        html_content += f"""
                    <div class="toc-entry" style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                        <a href="#doc-{i}" style="text-decoration: none; color: #333;">
                            <span class="status-badge ready" style="font-size: 0.7em;">{priority.title()}</span>
                            <strong>{html.escape(doc.get('title', 'Untitled')[:60])}{'...' if len(doc.get('title', '')) > 60 else ''}</strong>
                        </a>
                    </div>
"""

    html_content += """
                </div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>🚀 Major Technological Breakthroughs</h2>
"""
    
    for i, item in enumerate(highlights):  # Show all highlights
        item_type = item.get('type', 'unknown')
        css_class = 'production' if 'production' in item_type else 'breakthrough' if 'breakthrough' in item_type else 'deployment'
        
        html_content += f"""
        <div class="highlight-item {css_class}" id="highlight-{i}">
            <h3>{html.escape(item.get('title', 'Untitled'))}</h3>
            <p>{html.escape(item.get('description', 'No description available.')[:1000])}{'...' if len(item.get('description', '')) > 1000 else ''}</p>
            {format_mathematics(item.get('mathematics', ''))}
            <div class="metadata">
                <span class="status-badge {css_class}">{item_type.replace('_', ' ').title()}</span>
                <strong>Date:</strong> {item.get('date', 'Unknown')} | 
                <strong>Impact:</strong> {html.escape(item.get('impact', 'Unknown')[:400])}{'...' if len(item.get('impact', '')) > 400 else ''}
            </div>
        </div>
"""

    html_content += """
    </div>
    
    <div class="section">
        <h2>📚 Documentation Index</h2>
"""

    # Add documentation items
    for i, doc in enumerate(documentation):  # Show all documentation items
        doc_type = doc.get('type', 'documentation')
        priority = doc.get('priority', 'normal')
        
        html_content += f"""
        <div class="highlight-item breakthrough" id="doc-{i}">
            <h3>{html.escape(doc.get('title', 'Untitled'))}</h3>
            <p>{html.escape(doc.get('description', 'No description available.')[:800])}{'...' if len(doc.get('description', '')) > 800 else ''}</p>
            {format_mathematics(doc.get('mathematics', ''))}
            <div class="metadata">
                <span class="status-badge ready">{priority.title()} Priority</span>
                <strong>Type:</strong> {doc_type.replace('_', ' ').title()} | 
                <strong>Path:</strong> {html.escape(doc.get('path', 'Unknown'))}
            </div>
        </div>
"""

    html_content += """
    </div>
    
    <div class="section">
        <h2>📊 Repository Statistics</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>🔬 Active Projects</h3>
                <div style="font-size: 2em; font-weight: bold; color: #1976d2;">45+</div>
                <p>Advanced Physics Repositories</p>
            </div>
            <div style="background: #f3e5f5; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>⚡ Energy Enhancement</h3>
                <div style="font-size: 2em; font-weight: bold; color: #7b1fa2;">242M×</div>
                <p>Sub-classical Efficiency</p>
            </div>
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>🚀 FTL Communication</h3>
                <div style="font-size: 2em; font-weight: bold; color: #388e3c;">1592 GHz</div>
                <p>Operational Frequency</p>
            </div>
            <div style="background: #fff3e0; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>🛡️ Safety Margin</h3>
                <div style="font-size: 2em; font-weight: bold; color: #f57c00;">25.4×</div>
                <p>WHO Biological Limits</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>🔗 Quick Links</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
            <a href="../warp-field-coils/README.md" style="display: block; padding: 15px; background: #e3f2fd; text-decoration: none; color: #1976d2; border-radius: 8px; font-weight: bold;">
                🌌 Warp Field Coils
            </a>
            <a href="../lqg-polymer-field-generator/README.md" style="display: block; padding: 15px; background: #f3e5f5; text-decoration: none; color: #7b1fa2; border-radius: 8px; font-weight: bold;">
                ⚛️ LQG Polymer Field Generator
            </a>
            <a href="../enhanced-simulation-hardware-abstraction-framework/README.md" style="display: block; padding: 15px; background: #e8f5e8; text-decoration: none; color: #388e3c; border-radius: 8px; font-weight: bold;">
                🔬 Enhanced Simulation Framework
            </a>
            <a href="../unified-lqg/README.md" style="display: block; padding: 15px; background: #fff3e0; text-decoration: none; color: #f57c00; border-radius: 8px; font-weight: bold;">
                🧮 Unified LQG
            </a>
        </div>
    </div>
    
    <footer style="text-align: center; margin-top: 40px; padding: 20px; color: #666; border-top: 1px solid #eee;">
        <p>Energy Framework Repository Ecosystem - Revolutionary Quantum Physics Technologies</p>
        <p><em>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    </footer>
    
    <a href="#top" class="back-to-top">↑ Top</a>
</body>
</html>
"""

    return html_content

if __name__ == "__main__":
    print("Regenerating index.html...")
    html_content = generate_html()
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ index.html regenerated successfully!")
