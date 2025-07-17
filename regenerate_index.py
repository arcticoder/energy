import json
import html

# Read highlights DAG data
with open('highlights-dag.ndjson', 'r', encoding='utf-8') as f:
    highlights = [json.loads(line) for line in f if line.strip()]

# Generate HTML content
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LQG Energy Research Highlights</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .highlight { background: white; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .highlight h2 { color: #2c3e50; margin-top: 0; }
        .breakthrough_complete { border-left: 5px solid #e74c3c; }
        .revolutionary_breakthrough_complete { border-left: 5px solid #27ae60; }
        .production_breakthrough { border-left: 5px solid #3498db; }
        .medical_breakthrough_complete { border-left: 5px solid #9b59b6; }
        .revolutionary_production_deployment { border-left: 5px solid #f39c12; }
        .technological_breakthrough { border-left: 5px solid #34495e; }
        .physics_breakthrough { border-left: 5px solid #1abc9c; }
        .revolutionary_deployment { border-left: 5px solid #e67e22; }
        .theoretical_framework { border-left: 5px solid #95a5a6; }
        .meta { color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px; }
        .mathematics { background: #ecf0f1; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 0.9em; margin: 15px 0; overflow-x: auto; }
        .impact { background: #e8f5e8; padding: 15px; border-radius: 4px; margin: 15px 0; }
        .files { background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0; font-size: 0.85em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>LQG Energy Research Highlights - Revolutionary Achievements</h1>
        <p><strong>Last Updated:</strong> ''' + str(len(highlights)) + ''' breakthrough achievements documented</p>
'''

# Sort highlights by date (newest first)
sorted_highlights = sorted(highlights, key=lambda x: x.get('date', '2024'), reverse=True)

# Generate content for each highlight
for highlight in sorted_highlights:
    html_content += f'''
        <div class="highlight {highlight.get('type', 'breakthrough')}">
            <h2>{html.escape(highlight['title'])}</h2>
            <div class="meta">
                <strong>Type:</strong> {html.escape(highlight.get('type', 'N/A').replace('_', ' ').title())} | 
                <strong>Date:</strong> {html.escape(highlight.get('date', 'N/A'))}
            </div>
            <p>{html.escape(highlight['description'])}</p>
            
            {f'<div class="mathematics"><strong>Mathematics:</strong><br>{html.escape(highlight["mathematics"])}</div>' if highlight.get('mathematics') else ''}
            
            {f'<div class="impact"><strong>Impact:</strong><br>{html.escape(highlight["impact"])}</div>' if highlight.get('impact') else ''}
            
            {f'<div class="files"><strong>Source Files:</strong><br>{", ".join(highlight["source_files"])}</div>' if highlight.get('source_files') else ''}
        </div>
    '''

html_content += '''
    </div>
</body>
</html>'''

# Write HTML file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully generated index.html with', len(highlights), 'highlights including LQG Fusion Reactor Integration')
