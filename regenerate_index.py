import json
import os
from datetime import datetime

def find_connected_nodes(node_id, edges):
    """Find nodes connected to the given node through edges"""
    connected = {'predecessors': [], 'successors': []}
    
    for edge in edges:
        if edge.get('source') == node_id:
            target = edge.get('target')
            if target:
                connected['successors'].append({
                    'id': target,
                    'relationship': edge.get('relationship', ''),
                    'description': edge.get('description', ''),
                    'mathematics': edge.get('mathematics', '')
                })
        elif edge.get('target') == node_id:
            source = edge.get('source')
            if source:
                connected['predecessors'].append({
                    'id': source,
                    'relationship': edge.get('relationship', ''),
                    'description': edge.get('description', ''),
                    'mathematics': edge.get('mathematics', '')
                })
    
    return connected

def escape_html(text):
    """Escape HTML special characters"""
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    return text

def escape_html_preserve_math(text):
    """Escape HTML special characters but preserve MathJax expressions"""
    import re
    text = str(text)
    
    # Find all inline math expressions ($...$) and display math expressions ($$...$$)
    # We'll replace them with placeholders, escape HTML, then restore them
    math_expressions = []
    placeholder_template = "MATHPLACEHOLDER{}"
    
    # Find display math first ($$...$$)
    display_math_pattern = r'\$\$([^$]+?)\$\$'
    def replace_display_math(match):
        math_expressions.append(f'$${match.group(1)}$$')
        return placeholder_template.format(len(math_expressions) - 1)
    text = re.sub(display_math_pattern, replace_display_math, text)
    
    # Find inline math ($...$) - be careful not to match $$ which we already handled
    inline_math_pattern = r'(?<!\$)\$([^$\n]+?)\$(?!\$)'
    def replace_inline_math(match):
        math_expressions.append(f'${match.group(1)}$')
        return placeholder_template.format(len(math_expressions) - 1)
    text = re.sub(inline_math_pattern, replace_inline_math, text)
    
    # Now escape HTML characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    # Restore math expressions
    for i, math_expr in enumerate(math_expressions):
        text = text.replace(placeholder_template.format(i), math_expr)
    
    return text

def create_github_link(source_file):
    """Convert source file path to GitHub link"""
    # Extract repository name and file path
    if '/' in source_file:
        parts = source_file.split('/')
        repo_name = parts[0]
        file_path = '/'.join(parts[1:])
        return f'https://github.com/arcticoder/{repo_name}/blob/main/{file_path}'
    return source_file

def create_internal_links(text, items):
    """Convert comma-separated items to internal links"""
    if not items:
        return text
    
    links = []
    for item in items:
        item = item.strip()
        if item:
            link = f'<a href="#{item}" style="color: #007bff; text-decoration: none;">{escape_html(item)}</a>'
            links.append(link)
    
    return ', '.join(links)

def escape_math(text):
    """Preserve math expressions but escape other HTML"""
    # Math expressions are already properly formatted for MathJax
    return text

# Load the highlights DAG data
discoveries = []
try:
    with open('highlights-dag.ndjson', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    discoveries.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping line {line_num} due to JSON error: {e}")
                    print(f"Problematic line: {line[:100]}...")
                    continue
except FileNotFoundError:
    print("Error: highlights-dag.ndjson not found")
    exit(1)

print(f'Found {len(discoveries)} discoveries in highlights-dag.ndjson')

# Separate nodes and edges
nodes = [d for d in discoveries if d.get('type') != 'edge']
edges = [d for d in discoveries if d.get('type') == 'edge']
print(f'Found {len(nodes)} discovery nodes and {len(edges)} edges')

# Create comprehensive HTML content
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
                processEnvironments: true,
                packages: {'[+]': ['ams', 'newcommand', 'configmacros']},
                macros: {
                    RR: "{\\bf R}",
                    bold: ["{\\bf #1}", 1]
                }
            },
            options: {
                ignoreHtmlClass: "tex2jax_ignore",
                processHtmlClass: "tex2jax_process"
            },
            startup: {
                ready: () => {
                    console.log('MathJax is loaded and ready');
                    MathJax.startup.defaultReady();
                }
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
      .discovery-description .MathJax {
        font-size: inherit !important;
      }
      .discovery-description .MathJax_Display {
        margin: 0.5em 0 !important;
      }
      .discovery-meta {
        background: #f8f9fa;
        padding: 10px 15px;
        border-radius: 6px;
        margin: 10px 0;
        font-size: 0.9em;
        color: #6c757d;
        border-left: 3px solid #6c757d;
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
      .source-files {
        margin-top: 10px;
        font-size: 0.85em;
        color: #6c757d;
      }
      .source-files a {
        color: #007bff;
        text-decoration: none;
      }
      .source-files a:hover {
        text-decoration: underline;
      }
      .predecessors, .successors {
        margin: 10px 0;
        padding: 10px;
        background: #f1f3f4;
        border-radius: 6px;
        font-size: 0.9em;
      }
      .predecessors {
        border-left: 3px solid #ffc107;
      }
      .successors {
        border-left: 3px solid #17a2b8;
      }
      .predecessors a:hover, .successors a:hover {
        text-decoration: underline;
        color: #0056b3;
      }
      .summary-section {
        margin: 50px 0;
        padding: 30px;
        background: #f8f9fa;
        border-radius: 12px;
      }
      .toc-item {
        margin: 8px 0;
        padding: 8px;
        background: white;
        border-radius: 6px;
        border-left: 3px solid #007bff;
      }
      .toc-link {
        text-decoration: none;
        color: #1a1a2e;
        font-weight: 500;
        display: block;
      }
      .toc-link:hover {
        color: #007bff;
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
            <p style="font-size: 1em; opacity: 0.8;">Generated from ''' + str(len(nodes)) + ''' discoveries spanning theoretical breakthroughs to practical implementation</p>
        </div>

        <!-- Table of Contents -->
        <div class="summary-section">
            <h2 style="text-align: center; color: #1a1a2e; margin-bottom: 30px;">Table of Contents</h2>
            <div style="column-count: 2; column-gap: 20px; column-rule: 1px solid #ddd;">'''

# Add table of contents
for i, discovery in enumerate(nodes, 1):
    discovery_title = escape_html(discovery.get('title', 'Untitled'))
    discovery_id = discovery.get('id', f'discovery_{i}')
    discovery_type = discovery.get('type', 'unknown').replace('_', ' ').title()
    
    html_content += f'''
                <div class="toc-item">
                    <a href="#{discovery_id}" class="toc-link">
                        {i}. {discovery_title}
                    </a>
                    <small style="color: #6c757d;">{discovery_type}</small>
                </div>'''

html_content += '''
            </div>
        </div>

        <div class="summary-section">
            <h2>Research Overview</h2>
            <p style="font-size: 1.1em; margin: 20px 0;">
                This collection documents <strong>''' + str(len(nodes)) + '''</strong> theoretical points of interest in quantum gravity, spacetime engineering, and mathematical physics. Each development builds upon previous work through a network of mathematical dependencies and theoretical constraints, presented in DAG traversal order showing the logical flow of research development.
            </p>
            <p style="margin: 15px 0;">
                <strong>Research Scope:</strong> From foundational quantum gravity mathematics through exotic matter engineering to practical warp drive implementation, representing a comprehensive framework for revolutionary physics and engineering.
            </p>
        </div>'''

# Add discoveries content
for i, discovery in enumerate(nodes, 1):
    discovery_id = discovery.get('id', f'discovery_{i}')
    discovery_title = escape_html(discovery.get('title', 'Untitled Discovery'))
    discovery_description = escape_html_preserve_math(discovery.get('description', 'No description available'))
    discovery_type = discovery.get('type', 'unknown').replace('_', ' ').title()
    discovery_date = discovery.get('date', 'Unknown date')
    discovery_impact = escape_html_preserve_math(discovery.get('impact', 'Impact assessment pending'))
    
    # Get connected nodes through edges
    connections = find_connected_nodes(discovery_id, edges)
    
    html_content += f'''
        <div class="discovery" id="{discovery_id}">
            <div class="discovery-title">{discovery_title}</div>
            <div class="discovery-meta">
                <strong>Type:</strong> {discovery_type}
            </div>
            <div class="discovery-description">{discovery_description}</div>'''
    
    # Add mathematics if present
    if 'mathematics' in discovery and discovery['mathematics']:
        math_content = escape_math(discovery['mathematics'])
        html_content += f'''
            <div class="mathematics">
                <strong>Mathematical Framework:</strong><br>
                $${math_content}$$
            </div>'''
    
    # Add code example if present
    if 'code_example' in discovery and discovery['code_example']:
        code_content = escape_html(discovery['code_example'])
        html_content += f'''
            <div class="mathematics">
                <strong>Code Example:</strong><br>
                <pre style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto;"><code>{code_content}</code></pre>
            </div>'''
    
    # Add glossary if present
    if 'glossary' in discovery and discovery['glossary']:
        html_content += '''
            <div class="mathematics">
                <strong>Glossary:</strong><br>
                <dl style="margin: 10px 0;">'''
        for term, definition in discovery['glossary'].items():
            term_escaped = escape_html(term)
            definition_escaped = escape_html(definition)
            html_content += f'''
                    <dt style="font-weight: bold; margin-top: 10px;">{term_escaped}</dt>
                    <dd style="margin-left: 20px; color: #666;">{definition_escaped}</dd>'''
        html_content += '''
                </dl>
            </div>'''
    
    # Add edge-based predecessors
    if connections['predecessors']:
        html_content += '''
            <div class="predecessors">
                <strong>Builds Upon:</strong><br>'''
        for pred in connections['predecessors']:
            relationship = escape_html(pred['relationship'])
            description = escape_html(pred['description'])
            pred_id = pred['id']
            html_content += f'''
                <div style="margin: 5px 0; padding: 8px; background: rgba(255, 193, 7, 0.1); border-radius: 4px;">
                    <a href="#{pred_id}" style="color: #007bff; text-decoration: none; font-weight: bold;">{escape_html(pred_id)}</a>
                    <span style="color: #6c757d; font-style: italic;"> {relationship}</span><br>
                    <small style="color: #666;">{description}</small>'''
            if pred['mathematics']:
                html_content += f'''<br><span style="font-family: monospace; font-size: 0.9em; color: #333;">${escape_math(pred['mathematics'])}$</span>'''
            html_content += '''
                </div>'''
        html_content += '''
            </div>'''
    
    # Add edge-based successors  
    if connections['successors']:
        html_content += '''
            <div class="successors">
                <strong>Enables:</strong><br>'''
        for succ in connections['successors']:
            relationship = escape_html(succ['relationship'])
            description = escape_html(succ['description'])
            succ_id = succ['id']
            html_content += f'''
                <div style="margin: 5px 0; padding: 8px; background: rgba(23, 162, 184, 0.1); border-radius: 4px;">
                    <a href="#{succ_id}" style="color: #007bff; text-decoration: none; font-weight: bold;">{escape_html(succ_id)}</a>
                    <span style="color: #6c757d; font-style: italic;"> {relationship}</span><br>
                    <small style="color: #666;">{description}</small>'''
            if succ['mathematics']:
                html_content += f'''<br><span style="font-family: monospace; font-size: 0.9em; color: #333;">${escape_math(succ['mathematics'])}$</span>'''
            html_content += '''
                </div>'''
        html_content += '''
            </div>'''
    
    # Fallback to legacy predecessors/successors if no edges found
    if not connections['predecessors'] and 'predecessors' in discovery and discovery['predecessors']:
        html_content += '''
            <div class="predecessors">
                <strong>Builds Upon:</strong> '''
        html_content += create_internal_links('', discovery['predecessors'])
        html_content += '''
            </div>'''
    
    if not connections['successors'] and 'successors' in discovery and discovery['successors']:
        html_content += '''
            <div class="successors">
                <strong>Enables:</strong> '''
        html_content += create_internal_links('', discovery['successors'])
        html_content += '''
            </div>'''
    
    # Add source files if present
    if 'source_files' in discovery and discovery['source_files']:
        html_content += '''
            <div class="source-files">
                <strong>Source Files:</strong> '''
        source_links = []
        for source_file in discovery['source_files']:
            github_url = create_github_link(source_file)
            source_links.append(f'<a href="{github_url}" target="_blank" style="color: #007bff; text-decoration: none;"><code>{escape_html(source_file)}</code></a>')
        html_content += ', '.join(source_links)
        html_content += '''
            </div>'''
    
    html_content += f'''
            <div class="impact">
                <strong>Impact:</strong> {discovery_impact}
            </div>
        </div>'''

html_content += '''
        <div class="footer">
            <p><strong>Data Sources:</strong></p>
            <p><strong>DAG Structure:</strong> highlights-dag.ndjson | 
               <strong>Documentation Index:</strong> documentation-index.ndjson | 
               <strong>Uncertainty Analysis:</strong> UQ-TODO.ndjson</p>
            <p style="margin-top: 20px;">
                <em>Generated automatically from research highlights database on ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</em>
            </p>
        </div>
    </div>

    <!-- Smooth scrolling script -->
    <script>
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>'''

# Write the updated HTML file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully updated index.html with {len(nodes)} discoveries')
print(f'Generated HTML file with {len(html_content)} characters')
print(f'Estimated {len(html_content.split("\\n"))} lines')
