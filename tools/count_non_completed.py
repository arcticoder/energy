#!/usr/bin/env python3
"""
TODO Task Counter and Display Utility

This script provides robust parsing and counting of tasks from NDJSON or concatenated JSON files,
specifically designed for tracking TODO items in project management files. It handles various
JSON formats including newline-delimited JSON, concatenated JSON objects, and JSON arrays.

Key Features:
- Flexible JSON parsing that handles mixed formats (NDJSON, arrays, concatenated objects)
- Case-insensitive status filtering (treats 'COMPLETED', 'completed', 'Completed' as complete)
- Optional detailed task display with pretty-printed JSON
- Exit codes for automation (0 = all complete, 2 = incomplete tasks found)
- Robust error handling for malformed JSON

Usage Examples:
    # Count non-completed tasks in default TODO.ndjson file
    python count_non_completed.py

    # Count tasks in specific file
    python count_non_completed.py path/to/tasks.ndjson

    # Show detailed non-completed tasks
    python count_non_completed.py --show

    # Use in CI/CD pipeline (exits with code 2 if incomplete tasks exist)
    python count_non_completed.py && echo "All tasks complete!" || echo "Tasks pending"

Exit Codes:
    0: All tasks are COMPLETED (or no tasks found)
    1: File not found or JSON parsing error
    2: Non-completed tasks exist

Task Format Expected:
    Each task should be a JSON object with at least a 'status' field.
    The script treats any status that is not exactly 'COMPLETED' (case-insensitive) as incomplete.

Author: SITS Migration Team
Version: 1.1 (Enhanced with comprehensive documentation)
"""
import argparse
import json
from json import JSONDecoder
from pathlib import Path

def parse_args():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description='Count non-COMPLETED tasks in a NDJSON or concatenated JSON file.',
        epilog='''
        Examples:
          %(prog)s                           # Count tasks in TODO.ndjson
          %(prog)s tasks.json --show         # Show details of incomplete tasks
          %(prog)s data/backlog.ndjson       # Count tasks in specific file
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', nargs='?', default='TODO.ndjson',
                        help='Path to TODO ndjson file (default: TODO.ndjson)')
    parser.add_argument('-s', '--show', action='store_true',
                        help='Show non-COMPLETED task objects (pretty JSON)')
    return parser.parse_args()

def parse_json_robustly(content):
    """
    Parse JSON content that may be in various formats:
    - Single JSON object
    - JSON array
    - Newline-delimited JSON (NDJSON)
    - Concatenated JSON objects
    
    Returns:
        tuple: (total_objects_parsed, list_of_parsed_objects)
    """
    decoder = JSONDecoder()
    idx = 0
    length = len(content)
    parsed_objects = []
    
    while idx < length:
        # Skip whitespace
        while idx < length and content[idx].isspace():
            idx += 1
        if idx >= length:
            break
            
        try:
            obj, end_idx = decoder.raw_decode(content, idx)
            # Handle both individual objects and arrays
            items = obj if isinstance(obj, list) else [obj]
            parsed_objects.extend(items)
            idx = end_idx
        except json.JSONDecodeError as e:
            print(f'JSON decode error at position {idx}: {e}')
            break
    
    return len(parsed_objects), parsed_objects

def filter_non_completed_tasks(tasks):
    """
    Filter tasks that are not marked as COMPLETED.
    
    Args:
        tasks: List of task dictionaries
        
    Returns:
        tuple: (total_count, non_completed_count, non_completed_tasks)
    """
    total_count = len(tasks)
    non_completed_tasks = []
    
    for task in tasks:
        if not isinstance(task, dict):
            # Non-dict items are considered incomplete
            non_completed_tasks.append(task)
            continue
            
        status = str(task.get('status', '')).upper()
        if status != 'COMPLETED':
            non_completed_tasks.append(task)
    
    return total_count, len(non_completed_tasks), non_completed_tasks

def display_tasks(tasks):
    """Display tasks in pretty JSON format with error handling."""
    if not tasks:
        print('\nNo non-COMPLETED tasks to show.')
        return
        
    print(f"\nShowing {len(tasks)} non-COMPLETED task(s):\n")
    for i, task in enumerate(tasks, 1):
        try:
            print(f"--- Task {i} ---")
            print(json.dumps(task, indent=2, ensure_ascii=False))
            print()  # Add blank line for readability
        except Exception as e:
            print(f"--- Task {i} (Display Error) ---")
            print(f"Error formatting task: {e}")
            print(f"Raw task data: {repr(task)}")
            print()

def main():
    """Main execution function."""
    args = parse_args()
    
    # Check if file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f'Error: File "{file_path}" not found')
        return 1
    
    try:
        # Read and parse the file
        content = file_path.read_text(encoding='utf-8')
        total_parsed, all_tasks = parse_json_robustly(content)
        
        if total_parsed == 0:
            print('No tasks found in file')
            return 0
            
        # Filter and count non-completed tasks
        total_count, non_completed_count, non_completed_tasks = filter_non_completed_tasks(all_tasks)
        
        # Display results
        print(f'Total tasks parsed: {total_count}')
        print(f'Non-COMPLETED tasks: {non_completed_count}')
        
        # Show detailed tasks if requested
        if args.show:
            display_tasks(non_completed_tasks)
        
        # Return appropriate exit code for automation
        return 0 if non_completed_count == 0 else 2
        
    except Exception as e:
        print(f'Error processing file: {e}')
        return 1

if __name__ == '__main__':
    # Parse command line arguments
    args = parse_args()
    
    # Legacy code for backward compatibility
    p = Path(args.file)
if __name__ == '__main__':
    # Execute main function and exit with appropriate code
    exit_code = main()
    raise SystemExit(exit_code)