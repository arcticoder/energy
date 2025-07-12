#!/usr/bin/env python3
"""
GitHub Traffic Statistics Collection Tool
Collects traffic stats from arcticoder repositories with JSON logging and HTML chart generation.
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
import os

# Configuration
REPOS = [
    "energy", "artificial-gravity-field-generator", "casimir-anti-stiction-metasurface-coatings",
    "casimir-environmental-enclosure-platform", "casimir-nanopositioning-platform", 
    "casimir-tunable-permittivity-stacks", "casimir-ultra-smooth-fabrication-platform",
    "elemental-transmutator", "enhanced-simulation-hardware-abstraction-framework",
    "lqg-anec-framework", "lqg-cosmological-constant-predictor", "lqg-volume-kernel-catalog",
    "lqg-first-principles-fine-structure-constant", "lqg-first-principles-gravitational-constant",
    "lqg-ftl-metric-engineering", "lqg-polymer-field-generator", "lqg-positive-matter-assembler",
    "lqg-volume-quantization-controller", "lorentz-violation-pipeline", "medical-tractor-array",
    "negative-energy-generator", "polymer-fusion-framework", "polymerized-lqg-matter-transporter",
    "polymerized-lqg-replicator-recycler", "su2-3nj-closedform", "su2-3nj-generating-functional",
    "su2-3nj-recurrences", "su2-3nj-uniform-closed-form", "su2-node-matrix-elements",
    "unified-gut-polymerization", "unified-lqg", "unified-lqg-qft", "warp-bubble-assemble-expressions",
    "warp-bubble-connection-curvature", "warp-bubble-coordinate-spec", "warp-bubble-einstein-equations",
    "warp-bubble-exotic-matter-density", "warp-bubble-metric-ansatz", "warp-bubble-mvp-simulator",
    "warp-bubble-optimizer", "warp-bubble-parameter-constraints", "warp-bubble-qft",
    "warp-bubble-shape-catalog", "warp-convergence-analysis", "warp-curvature-analysis",
    "warp-discretization", "warp-field-coils", "warp-lqg-midisuperspace", "warp-mock-data-generator",
    "warp-sensitivity-analysis", "warp-signature-workflow", "warp-solver-equations",
    "warp-spacetime-stability-controller"
]

SCRIPT_DIR = Path(__file__).parent
JSON_STATS_FILE = SCRIPT_DIR / "traffic_stats_history.json"
HTML_CHART_FILE = SCRIPT_DIR / "traffic_stats_chart.html"
HTML_TEMPLATE_FILE = SCRIPT_DIR / "traffic_chart_template.html"

def run_gh_command(args):
    """Run GitHub CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode != 0:
            # print(f"GitHub CLI error (code {result.returncode}): {result.stderr}")
            return None
            
        if not result.stdout or not result.stdout.strip():
            return None
            
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Command execution error: {e}")
        return None

def load_stats_history():
    """Load existing stats history from JSON file."""
    if JSON_STATS_FILE.exists():
        try:
            with open(JSON_STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading stats history: {e}")
            return []
    return []

def save_stats_history(history):
    """Save stats history to JSON file."""
    try:
        with open(JSON_STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"✅ Stats saved to {JSON_STATS_FILE}")
    except IOError as e:
        print(f"Error saving stats history: {e}")

def check_gh_auth():
    """Check if GitHub CLI is authenticated."""
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI not authenticated. Please run 'gh auth login'")
            return False
        print("✅ GitHub CLI authenticated")
        return True
    except FileNotFoundError:
        print("❌ GitHub CLI not found. Please install GitHub CLI")
        return False

def get_repo_info(repo):
    """Get repository information (stars, watchers, forks)."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}"])

def get_traffic_views(repo):
    """Get repository traffic views."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}/traffic/views"])

def get_traffic_clones(repo):
    """Get repository traffic clones."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}/traffic/clones"])

def process_repository(repo):
    """Process a single repository and return its data."""
    print(f"Repository: arcticoder/{repo}")
    print("-" * 60)
    
    repo_data = {
        "name": repo,
        "stars": 0,
        "watchers": 0,
        "forks": 0,
        "views_total": 0,
        "views_unique": 0,
        "clones_total": 0,
        "clones_unique": 0,
        "last_updated": "",
        "daily_views": [],
        "daily_clones": []
    }
    
    try:
        # Get repository info
        repo_info = get_repo_info(repo)
        if repo_info:
            print("📊 Repository Stats:")
            print(f"   ⭐ Stars: {repo_info.get('stargazers_count', 0)}")
            print(f"   👁️  Watchers: {repo_info.get('watchers_count', 0)}")
            print(f"   🍴 Forks: {repo_info.get('forks_count', 0)}")
            updated_at = repo_info.get('updated_at', '')
            if updated_at:
                updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                print(f"   📅 Last Updated: {updated_date.strftime('%b %d, %Y %H:%M')}")
            
            repo_data.update({
                "stars": repo_info.get('stargazers_count', 0),
                "watchers": repo_info.get('watchers_count', 0),
                "forks": repo_info.get('forks_count', 0),
                "last_updated": updated_at
            })
        else:
            print("📊 Repository Stats: Access denied or repository not found")
    except Exception as e:
        print(f"📊 Repository Stats: Error processing repository info - {e}")
    
    try:
        # Get views traffic
        views = get_traffic_views(repo)
        if views:
            print("📈 Views:")
            views_count = views.get('count', 0)
            views_uniques = views.get('uniques', 0)
            print(f"   Total: {views_count}, Unique: {views_uniques}")
            
            repo_data.update({
                "views_total": views_count,
                "views_unique": views_uniques
            })
            
            # Process daily views
            if 'views' in views and views['views']:
                from datetime import timezone
                past_24_hours = datetime.now(timezone.utc) - timedelta(days=1)
                print("   Recent daily breakdown:")
                
                for day in sorted(views['views'], key=lambda x: x['timestamp'], reverse=True)[:7]:
                    day_date = datetime.fromisoformat(day['timestamp'].replace('Z', '+00:00'))
                    date_str = day_date.strftime("%b %d")
                    count = day.get('count', 0)
                    uniques = day.get('uniques', 0)
                    
                    if count > 0:
                        indicator = " 🔥" if day_date > past_24_hours else ""
                        print(f"   {date_str}: {count} views ({uniques} unique){indicator}")
                    
                    repo_data["daily_views"].append({
                        "date": day_date.strftime("%Y-%m-%d"),
                        "views": count,
                        "unique_views": uniques
                    })
        else:
            print("📈 Views: Access denied or repository not found")
    except Exception as e:
        print(f"📈 Views: Error processing views data - {e}")
    
    try:
        # Get clones traffic
        clones = get_traffic_clones(repo)
        if clones:
            print("📦 Clones:")
            clones_count = clones.get('count', 0)
            clones_uniques = clones.get('uniques', 0)
            print(f"   Total: {clones_count}, Unique: {clones_uniques}")
            
            repo_data.update({
                "clones_total": clones_count,
                "clones_unique": clones_uniques
            })
            
            # Process daily clones
            if 'clones' in clones and clones['clones']:
                from datetime import timezone
                past_48_hours = datetime.now(timezone.utc) - timedelta(days=2)
                print("   Recent daily breakdown:")
                
                for day in sorted(clones['clones'], key=lambda x: x['timestamp'], reverse=True)[:7]:
                    day_date = datetime.fromisoformat(day['timestamp'].replace('Z', '+00:00'))
                    date_str = day_date.strftime("%b %d")
                    count = day.get('count', 0)
                    uniques = day.get('uniques', 0)
                    
                    if count > 0:
                        indicator = " ⭐" if day_date > past_48_hours else ""
                        print(f"   {date_str}: {count} clones ({uniques} unique){indicator}")
                    
                    repo_data["daily_clones"].append({
                        "date": day_date.strftime("%Y-%m-%d"),
                        "clones": count,
                        "unique_clones": uniques
                    })
        else:
            print("📦 Clones: Access denied or repository not found")
    except Exception as e:
        print(f"📦 Clones: Error processing clones data - {e}")
    
    print()
    return repo_data

def generate_html_chart(current_run, stats_history):
    """Generate HTML chart using template."""
    print("📊 Generating HTML chart...")
    
    # Prepare chart data
    chart_data = {
        "labels": [],
        "datasets": [
            {
                "label": "Total Views",
                "data": [],
                "borderColor": "rgb(75, 192, 192)",
                "backgroundColor": "rgba(75, 192, 192, 0.1)",
                "tension": 0.1
            },
            {
                "label": "Unique Views", 
                "data": [],
                "borderColor": "rgb(255, 99, 132)",
                "backgroundColor": "rgba(255, 99, 132, 0.1)",
                "tension": 0.1
            },
            {
                "label": "Total Clones",
                "data": [],
                "borderColor": "rgb(54, 162, 235)",
                "backgroundColor": "rgba(54, 162, 235, 0.1)",
                "tension": 0.1
            },
            {
                "label": "Unique Clones",
                "data": [],
                "borderColor": "rgb(255, 206, 86)",
                "backgroundColor": "rgba(255, 206, 86, 0.1)",
                "tension": 0.1
            }
        ]
    }
    
    # Extract data from history (last 30 runs)
    recent_history = sorted(stats_history, key=lambda x: x['timestamp'])[-30:]
    for run in recent_history:
        chart_data["labels"].append(run["date"])
        chart_data["datasets"][0]["data"].append(run["totals"]["views"])
        chart_data["datasets"][1]["data"].append(run["totals"]["unique_views"])
        chart_data["datasets"][2]["data"].append(run["totals"]["clones"])
        chart_data["datasets"][3]["data"].append(run["totals"]["unique_clones"])
    
    # Read template and replace placeholders
    try:
        with open(HTML_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print(f"❌ HTML template not found: {HTML_TEMPLATE_FILE}")
        return
    
    update_time = datetime.now().strftime("%B %d, %Y %H:%M")
    chart_data_json = json.dumps(chart_data)
    
    # Replace placeholders
    html = html_template.replace('{{UPDATE_TIME}}', update_time)
    html = html.replace('{{TOTAL_VIEWS}}', str(current_run["totals"]["views"]))
    html = html.replace('{{UNIQUE_VIEWS}}', str(current_run["totals"]["unique_views"]))
    html = html.replace('{{TOTAL_CLONES}}', str(current_run["totals"]["clones"]))
    html = html.replace('{{UNIQUE_CLONES}}', str(current_run["totals"]["unique_clones"]))
    html = html.replace('{{TOTAL_STARS}}', str(current_run["totals"]["stars"]))
    html = html.replace('{{CHART_DATA}}', chart_data_json)
    
    # Write HTML file
    try:
        with open(HTML_CHART_FILE, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML chart generated: {HTML_CHART_FILE}")
        print("🌐 Open the file in your browser to view the interactive chart")
    except IOError as e:
        print(f"Error writing HTML file: {e}")

def main():
    """Main function."""
    print("🚀 GitHub Traffic Stats Collection Tool")
    print("=" * 50)
    
    # Check authentication
    if not check_gh_auth():
        sys.exit(1)
    
    # Load existing stats history
    stats_history = load_stats_history()
    print(f"📚 Loaded {len(stats_history)} previous runs from history")
    
    # Create current run data structure
    current_run = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "repositories": {},
        "totals": {
            "views": 0,
            "unique_views": 0,
            "clones": 0,
            "unique_clones": 0,
            "stars": 0,
            "watchers": 0,
            "forks": 0,
            "repositories_count": len(REPOS)
        }
    }
    
    # Process each repository
    for repo in REPOS:
        repo_data = process_repository(repo)
        current_run["repositories"][repo] = repo_data
        
        # Add to totals
        current_run["totals"]["views"] += repo_data["views_total"]
        current_run["totals"]["unique_views"] += repo_data["views_unique"]
        current_run["totals"]["clones"] += repo_data["clones_total"]
        current_run["totals"]["unique_clones"] += repo_data["clones_unique"]
        current_run["totals"]["stars"] += repo_data["stars"]
        current_run["totals"]["watchers"] += repo_data["watchers"]
        current_run["totals"]["forks"] += repo_data["forks"]
    
    # Display summary
    totals = current_run["totals"]
    print("=== SUMMARY ===")
    print(f"Total Views: {totals['views']} (Unique: {totals['unique_views']})")
    print(f"Total Clones: {totals['clones']} (Unique: {totals['unique_clones']})")
    print("\nRepository Engagement:")
    print(f"Total Stars: {totals['stars']}")
    print(f"Total Watchers: {totals['watchers']}")
    print(f"Total Forks: {totals['forks']}")
    print(f"Repositories Checked: {totals['repositories_count']}")
    print()
    print("🔥 indicates activity within the past 24 hours")
    print("Note: GitHub Traffic API provides data for the past 14 days maximum")
    
    # Save stats history
    stats_history.append(current_run)
    save_stats_history(stats_history)
    
    # Generate HTML chart
    generate_html_chart(current_run, stats_history)

if __name__ == "__main__":
    main()
