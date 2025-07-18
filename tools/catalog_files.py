#!/usr/bin/env python3
"""
File Catalog System for ASCIIMath Projects
Recursively scans all .ps1 and .py files under C:\\Users\\%USERNAME%\\Code\\asciimath
and generates a comprehensive catalog with metadata.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import getpass

def get_file_metadata(file_path):
    """Extract metadata for a given file."""
    stat = file_path.stat()
    return {
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
    }

def get_repo_name(file_path, base_path):
    """Extract repository name from file path."""
    relative_to_base = file_path.relative_to(base_path)
    return relative_to_base.parts[0] if relative_to_base.parts else ""

def normalize_path_for_username(path_str):
    """Replace actual username with %USERNAME% placeholder."""
    username = getpass.getuser()
    return path_str.replace(f"C:\\Users\\{username}\\", "C:\\Users\\%USERNAME%\\")

def scan_asciimath_files():
    """Scan all .ps1 and .py files in the asciimath directory tree."""
    username = getpass.getuser()
    base_path = Path(f"C:\\Users\\{username}\\Code\\asciimath")
    
    if not base_path.exists():
        print(f"Error: Base path {base_path} does not exist!")
        return []
    
    files_data = []
    file_extensions = {'.py', '.ps1', '.js'}
    
    print(f"Scanning files in: {base_path}")
    
    for file_path in base_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in file_extensions:
            try:
                # Get repository name
                repo_name = get_repo_name(file_path, base_path)
                
                # Calculate relative path within repository
                repo_path = base_path / repo_name
                relative_path = file_path.relative_to(repo_path)
                
                # Get file metadata
                metadata = get_file_metadata(file_path)
                
                # Create file record
                file_record = {
                    'file_name': file_path.name,
                    'relative_path': str(relative_path).replace('\\', '/'),
                    'absolute_path': normalize_path_for_username(str(file_path)),
                    'repository': repo_name,
                    'file_extension': file_path.suffix.lower(),
                    'date_created': metadata['created'],
                    'date_modified': metadata['modified'],
                    'file_size_bytes': file_path.stat().st_size
                }
                
                files_data.append(file_record)
                print(f"Cataloged: {repo_name}/{relative_path}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
    
    return files_data

def save_catalog_json(files_data, output_path):
    """Save the file catalog as JSON."""
    # Load existing catalog if present
    if output_path.exists():
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_catalog = json.load(f)
            existing_files = { (f['repository'], f['relative_path']): f for f in existing_catalog.get('files', []) }
        except Exception as e:
            print(f"Warning: Could not load existing catalog: {e}")
            existing_files = {}
    else:
        existing_files = {}

    # Merge new scan with existing entries
    updated_files = []
    for file_record in files_data:
        key = (file_record['repository'], file_record['relative_path'])
        if key in existing_files:
            # Update only scanned fields, preserve extra metadata
            merged = existing_files[key].copy()
            merged.update(file_record)
            updated_files.append(merged)
        else:
            updated_files.append(file_record)

    # Optionally, keep entries not present in new scan (unscanned files)
    # If you want to remove them, comment out the following block
    for key, entry in existing_files.items():
        if key not in { (f['repository'], f['relative_path']) for f in files_data }:
            updated_files.append(entry)

    catalog = {
        'scan_timestamp': datetime.now().isoformat(),
        'total_files': len(updated_files),
        'scan_summary': {
            'python_files': len([f for f in updated_files if f['file_extension'] == '.py']),
            'powershell_files': len([f for f in updated_files if f['file_extension'] == '.ps1']),
            'repositories': len(set(f['repository'] for f in updated_files))
        },
        'files': updated_files
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Catalog saved to: {output_path}")
    return catalog

def generate_html_report(catalog, output_path):
    """Generate an HTML report from the catalog data."""
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCIIMath Project File Catalog</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .controls {
            padding: 20px 30px;
            background: white;
            border-bottom: 1px solid #eee;
        }
        
        .search-box {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }
        
        .search-box:focus {
            border-color: #667eea;
            outline: none;
        }
        
        .filters {
            margin-top: 15px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
        }
        
        .table-container {
            overflow-x: auto;
            max-height: 600px;
            overflow-y: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        
        th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.2s;
        }
        
        th:hover {
            background: #5a6fd8;
        }
        
        th.sortable::after {
            content: ' ↕️';
            font-size: 0.8em;
            opacity: 0.7;
        }
        
        th.sort-asc::after {
            content: ' ↑';
            font-size: 0.8em;
            opacity: 1;
        }
        
        th.sort-desc::after {
            content: ' ↓';
            font-size: 0.8em;
            opacity: 1;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            vertical-align: top;
        }
        
        tr:hover {
            background-color: #f8f9fa;
        }
        
        .repo-badge {
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .ext-py {
            color: #3776ab;
            font-weight: bold;
        }
        
        .ext-ps1 {
            color: #012456;
            font-weight: bold;
        }
        
        .ext-js {
            color: #f7df1e;
            background: #323330;
            font-weight: bold;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        .path-code {
            font-family: 'Courier New', monospace;
            background: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        
        .timestamp {
            font-size: 0.85em;
            color: #666;
        }
        
        .file-size {
            text-align: right;
            font-family: monospace;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
            font-style: italic;
        }
        
        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8em;
            transition: all 0.2s;
            min-width: 50px;
        }
        
        .copy-btn:hover {
            background: #5a6fd8;
            transform: translateY(-1px);
        }
        
        .copy-btn:active {
            transform: translateY(0);
        }
        
        .copy-btn.copied {
            background: #28a745;
        }
        
        .copy-btn.copied::after {
            content: ' ✓';
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 0;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .stats {
                grid-template-columns: 1fr 1fr;
                padding: 20px;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ASCIIMath Project File Catalog</h1>
            <p>Comprehensive scan of Python and PowerShell files</p>
            <p class="timestamp">Last updated: {{SCAN_TIMESTAMP}}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{TOTAL_FILES}}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{PYTHON_FILES}}</div>
                <div class="stat-label">Python Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{POWERSHELL_FILES}}</div>
                <div class="stat-label">PowerShell Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{REPOSITORIES}}</div>
                <div class="stat-label">Repositories</div>
            </div>
        </div>
        
        <div class="controls">
            <input type="text" id="searchBox" class="search-box" placeholder="Search files, repositories, or paths...">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">All Files</button>
                <button class="filter-btn" data-filter=".py">Python Only</button>
                <button class="filter-btn" data-filter=".ps1">PowerShell Only</button>
                <button class="filter-btn" data-filter="recent">Recently Modified</button>
            </div>
        </div>
        
        <div class="table-container">
            <table id="filesTable">
                <thead>
                    <tr>
                        <th class="sortable" data-sort="file_name">File Name</th>
                        <th class="sortable" data-sort="repository">Repository</th>
                        <th class="sortable" data-sort="relative_path">Relative Path</th>
                        <th class="sortable" data-sort="date_modified">Date Modified</th>
                        <th class="sortable" data-sort="date_created">Date Created</th>
                        <th class="sortable" data-sort="file_size_bytes">Size</th>
                        <th>Copy Path</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <!-- Rows will be populated by JavaScript -->
                </tbody>
            </table>
            <div id="noResults" class="no-results" style="display: none;">
                No files match your search criteria.
            </div>
        </div>
    </div>

    <script>
        const filesData = {{FILES_JSON}};
        let currentSort = { column: null, direction: 'asc' };
        
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        }
        
        function formatDate(isoString) {
            const date = new Date(isoString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
        
        function sortFiles(files, column, direction) {
            return files.sort((a, b) => {
                let aVal = a[column];
                let bVal = b[column];
                
                // Handle different data types
                if (column === 'date_modified' || column === 'date_created') {
                    aVal = new Date(aVal);
                    bVal = new Date(bVal);
                } else if (column === 'file_size_bytes') {
                    aVal = parseInt(aVal);
                    bVal = parseInt(bVal);
                } else {
                    aVal = aVal.toString().toLowerCase();
                    bVal = bVal.toString().toLowerCase();
                }
                
                let comparison = 0;
                if (aVal > bVal) {
                    comparison = 1;
                } else if (aVal < bVal) {
                    comparison = -1;
                }
                
                return direction === 'desc' ? comparison * -1 : comparison;
            });
        }
        
        function copyToClipboard(path, buttonId) {
            console.log('Copy button clicked for path:', path);
            console.log('Button ID:', buttonId);
            
            // Use the modern Clipboard API if available
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(path).then(() => {
                    console.log('Successfully copied to clipboard:', path);
                    showCopySuccess(buttonId);
                }).catch((err) => {
                    console.error('Failed to copy text: ', err);
                    fallbackCopyTextToClipboard(path, buttonId);
                });
            } else {
                console.log('Using fallback copy method');
                // Fallback for older browsers or non-secure contexts
                fallbackCopyTextToClipboard(path, buttonId);
            }
        }
        
        function fallbackCopyTextToClipboard(text, buttonId) {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.position = "fixed";
            textArea.style.opacity = "0";
            
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                const successful = document.execCommand('copy');
                if (successful) {
                    showCopySuccess(buttonId);
                } else {
                    console.error('Fallback: Copying text command was unsuccessful');
                }
            } catch (err) {
                console.error('Fallback: Unable to copy', err);
            }
            
            document.body.removeChild(textArea);
        }
        
        function showCopySuccess(buttonId) {
            const button = document.getElementById(buttonId);
            if (button) {
                const originalText = button.textContent;
                button.classList.add('copied');
                button.textContent = 'Copied';
                
                setTimeout(() => {
                    button.classList.remove('copied');
                    button.textContent = originalText;
                }, 2000);
            }
        }
        
        function updateSortIndicators(activeColumn, direction) {
            // Remove all sort classes
            document.querySelectorAll('th.sortable').forEach(th => {
                th.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add sort class to active column
            if (activeColumn) {
                const activeHeader = document.querySelector(`th[data-sort="${activeColumn}"]`);
                if (activeHeader) {
                    activeHeader.classList.add(direction === 'asc' ? 'sort-asc' : 'sort-desc');
                }
            }
        }
        
        function createFileRow(file) {
            let extClass = 'ext-other';
            if (file.file_extension === '.py') {
                extClass = 'ext-py';
            } else if (file.file_extension === '.ps1') {
                extClass = 'ext-ps1';
            } else if (file.file_extension === '.js') {
                extClass = 'ext-js';
            }
            
            const copyBtnId = `copy-${file.repository}-${file.file_name}`.replace(/[^a-zA-Z0-9-]/g, '-');
            // Properly escape the path for onclick handler
            const escapedPath = file.absolute_path.replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\'");
            return `
                <tr data-repo="${file.repository}" data-ext="${file.file_extension}" data-modified="${file.date_modified}">
                    <td><span class="${extClass}">${file.file_name}</span></td>
                    <td><span class="repo-badge">${file.repository}</span></td>
                    <td><code class="path-code">${file.relative_path}</code></td>
                    <td class="timestamp">${formatDate(file.date_modified)}</td>
                    <td class="timestamp">${formatDate(file.date_created)}</td>
                    <td class="file-size">${formatFileSize(file.file_size_bytes)}</td>
                    <td><button class="copy-btn" id="${copyBtnId}" onclick="copyToClipboard('${escapedPath}', '${copyBtnId}')">Copy</button></td>
                </tr>
            `;
        }
        
        function filterFiles(searchTerm, extensionFilter, recentFilter) {
            let filteredFiles = filesData.files;
            
            // Extension filter
            if (extensionFilter !== 'all') {
                if (extensionFilter === 'recent') {
                    const thirtyDaysAgo = new Date();
                    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
                    filteredFiles = filteredFiles.filter(file => 
                        new Date(file.date_modified) > thirtyDaysAgo
                    );
                } else {
                    filteredFiles = filteredFiles.filter(file => 
                        file.file_extension === extensionFilter
                    );
                }
            }
            
            // Search filter
            if (searchTerm) {
                const term = searchTerm.toLowerCase();
                filteredFiles = filteredFiles.filter(file =>
                    file.file_name.toLowerCase().includes(term) ||
                    file.repository.toLowerCase().includes(term) ||
                    file.relative_path.toLowerCase().includes(term) ||
                    file.absolute_path.toLowerCase().includes(term)
                );
            }
            
            return filteredFiles;
        }
        
        function updateTable() {
            console.log('updateTable called');
            console.log('Total files in filesData:', filesData.files.length);
            
            const searchTerm = document.getElementById('searchBox').value;
            const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
            
            let filteredFiles = filterFiles(searchTerm, activeFilter);
            console.log('Filtered files:', filteredFiles.length);
            
            // Apply sorting if a column is selected
            if (currentSort.column) {
                filteredFiles = sortFiles(filteredFiles, currentSort.column, currentSort.direction);
            }
            
            const tableBody = document.getElementById('tableBody');
            const noResults = document.getElementById('noResults');
            
            if (filteredFiles.length === 0) {
                console.log('No files to display');
                tableBody.innerHTML = '';
                noResults.style.display = 'block';
            } else {
                console.log('Displaying', filteredFiles.length, 'files');
                tableBody.innerHTML = filteredFiles.map(createFileRow).join('');
                noResults.style.display = 'none';
            }
            
            // Update sort indicators
            updateSortIndicators(currentSort.column, currentSort.direction);
        }
        
        // Event listeners
        document.getElementById('searchBox').addEventListener('input', updateTable);
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                updateTable();
            });
        });
        
        // Add sorting event listeners
        document.querySelectorAll('th.sortable').forEach(header => {
            header.addEventListener('click', function() {
                const column = this.dataset.sort;
                
                // Toggle direction if same column, otherwise start with asc
                if (currentSort.column === column) {
                    currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
                } else {
                    currentSort.column = column;
                    currentSort.direction = 'asc';
                }
                
                updateTable();
            });
        });
        
        // Initialize table
        updateTable();
    </script>
</body>
</html>"""
    
    # Replace placeholders
    html_content = html_template.replace('{{SCAN_TIMESTAMP}}', datetime.fromisoformat(catalog['scan_timestamp']).strftime('%B %d, %Y at %I:%M %p'))
    html_content = html_content.replace('{{TOTAL_FILES}}', str(catalog['total_files']))
    html_content = html_content.replace('{{PYTHON_FILES}}', str(catalog['scan_summary']['python_files']))
    html_content = html_content.replace('{{POWERSHELL_FILES}}', str(catalog['scan_summary']['powershell_files']))
    html_content = html_content.replace('{{REPOSITORIES}}', str(catalog['scan_summary']['repositories']))
    html_content = html_content.replace('{{FILES_JSON}}', json.dumps(catalog, ensure_ascii=False))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML report generated: {output_path}")

def format_file_size(bytes_size):
    """Format file size in human-readable format."""
    if bytes_size == 0:
        return '0 B'
    
    size_names = ['B', 'KB', 'MB', 'GB']
    i = 0
    while bytes_size >= 1024 and i < len(size_names) - 1:
        bytes_size /= 1024.0
        i += 1
    
    return f"{bytes_size:.1f} {size_names[i]}"

def main():
    """Main execution function."""
    print("=== ASCIIMath File Catalog System ===")
    print("Scanning for .py and .ps1 files...")
    
    # Scan files
    files_data = scan_asciimath_files()
    
    if not files_data:
        print("No files found to catalog!")
        return
    
    # Save JSON catalog
    json_path = Path(__file__).parent / "file_catalog.json"
    catalog = save_catalog_json(files_data, json_path)
    
    # Generate HTML report
    html_path = Path(__file__).parent / "file_catalog.html"
    generate_html_report(catalog, html_path)
    
    print(f"\n=== Catalog Complete ===")
    print(f"Files cataloged: {len(files_data)}")
    print(f"Python files: {catalog['scan_summary']['python_files']}")
    print(f"PowerShell files: {catalog['scan_summary']['powershell_files']}")
    print(f"Repositories: {catalog['scan_summary']['repositories']}")
    print(f"JSON catalog: {json_path}")
    print(f"HTML report: {html_path}")

if __name__ == "__main__":
    main()
