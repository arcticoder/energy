import re
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY")
GROUP_ID = os.getenv("GROUP_ID")

# Mapping from citation key to (Parent Item Key, Note Item Key)
MAPPING = {
    "jacobson1995": {"parent": "7NGTW7FM", "note": "3FRUVEA8", "version": 294},
    "birrell2012": {"parent": "R85HTGW3", "note": "XA9FKMY9", "version": 290}
}

SOURCE_FILE = "/home/echo_/Code/asciimath/coherence-gravity-coupling/papers/coherence_gravity_coupling-bib-annotations.md"

def parse_markdown_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by "### " (citation keys)
    sections = re.split(r'^###\s+', content, flags=re.MULTILINE)
    parsed = {}
    for section in sections:
        if not section.strip():
            continue
        lines = section.split('\n', 1)
        # keys are like "verlinde2011: Title"
        key_part = lines[0].strip()
        if ':' in key_part:
            key = key_part.split(':')[0].strip()
        else:
            key = key_part.strip()
            
        body = lines[1].strip() if len(lines) > 1 else ""
        parsed[key] = body
    return parsed

def convert_to_zotero_html(markdown_text):
    # 1. Protect Math Blocks
    math_display = []
    def protect_display_math(match):
        math_display.append(match.group(1))
        return f"__MATH_DISPLAY_{len(math_display)-1}__"
    
    text = re.sub(r'\$\$(.+?)\$\$', protect_display_math, markdown_text, flags=re.DOTALL)
    
    math_inline = []
    def protect_inline_math(match):
        math_inline.append(match.group(1))
        return f"__MATH_INLINE_{len(math_inline)-1}__"
    
    text = re.sub(r'\$(.+?)\$', protect_inline_math, text)
    
    # 2. Escape HTML (basic)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # 3. Markdown Conversions
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Lists
    lines = text.split('\n')
    new_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('* ') or stripped.startswith('- '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            content = stripped[2:]
            new_lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            
            if stripped:
                new_lines.append(f'<p>{stripped}</p>')
            else:
                pass 
    
    if in_list:
        new_lines.append('</ul>')
        
    html = '\n'.join(new_lines)
    
    # 4. Restore Math
    for i, m in enumerate(math_display):
        replacement = f'<pre class="math">$${m}$$</pre>'
        html = html.replace(f"__MATH_DISPLAY_{i}__", replacement)
        
    for i, m in enumerate(math_inline):
        replacement = f'<span class="math">${m}$</span>'
        html = html.replace(f"__MATH_INLINE_{i}__", replacement)
        
    return html

def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: {SOURCE_FILE} not found")
        return

    data = parse_markdown_file(SOURCE_FILE)
    print(f"DEBUG: Keys found in markdown: {list(data.keys())}")
    
    commands = []
    
    for key, config in MAPPING.items():
        if key in data:
            html = convert_to_zotero_html(data[key])
            
            payload = {
                "key": config["note"],
                "version": config["version"],
                "parentItem": config["parent"],
                "itemType": "note",
                "note": f'<div data-schema-version="9">{html}</div>',
                "tags": [],
                "relations": {}
            }
            
            payload_filename = f"{key}_payload.json"
            # Write to current directory
            with open(payload_filename, 'w') as f:
                json.dump(payload, f)
            
            cmd = f'curl -s -X PUT -H "Zotero-API-Key: {ZOTERO_API_KEY}" -H "Content-Type: application/json" --data @{payload_filename} "https://api.zotero.org/groups/{GROUP_ID}/items/{config["note"]}"'
            commands.append(cmd)
            
    # print("# Run these commands:")
    for cmd in commands:
        print(cmd)

if __name__ == "__main__":
    main()
