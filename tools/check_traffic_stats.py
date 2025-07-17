#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Traffic Statistics Collection Tool
Collects traffic stats from arcticoder repositories with JSON logging and HTML chart generation.
"""

import json
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
import os
import numpy as np
from scipy import stats

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    try:
        # Try to set console to UTF-8 mode
        import locale
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        # Fallback for older Python versions or if reconfigure fails
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach(), errors='replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach(), errors='replace')

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
NDJSON_STATS_FILE = SCRIPT_DIR / "traffic_stats_history.ndjson"
HTML_CHART_FILE = SCRIPT_DIR / "traffic_stats_chart.html"
HTML_TEMPLATE_FILE = SCRIPT_DIR / "traffic_chart_template.html"
SLOPE_HISTORY_FILE = SCRIPT_DIR / "traffic_slope_history.json"

def run_gh_command(args):
    """Run GitHub CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30,  # Add 30-second timeout
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode != 0:
            # print(f"GitHub CLI error (code {result.returncode}): {result.stderr}")
            return None
            
        if not result.stdout or not result.stdout.strip():
            return None
            
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  GitHub CLI command timed out after 30 seconds")
        return None
    except json.JSONDecodeError:
        print(f"   ⚠️  Invalid JSON response from GitHub CLI")
        return None
    except Exception as e:
        print(f"   ⚠️  Error running GitHub CLI command: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Command execution error: {e}")
        return None

def load_stats_history():
    """Load existing stats history from NDJSON file."""
    if NDJSON_STATS_FILE.exists():
        try:
            history = []
            with open(NDJSON_STATS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        history.append(json.loads(line))
            return history
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading stats history: {e}")
            return []
    return []

def save_stats_history(history):
    """Save stats history to NDJSON file with deduplication by date."""
    try:
        # Deduplicate by date - keep only the latest entry for each date
        date_entries = {}
        
        for entry in history:
            date = entry.get('date')
            if date:
                # Keep the latest timestamp for each date
                if date not in date_entries or entry.get('timestamp', '') > date_entries[date].get('timestamp', ''):
                    date_entries[date] = entry
        
        # Sort by date
        sorted_entries = sorted(date_entries.values(), key=lambda x: x.get('date', ''))
        
        with open(NDJSON_STATS_FILE, 'w', encoding='utf-8') as f:
            for entry in sorted_entries:
                f.write(json.dumps(entry, separators=(',', ':')) + '\n')
        
        safe_print(f"✅ Stats saved to {NDJSON_STATS_FILE} ({len(sorted_entries)} unique dates)")
    except IOError as e:
        print(f"Error saving stats history: {e}")

def load_slope_history():
    """Load existing slope history from JSON file."""
    if SLOPE_HISTORY_FILE.exists():
        try:
            with open(SLOPE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading slope history: {e}")
            return []
    return []

def save_slope_history(slope_history):
    """Save slope history to JSON file."""
    try:
        with open(SLOPE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(slope_history, f, indent=2, ensure_ascii=False)
        safe_print(f"✅ Slope history saved to {SLOPE_HISTORY_FILE}")
    except IOError as e:
        print(f"Error saving slope history: {e}")

def calculate_trend_slope(daily_aggregates, metric='views'):
    """Calculate the slope (trend) of the specified metric over time."""
    if len(daily_aggregates) < 3:  # Need at least 3 points for meaningful slope
        return None, None, None
    
    # Sort dates and prepare data
    sorted_dates = sorted(daily_aggregates.keys())
    x_values = list(range(len(sorted_dates)))  # Day indices
    y_values = [daily_aggregates[date][metric] for date in sorted_dates]
    
    # Calculate linear regression
    if len(x_values) >= 2 and any(y > 0 for y in y_values):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
        return slope, r_value**2, len(sorted_dates)  # slope, R², number of days
    
    return None, None, None

def merge_historical_daily_data(stats_history):
    """Merge daily data from all historical runs, preserving all historical data."""
    all_daily_data = {}
    
    for run in stats_history:
        run_date = run.get("date", "")
        run_totals = run.get("totals", {})
        
        # Store totals for this date (repository-level aggregation)
        if run_date and run_date not in all_daily_data:
            all_daily_data[run_date] = {
                "views": 0, 
                "unique_views": 0, 
                "clones": 0, 
                "unique_clones": 0,
                "stars": run_totals.get("stars", 0),
                "watchers": run_totals.get("watchers", 0), 
                "forks": run_totals.get("forks", 0),
                "active_forks": run_totals.get("active_forks", 0),
                "recent_forks": run_totals.get("recent_forks", 0)
            }
        elif run_date:
            # Update with latest totals for the date
            all_daily_data[run_date]["stars"] = run_totals.get("stars", 0)
            all_daily_data[run_date]["watchers"] = run_totals.get("watchers", 0)
            all_daily_data[run_date]["forks"] = run_totals.get("forks", 0)
            all_daily_data[run_date]["active_forks"] = run_totals.get("active_forks", 0)
            all_daily_data[run_date]["recent_forks"] = run_totals.get("recent_forks", 0)
        
        # Process each repository in this run for traffic data
        for repo_name, repo_data in run.get("repositories", {}).items():
            
            # Merge daily views
            for day_data in repo_data.get("daily_views", []):
                date = day_data["date"]
                if date not in all_daily_data:
                    all_daily_data[date] = {"views": 0, "unique_views": 0, "clones": 0, "unique_clones": 0, "stars": 0, "watchers": 0, "forks": 0, "active_forks": 0, "recent_forks": 0}
                
                # Accumulate data (sum across all repos for that date)
                all_daily_data[date]["views"] += day_data.get("views", 0)
                all_daily_data[date]["unique_views"] += day_data.get("unique_views", 0)
            
            # Merge daily clones
            for day_data in repo_data.get("daily_clones", []):
                date = day_data["date"]
                if date not in all_daily_data:
                    all_daily_data[date] = {"views": 0, "unique_views": 0, "clones": 0, "unique_clones": 0, "stars": 0, "watchers": 0, "forks": 0, "active_forks": 0, "recent_forks": 0}
                
                # Accumulate data (sum across all repos for that date)
                all_daily_data[date]["clones"] += day_data.get("clones", 0)
                all_daily_data[date]["unique_clones"] += day_data.get("unique_clones", 0)
    
    return all_daily_data

def check_gh_auth():
    """Check if GitHub CLI is authenticated."""
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            safe_print("❌ GitHub CLI not authenticated. Please run 'gh auth login'")
            return False
        safe_print("✅ GitHub CLI authenticated")
        return True
    except FileNotFoundError:
        safe_print("❌ GitHub CLI not found. Please install GitHub CLI")
        return False

def get_repo_forks(repo):
    """Get detailed repository forks information."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}/forks", "--paginate"])

def get_repo_info(repo):
    """Get repository information (stars, watchers, forks)."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}"])

def get_traffic_views(repo):
    """Get repository traffic views."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}/traffic/views"])

def get_traffic_clones(repo):
    """Get repository traffic clones."""
    return run_gh_command(["api", f"repos/arcticoder/{repo}/traffic/clones"])

def get_repo_commits(repo, days=30):
    """Get recent commit activity to help infer pull frequency."""
    since_date = (datetime.now() - timedelta(days=days)).isoformat()
    return run_gh_command(["api", f"repos/arcticoder/{repo}/commits", "--field", "sha,commit,author", "-F", f"since={since_date}", "--paginate"])

def safe_print(text):
    """Safely print text with Unicode characters, falling back to ASCII if needed."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: replace Unicode characters with ASCII equivalents
        ascii_text = text.replace("🚀", "[ROCKET]").replace("✅", "[OK]").replace("❌", "[ERROR]")
        ascii_text = ascii_text.replace("📊", "[CHART]").replace("⭐", "[STAR]").replace("👁️", "[EYE]")
        ascii_text = ascii_text.replace("🍴", "[FORK]").replace("📅", "[DATE]").replace("📈", "[GRAPH]")
        ascii_text = ascii_text.replace("🔥", "[HOT]")
        print(ascii_text)

def process_repository(repo):
    """Process a single repository and return its data."""
    print(f"Repository: arcticoder/{repo}")
    print("-" * 60)
    
    repo_data = {
        "name": repo,
        "stars": 0,
        "watchers": 0,
        "forks": 0,
        "fork_details": [],
        "active_forks": 0,
        "recent_forks": 0,
        "views_total": 0,
        "views_unique": 0,
        "clones_total": 0,
        "clones_unique": 0,
        "clone_pull_ratio": 0,
        "recent_commits": 0,
        "commit_frequency": 0,
        "last_updated": "",
        "daily_views": [],
        "daily_clones": []
    }
    
    try:
        # Get repository info
        repo_info = get_repo_info(repo)
        if repo_info:
            safe_print("📊 Repository Stats:")
            safe_print(f"   ⭐ Stars: {repo_info.get('stargazers_count', 0)}")
            safe_print(f"   👁️  Watchers: {repo_info.get('watchers_count', 0)}")
            safe_print(f"   🍴 Forks: {repo_info.get('forks_count', 0)}")
            updated_at = repo_info.get('updated_at', '')
            if updated_at:
                updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                safe_print(f"   📅 Last Updated: {updated_date.strftime('%b %d, %Y %H:%M')}")
            
            repo_data.update({
                "stars": repo_info.get('stargazers_count', 0),
                "watchers": repo_info.get('watchers_count', 0),
                "forks": repo_info.get('forks_count', 0),
                "last_updated": updated_at
            })
        else:
            safe_print("📊 Repository Stats: Access denied or repository not found")
    except Exception as e:
        safe_print(f"📊 Repository Stats: Error processing repository info - {e}")

    # Get detailed fork information
    try:
        forks_data = get_repo_forks(repo)
        if forks_data and isinstance(forks_data, list):
            safe_print("🍴 Fork Analysis:")
            total_forks = len(forks_data)
            
            # Analyze fork activity
            active_forks = 0
            recent_forks = 0
            fork_details = []
            
            # Define thresholds
            from datetime import timezone
            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            ninety_days_ago = datetime.now(timezone.utc) - timedelta(days=90)
            
            for fork in forks_data:
                fork_info = {
                    "name": fork.get('full_name', ''),
                    "owner": fork.get('owner', {}).get('login', ''),
                    "created_at": fork.get('created_at', ''),
                    "updated_at": fork.get('updated_at', ''),
                    "stars": fork.get('stargazers_count', 0),
                    "size": fork.get('size', 0)
                }
                
                # Check if fork is active (updated in last 90 days)
                if fork.get('updated_at'):
                    updated_date = datetime.fromisoformat(fork['updated_at'].replace('Z', '+00:00'))
                    if updated_date > ninety_days_ago:
                        active_forks += 1
                    if updated_date > thirty_days_ago:
                        recent_forks += 1
                
                fork_details.append(fork_info)
            
            print(f"   Total Forks: {total_forks}")
            print(f"   Active Forks (90 days): {active_forks}")
            print(f"   Recent Forks (30 days): {recent_forks}")
            
            # Show most starred forks
            if fork_details:
                starred_forks = [f for f in fork_details if f['stars'] > 0]
                if starred_forks:
                    starred_forks.sort(key=lambda x: x['stars'], reverse=True)
                    print(f"   Most Starred Forks:")
                    for fork in starred_forks[:3]:  # Show top 3
                        safe_print(f"     ⭐ {fork['name']} ({fork['stars']} stars)")
            
            repo_data.update({
                "fork_details": fork_details[:20],  # Store top 20 for space
                "active_forks": active_forks,
                "recent_forks": recent_forks
            })
        elif repo_data["forks"] > 0:
            safe_print(f"🍴 Fork Analysis: {repo_data['forks']} forks (details not accessible)")
        else:
            safe_print("🍴 Fork Analysis: No forks")
    except Exception as e:
        safe_print(f"🍴 Fork Analysis: Error processing fork data - {e}")
    
    try:
        # Get views traffic
        views = get_traffic_views(repo)
        if views:
            safe_print("📈 Views:")
            views_count = views.get('count', 0)
            views_uniques = views.get('uniques', 0)
            print(f"   Total: {views_count}, Unique: {views_uniques}")
            
            repo_data.update({
                "views_total": views_count,
                "views_unique": views_uniques
            })
            
            # Process daily views (extend to full 14 days)
            if 'views' in views and views['views']:
                from datetime import timezone
                past_24_hours = datetime.now(timezone.utc) - timedelta(days=1)
                print("   Daily breakdown (last 14 days):")
                
                # Sort by date and show all available days (up to 14)
                all_views = sorted(views['views'], key=lambda x: x['timestamp'], reverse=True)[:14]
                for day in all_views:
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
            
            # Calculate clone-to-pull ratio estimate
            clone_pull_ratio = 0
            if clones_uniques > 0:
                clone_pull_ratio = clones_count / clones_uniques
            
            print(f"   Total: {clones_count}, Unique: {clones_uniques}")
            print(f"   Clone/Pull Ratio: {clone_pull_ratio:.1f}x (estimated pulls per unique user)")
            
            repo_data.update({
                "clones_total": clones_count,
                "clones_unique": clones_uniques,
                "clone_pull_ratio": clone_pull_ratio
            })
            
            # Process daily clones (extend to full 14 days)
            if 'clones' in clones and clones['clones']:
                from datetime import timezone
                past_48_hours = datetime.now(timezone.utc) - timedelta(days=2)
                print("   Daily breakdown (last 14 days):")
                
                # Sort by date and show all available days (up to 14)
                all_clones = sorted(clones['clones'], key=lambda x: x['timestamp'], reverse=True)[:14]
                total_daily_clones = 0
                total_daily_unique = 0
                
                for day in all_clones:
                    day_date = datetime.fromisoformat(day['timestamp'].replace('Z', '+00:00'))
                    date_str = day_date.strftime("%b %d")
                    count = day.get('count', 0)
                    uniques = day.get('uniques', 0)
                    
                    total_daily_clones += count
                    total_daily_unique += uniques
                    
                    if count > 0:
                        daily_ratio = count / uniques if uniques > 0 else 0
                        indicator = " ⭐" if day_date > past_48_hours else ""
                        print(f"   {date_str}: {count} clones ({uniques} unique, {daily_ratio:.1f}x ratio){indicator}")
                    
                    repo_data["daily_clones"].append({
                        "date": day_date.strftime("%Y-%m-%d"),
                        "clones": count,
                        "unique_clones": uniques,
                        "clone_pull_ratio": daily_ratio
                    })
                
                # Show pull activity insights
                if total_daily_unique > 0:
                    avg_ratio = total_daily_clones / total_daily_unique
                    if avg_ratio > 2.0:
                        print(f"   📈 High pull activity detected! Average {avg_ratio:.1f} clones per user suggests frequent pulls")
                    elif avg_ratio > 1.5:
                        print(f"   📊 Moderate pull activity. Average {avg_ratio:.1f} clones per user")
                    else:
                        print(f"   � Mostly fresh clones. Average {avg_ratio:.1f} clones per user")
        else:
            print("�📦 Clones: Access denied or repository not found")
    except Exception as e:
        print(f"📦 Clones: Error processing clones data - {e}")
    
    # Analyze commit activity to correlate with clone patterns
    try:
        commits = get_repo_commits(repo, days=30)
        if commits and isinstance(commits, list):
            recent_commits = len(commits)
            commit_frequency = recent_commits / 30.0  # commits per day
            
            print(f"🔄 Recent Activity (30 days):")
            print(f"   Commits: {recent_commits} ({commit_frequency:.1f}/day)")
            
            repo_data.update({
                "recent_commits": recent_commits,
                "commit_frequency": commit_frequency
            })
            
            # Correlate commit activity with clone patterns
            if recent_commits > 20 and repo_data.get("clone_pull_ratio", 0) > 2.0:
                print(f"   🔥 Active development + high clone ratio suggests frequent pulls for updates!")
            elif recent_commits > 10 and repo_data.get("clone_pull_ratio", 0) > 1.5:
                print(f"   📈 Moderate development activity correlates with pull patterns")
            elif recent_commits < 5:
                print(f"   📋 Low commit activity - clones likely for browsing/forking")
        else:
            print(f"🔄 Recent Activity: Access limited or no recent commits")
    except Exception as e:
        print(f"🔄 Recent Activity: Error processing commit data - {e}")
    
    print()
    return repo_data

def generate_html_chart(current_run, stats_history):
    """Generate HTML chart using template with complete historical data."""
    print("📊 Generating HTML chart...")
    
    # Use the improved historical data merging
    daily_aggregates = merge_historical_daily_data(stats_history)
    
    print(f"📈 Total historical data spans {len(daily_aggregates)} days")
    
    # Prepare chart data from all historical data
    chart_data = {
        "labels": [],
        "datasets": [
            {
                "label": "Total Views",
                "data": [],
                "borderColor": "rgb(75, 192, 192)",
                "backgroundColor": "rgba(75, 192, 192, 0.1)",
                "tension": 0.1,
                "order": 2
            },
            {
                "label": "Unique Views", 
                "data": [],
                "borderColor": "rgb(255, 99, 132)",
                "backgroundColor": "rgba(255, 99, 132, 0.1)",
                "tension": 0.1,
                "order": 2
            },
            {
                "label": "Total Clones",
                "data": [],
                "borderColor": "rgb(54, 162, 235)",
                "backgroundColor": "rgba(54, 162, 235, 0.1)",
                "tension": 0.1,
                "order": 2
            },
            {
                "label": "Unique Clones",
                "data": [],
                "borderColor": "rgb(255, 206, 86)",
                "backgroundColor": "rgba(255, 206, 86, 0.1)",
                "tension": 0.1,
                "order": 2
            },
            {
                "label": "Total Stars",
                "data": [],
                "borderColor": "rgb(153, 102, 255)",
                "backgroundColor": "rgba(153, 102, 255, 0.1)",
                "tension": 0.1,
                "order": 2
            },
            {
                "label": "Total Forks",
                "data": [],
                "borderColor": "rgb(255, 159, 64)",
                "backgroundColor": "rgba(255, 159, 64, 0.1)",
                "tension": 0.1,
                "order": 2
            },
            {
                "label": "Active Forks",
                "data": [],
                "borderColor": "rgb(199, 199, 199)",
                "backgroundColor": "rgba(199, 199, 199, 0.1)",
                "tension": 0.1,
                "order": 2
            }
        ]
    }
    
    # Sort dates and use ALL available historical data (not limited to 30 days)
    sorted_dates = sorted(daily_aggregates.keys())
    
    for date in sorted_dates:
        chart_data["labels"].append(date)
        chart_data["datasets"][0]["data"].append(daily_aggregates[date]["views"])
        chart_data["datasets"][1]["data"].append(daily_aggregates[date]["unique_views"])
        chart_data["datasets"][2]["data"].append(daily_aggregates[date]["clones"])
        chart_data["datasets"][3]["data"].append(daily_aggregates[date]["unique_clones"])
        chart_data["datasets"][4]["data"].append(daily_aggregates[date]["stars"])
        chart_data["datasets"][5]["data"].append(daily_aggregates[date]["forks"])
        chart_data["datasets"][6]["data"].append(daily_aggregates[date]["active_forks"])
    
    print(f"📈 Chart includes {len(sorted_dates)} days of data (last 14 shown below):")
    for date in sorted_dates[-14:]:  # Show last 14 days in console
        agg = daily_aggregates[date]
        print(f"   {date}: {agg['views']} views ({agg['unique_views']} unique), {agg['clones']} clones ({agg['unique_clones']} unique)")
    
    # Calculate trend slopes
    slope_data = {}
    for metric in ['views', 'unique_views', 'clones', 'unique_clones', 'stars', 'forks', 'active_forks']:
        slope, r_squared, days = calculate_trend_slope(daily_aggregates, metric)
        slope_data[metric] = {
            'slope': slope,
            'r_squared': r_squared,
            'days': days
        }
        if slope is not None:
            print(f"📈 {metric.replace('_', ' ').title()} trend: {slope:.2f} per day (R²={r_squared:.3f}, {days} days)")
    
    # Save slope data
    slope_history = load_slope_history()
    slope_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "slopes": slope_data
    }
    slope_history.append(slope_entry)
    save_slope_history(slope_history)
    
    # Read template and replace placeholders
    try:
        with open(HTML_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print(f"❌ HTML template not found: {HTML_TEMPLATE_FILE}")
        return
    
    update_time = datetime.now().strftime("%B %d, %Y %H:%M")
    chart_data_json = json.dumps(chart_data)
    repo_data_json = json.dumps(current_run["repositories"])
    
    # Prepare slope information for HTML
    slope_info = ""
    for metric, data in slope_data.items():
        if data['slope'] is not None:
            trend_direction = "📈" if data['slope'] > 0 else "📉" if data['slope'] < 0 else "➡️"
            slope_info += f"<p>{trend_direction} <strong>{metric.replace('_', ' ').title()}</strong>: {data['slope']:.2f} per day (R²={data['r_squared']:.3f})</p>"
    
    # Replace placeholders
    html = html_template.replace('{{UPDATE_TIME}}', update_time)
    html = html.replace('{{TOTAL_VIEWS}}', str(current_run["totals"]["views"]))
    html = html.replace('{{UNIQUE_VIEWS}}', str(current_run["totals"]["unique_views"]))
    html = html.replace('{{TOTAL_CLONES}}', str(current_run["totals"]["clones"]))
    html = html.replace('{{UNIQUE_CLONES}}', str(current_run["totals"]["unique_clones"]))
    html = html.replace('{{TOTAL_STARS}}', str(current_run["totals"]["stars"]))
    html = html.replace('{{TOTAL_FORKS}}', str(current_run["totals"]["forks"]))
    html = html.replace('{{ACTIVE_FORKS}}', str(current_run["totals"]["active_forks"]))
    html = html.replace('{{RECENT_FORKS}}', str(current_run["totals"]["recent_forks"]))
    html = html.replace('{{CHART_DATA}}', chart_data_json)
    html = html.replace('{{REPO_DATA}}', repo_data_json)
    html = html.replace('{{SLOPE_INFO}}', slope_info)
    html = html.replace('{{TOTAL_DAYS}}', str(len(sorted_dates)))
    
    # Write HTML file
    try:
        with open(HTML_CHART_FILE, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML chart generated: {HTML_CHART_FILE}")
        print(f"🌐 Chart now shows {len(sorted_dates)} days of historical data with trend analysis")
    except IOError as e:
        print(f"Error writing HTML file: {e}")

def main():
    """Main function."""
    safe_print("🚀 GitHub Traffic Stats Collection Tool")
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
            "active_forks": 0,
            "recent_forks": 0,
            "repositories_count": len(REPOS)
        }
    }
    
    # Process each repository
    total_repos = len(REPOS)
    for i, repo in enumerate(REPOS, 1):
        safe_print(f"📊 Processing repository {i}/{total_repos}: {repo}")
        try:
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
            current_run["totals"]["active_forks"] += repo_data["active_forks"]
            current_run["totals"]["recent_forks"] += repo_data["recent_forks"]
            
            safe_print(f"✅ Completed {repo} ({i}/{total_repos})")
            
            # Small delay to avoid rate limiting
            if i < total_repos:  # Don't delay after the last repository
                time.sleep(0.5)
            
        except Exception as e:
            safe_print(f"❌ Error processing {repo}: {e}")
            # Create minimal repo data to continue processing
            current_run["repositories"][repo] = {
                "name": repo,
                "stars": 0, "watchers": 0, "forks": 0,
                "fork_details": [], "active_forks": 0, "recent_forks": 0,
                "views_total": 0, "views_unique": 0,
                "clones_total": 0, "clones_unique": 0,
                "last_updated": "", "daily_views": [], "daily_clones": []
            }
    
    # Display summary
    totals = current_run["totals"]
    print("=== SUMMARY ===")
    print(f"Total Views: {totals['views']} (Unique: {totals['unique_views']})")
    print(f"Total Clones: {totals['clones']} (Unique: {totals['unique_clones']})")
    print("\nRepository Engagement:")
    print(f"Total Stars: {totals['stars']}")
    print(f"Total Watchers: {totals['watchers']}")
    print(f"Total Forks: {totals['forks']}")
    print(f"Active Forks (90 days): {totals['active_forks']}")
    print(f"Recent Forks (30 days): {totals['recent_forks']}")
    if totals['forks'] > 0:
        activity_rate = (totals['active_forks'] / totals['forks']) * 100
        print(f"Fork Activity Rate: {activity_rate:.1f}%")
    print(f"Repositories Checked: {totals['repositories_count']}")
    print()
    safe_print("🔥 indicates activity within the past 24 hours")
    print("Note: GitHub Traffic API provides data for the past 14 days maximum")
    
    # Save stats history with deduplication
    # Remove any existing entry for today's date to avoid duplicates
    current_date = current_run["date"]
    stats_history = [entry for entry in stats_history if entry.get("date") != current_date]
    
    # Add today's run
    stats_history.append(current_run)
    save_stats_history(stats_history)
    
    # Generate HTML chart
    generate_html_chart(current_run, stats_history)
    
    # Git commit and push updated results
    git_commit_and_push()

def git_commit_and_push():
    """Commit and push the updated traffic stats and chart to git repository."""
    try:
        print("\n🔄 Committing and pushing updated traffic analytics...")
        
        # Get current timestamp for commit message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add all files
        result = subprocess.run(['git', 'add', 'traffic_stats_history.ndjson', 'traffic_stats_chart.html', 'traffic_slope_history.json'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Git add warning: {result.stderr}")
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("📝 No changes to commit - traffic data unchanged")
            return
        
        # Commit changes
        commit_message = f"Auto-update traffic analytics - {timestamp}\n\nUpdated traffic statistics and interactive chart with latest GitHub data"
        result = subprocess.run(['git', 'commit', '-m', commit_message], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Git commit failed: {result.stderr}")
            return
        
        print("✅ Changes committed successfully")
        
        # Push to remote
        result = subprocess.run(['git', 'push'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Git push failed: {result.stderr}")
            print("💡 You may need to manually push or check your git configuration")
            return
        
        print("🚀 Changes pushed to remote repository successfully")
        
    except Exception as e:
        print(f"❌ Git operations failed: {e}")
        print("💡 Continuing without git operations...")

if __name__ == "__main__":
    main()
