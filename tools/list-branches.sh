#!/bin/bash

# Script location: ~/Code/asciimath/energy/tools/list-branches.sh
# This script checks git branches in all repositories under ~/Code/asciimath/

# Function to list git branches for a directory
list_branches() {
    local dir="$1"
    echo "=== $dir ==="
    
    # Check if it's a git repository
    if [ -d "$dir/.git" ] || git -C "$dir" rev-parse --git-dir >/dev/null 2>&1; then
        # List all branches (local and remote)
        echo "Branches:"
        git -C "$dir" branch -a 2>/dev/null | sed 's/^/  /'
        
        # Show current branch more prominently
        current_branch=$(git -C "$dir" branch --show-current 2>/dev/null)
        if [ -n "$current_branch" ]; then
            echo "  Current: $current_branch"
        fi
    else
        echo "  Not a git repository"
    fi
    echo
}

# Main execution
# Navigate to the asciimath directory (two levels up from tools)
ASCIIMATH_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
echo "Checking git branches in repositories under $ASCIIMATH_DIR"
echo "============================================================="
echo

# Check if asciimath directory exists and has subdirectories
if [ ! -d "$ASCIIMATH_DIR" ]; then
    echo "Error: asciimath directory not found at $ASCIIMATH_DIR"
    exit 1
fi

if ! find "$ASCIIMATH_DIR" -mindepth 1 -maxdepth 1 -type d -print -quit | grep -q .; then
    echo "No subdirectories found in $ASCIIMATH_DIR"
    exit 0
fi

# Iterate through each subdirectory in asciimath (only 1 level deep)
cd "$ASCIIMATH_DIR"
for dir in */; do
    # Remove trailing slash and check if it's actually a directory
    dir_name="${dir%/}"
    if [ -d "$dir_name" ]; then
        list_branches "$dir_name"
    fi
done