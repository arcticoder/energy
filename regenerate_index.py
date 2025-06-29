import json
import os
from datetime import datetime

# Load the highlights DAG data
with open('highlights-dag.ndjson', 'r') as f:
    discoveries = [json.loads(line) for line in f]

print(f'Found {len(discoveries)} discoveries in highlights-dag.ndjson')

# Create HTML content
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Highlights - Mathematical Physics & Quantum Gravity</title>
    
    <!-- MathJax Configuration -->
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
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
    <div class="container">
        <div class="header">
            <h1>Research Highlights</h1>
            <p>Mathematical Physics & Quantum Gravity Points of Interest</p>
        </div>

        <!-- Table of Contents -->
        <div class="summary-section">
            <h2 style="text-align: center; color: #1a1a2e; margin-bottom: 30px;">Table of Contents</h2>
            <ul style="list-style-type: none; padding: 0;">'''

# Add table of contents
toc_counter = 1
for discovery in discoveries:
    if discovery.get('type') != 'edge':  # Only include nodes, not edges
        html_content += f'''
                <li style="margin: 8px 0; padding: 8px; background: white; border-radius: 6px; border-left: 3px solid #007bff;">
                    <a href="#{discovery['id']}" style="text-decoration: none; color: #1a1a2e; font-weight: 500;">
                        {toc_counter}. {discovery['title']}
                    </a>
                </li>'''
        toc_counter += 1

html_content += '''
            </ul>
        </div>

        <div class="summary-section">
            <h2>Research Overview</h2>
            <p style="font-size: 1.1em; margin: 20px 0;">
                This collection documents <strong>''' + str(len([d for d in discoveries if d.get('type') != 'edge'])) + '''</strong> theoretical points of interest in quantum gravity, spacetime engineering, and mathematical physics. Each development builds upon previous work through a network of mathematical dependencies and theoretical constraints, presented in DAG traversal order showing the logical flow of research development.
            </p>
        </div>'''

# Add discoveries content
for discovery in discoveries:
    if discovery.get('type') == 'edge':  # Skip edges
        continue
        
    html_content += f'''
        <div class="discovery" id="{discovery['id']}">
            <div class="discovery-title">{discovery['title']}</div>
            <div class="discovery-description">{discovery['description']}</div>'''
    
    if 'mathematics' in discovery:
        html_content += f'''
            <div class="mathematics">
                <strong>Mathematical Framework:</strong><br>
                $${discovery['mathematics']}$$
            </div>'''
    
    html_content += f'''
            <div class="impact">
                <strong>Impact:</strong> {discovery['impact']}
            </div>
        </div>'''

html_content += '''
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
</html>'''

# Write the updated HTML file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully updated index.html with {len([d for d in discoveries if d.get("type") != "edge"])} discoveries')
