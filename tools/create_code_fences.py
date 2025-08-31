#!/usr/bin/env python3
import argparse
import os
import sys
import fnmatch

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def find_files(root_dir, patterns, exclude_patterns):
    matches = []
    for base, dirs, files in os.walk(root_dir):
        # prune directories whose names match any exclude pattern
        dirs[:] = [
            d for d in dirs
            if not any(fnmatch.fnmatch(d, pat) for pat in exclude_patterns)
        ]
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(base, filename))
    return matches

def is_npy_file(filepath):
    """Check if file has .npy extension"""
    return filepath.lower().endswith('.npy')

def read_npy_file(filepath):
    """Read .npy file and return string representation"""
    if not HAS_NUMPY:
        return "Error: NumPy not available. Install with: pip install numpy"
    
    try:
        array = np.load(filepath)
        # Create a comprehensive string representation
        lines = []
        lines.append(f"# NumPy array file: {os.path.basename(filepath)}")
        lines.append(f"# Shape: {array.shape}")
        lines.append(f"# Data type: {array.dtype}")
        lines.append(f"# Size: {array.size} elements")
        lines.append("")
        
        # Add the array representation
        lines.append("# Array contents:")
        if array.size <= 1000:  # For small arrays, show full content
            lines.append(repr(array))
        else:  # For large arrays, show summary
            lines.append(f"# Large array with {array.size} elements. Showing summary:")
            lines.append(str(array))
        
        return "\n".join(lines)
    except Exception as e:
        return f"Error reading .npy file: {e}"

def create_code_fences(file_paths, output_path):
    with open(output_path, 'w', encoding='utf-8') as out_f:
        for path in file_paths:
            abs_path = os.path.abspath(path)
            try:
                if is_npy_file(path):
                    # Handle .npy files specially
                    content = read_npy_file(path)
                else:
                    # Handle regular text files
                    with open(path, 'r', encoding='utf-8') as in_f:
                        content = in_f.read()
            except Exception as e:
                print(f"Warning: could not read {path}: {e}", file=sys.stderr)
                continue

            out_f.write(f"```{abs_path}\n")
            out_f.write(content)
            if not content.endswith('\n'):
                out_f.write('\n')
            out_f.write("```\n")

def main():
    parser = argparse.ArgumentParser(
        description="Recursively find files under a root (excluding folders by wildcard patterns) and generate markdown code fences."
    )
    parser.add_argument(
        "--root", "-r", required=True,
        help="Root directory to search."
    )
    parser.add_argument(
        "--pattern", "-p", required=True, nargs="+",
        help="Wildcard patterns to include (e.g. *.py *.md)."
    )
    parser.add_argument(
        "--exclude", "-e", nargs="*", default=[],
        help="Directory name patterns to exclude (supports wildcards, e.g. node_* .git build?)."
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Full path to the output file where fenced code will be written."
    )
    args = parser.parse_args()

    files = find_files(args.root, args.pattern, args.exclude)
    if not files:
        print(f"No files matching {args.pattern} under {args.root}", file=sys.stderr)
        sys.exit(1)

    create_code_fences(files, args.output)

if __name__ == "__main__":
    main()
