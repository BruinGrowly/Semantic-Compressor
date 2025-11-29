#!/usr/bin/env python3
"""
Code Evolution Visualizer
=========================

Visualize how code evolves through semantic space over time.

Creates:
- Timeline chart showing L/J/P/W over commits
- Health score trajectory
- Distance from Natural Equilibrium over time
- Semantic velocity (rate of change)
- Export to HTML for interactive viewing

Usage:
    python evolution_visualizer.py <file> --output evolution.html
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.ljpw.ljpw_standalone import analyze_quick, calculate_distance

# Natural Equilibrium
NATURAL_EQUILIBRIUM = (0.618, 0.414, 0.718, 0.693)


def get_genome(result):
    """Create genome from LJPW result"""
    L = result["ljpw"]["L"]
    J = result["ljpw"]["J"]
    P = result["ljpw"]["P"]
    W = result["ljpw"]["W"]

    L_digit = int(round(L * 10)) % 10
    J_digit = int(round(J * 10)) % 10
    P_digit = int(round(P * 10)) % 10
    W_digit = int(round(W * 10)) % 10

    return f"L{L_digit}J{J_digit}P{P_digit}W{W_digit}"


def calculate_health(coords):
    """Calculate health score (0-100)"""
    max_distance = 2.0
    dist = calculate_distance(coords, NATURAL_EQUILIBRIUM)
    return max(0, 100 * (1 - dist / max_distance))


def get_git_history(filepath, num_commits=50):
    """Get git history for file"""
    try:
        result = subprocess.run(
            ["git", "log", f"-{num_commits}", "--format=%H|%ai|%s", "--", filepath],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return []


def get_git_file_content(commit, filepath):
    """Get file content at commit"""
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{filepath}"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except:
        return None


def analyze_evolution(filepath, num_commits=50):
    """Analyze code evolution over git history"""
    print(f"Analyzing evolution of {filepath}...")
    print(f"Fetching last {num_commits} commits...\n")

    commits = get_git_history(filepath, num_commits)

    if not commits or commits[0] == "":
        print(f"No git history found for {filepath}")
        return []

    evolution = []

    for i, commit_line in enumerate(commits):
        if not commit_line.strip():
            continue

        parts = commit_line.split("|")
        if len(parts) < 3:
            continue

        commit_hash, commit_date, commit_msg = parts[0], parts[1], "|".join(parts[2:])

        # Get code at this commit
        code = get_git_file_content(commit_hash, filepath)
        if not code or not code.strip():
            continue

        # Analyze
        try:
            result = analyze_quick(code)
            l = result["ljpw"]["L"]
            j = result["ljpw"]["J"]
            p = result["ljpw"]["P"]
            w = result["ljpw"]["W"]

            coords = (l, j, p, w)
            genome = get_genome(result)
            dist_to_ne = calculate_distance(coords, NATURAL_EQUILIBRIUM)
            health = calculate_health(coords)

            evolution.append(
                {
                    "commit": commit_hash[:7],
                    "date": commit_date,
                    "message": commit_msg[:60],
                    "L": l,
                    "J": j,
                    "P": p,
                    "W": w,
                    "genome": genome,
                    "dist_ne": dist_to_ne,
                    "health": health,
                    "loc": len(code.split("\n")),
                }
            )

            print(f"  [{i+1}/{len(commits)}] {commit_hash[:7]} - {health:.1f}/100")

        except Exception as e:
            print(f"  [{i+1}/{len(commits)}] {commit_hash[:7]} - Error: {e}")
            continue

    return list(reversed(evolution))  # Chronological order


def generate_html(evolution, filepath, output_file):
    """Generate interactive HTML visualization"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Evolution: {filepath}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }}
        h1 {{
            color: #4fc3f7;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .chart-container {{
            background: #2d2d2d;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        canvas {{
            max-height: 400px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #2d2d2d;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4fc3f7;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #4fc3f7;
        }}
        .stat-label {{
            font-size: 12px;
            color: #9e9e9e;
            text-transform: uppercase;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #2d2d2d;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #404040;
        }}
        th {{
            background: #1a1a1a;
            color: #4fc3f7;
        }}
        tr:hover {{
            background: #353535;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 Code Evolution Analysis</h1>
        <h2>{filepath}</h2>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(evolution)}</div>
                <div class="stat-label">Commits Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{evolution[-1]['genome'] if evolution else 'N/A'}</div>
                <div class="stat-label">Current Genome</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{evolution[-1]['health']:.1f}/100</div>
                <div class="stat-label">Current Health</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{(evolution[-1]['health'] - evolution[0]['health']):.1f}</div>
                <div class="stat-label">Health Change</div>
            </div>
        </div>

        <div class="chart-container">
            <h3>4D Coordinates Over Time</h3>
            <canvas id="coordsChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Health Score Trajectory</h3>
            <canvas id="healthChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Distance from Natural Equilibrium</h3>
            <canvas id="neChart"></canvas>
        </div>

        <h3>Commit History</h3>
        <table>
            <thead>
                <tr>
                    <th>Commit</th>
                    <th>Date</th>
                    <th>Genome</th>
                    <th>Health</th>
                    <th>Dist NE</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
"""

    for e in reversed(evolution):  # Most recent first
        html += f"""
                <tr>
                    <td>{e['commit']}</td>
                    <td>{e['date'][:10]}</td>
                    <td>{e['genome']}</td>
                    <td>{e['health']:.1f}/100</td>
                    <td>{e['dist_ne']:.3f}</td>
                    <td>{e['message']}</td>
                </tr>
"""

    # Prepare data for charts
    labels = [f"{e['commit']}" for e in evolution]
    l_data = [e["L"] for e in evolution]
    j_data = [e["J"] for e in evolution]
    p_data = [e["P"] for e in evolution]
    w_data = [e["W"] for e in evolution]
    health_data = [e["health"] for e in evolution]
    ne_data = [e["dist_ne"] for e in evolution]

    html += f"""
            </tbody>
        </table>
    </div>

    <script>
        // 4D Coordinates Chart
        new Chart(document.getElementById('coordsChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [
                    {{
                        label: 'Love (L)',
                        data: {json.dumps(l_data)},
                        borderColor: '#ff6b6b',
                        backgroundColor: 'rgba(255, 107, 107, 0.1)',
                        tension: 0.3
                    }},
                    {{
                        label: 'Justice (J)',
                        data: {json.dumps(j_data)},
                        borderColor: '#4ecdc4',
                        backgroundColor: 'rgba(78, 205, 196, 0.1)',
                        tension: 0.3
                    }},
                    {{
                        label: 'Power (P)',
                        data: {json.dumps(p_data)},
                        borderColor: '#ffe66d',
                        backgroundColor: 'rgba(255, 230, 109, 0.1)',
                        tension: 0.3
                    }},
                    {{
                        label: 'Wisdom (W)',
                        data: {json.dumps(w_data)},
                        borderColor: '#a8dadc',
                        backgroundColor: 'rgba(168, 218, 220, 0.1)',
                        tension: 0.3
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        labels: {{ color: '#e0e0e0' }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: '#404040' }},
                        ticks: {{ color: '#e0e0e0' }}
                    }},
                    x: {{
                        grid: {{ color: '#404040' }},
                        ticks: {{ color: '#e0e0e0', maxRotation: 45 }}
                    }}
                }}
            }}
        }});

        // Health Chart
        new Chart(document.getElementById('healthChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Health Score',
                    data: {json.dumps(health_data)},
                    borderColor: '#4fc3f7',
                    backgroundColor: 'rgba(79, 195, 247, 0.2)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        labels: {{ color: '#e0e0e0' }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        grid: {{ color: '#404040' }},
                        ticks: {{ color: '#e0e0e0' }}
                    }},
                    x: {{
                        grid: {{ color: '#404040' }},
                        ticks: {{ color: '#e0e0e0', maxRotation: 45 }}
                    }}
                }}
            }}
        }});

        // NE Distance Chart
        new Chart(document.getElementById('neChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Distance from NE',
                    data: {json.dumps(ne_data)},
                    borderColor: '#f06292',
                    backgroundColor: 'rgba(240, 98, 146, 0.2)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        labels: {{ color: '#e0e0e0' }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: '#404040' }},
                        ticks: {{ color: '#e0e0e0' }}
                    }},
                    x: {{
                        grid: {{ color: '#404040' }},
                        ticks: {{ color: '#e0e0e0', maxRotation: 45 }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(output_file, "w") as f:
        f.write(html)

    print(f"\n✓ Visualization saved to {output_file}")
    print(f"  Open in browser to see interactive charts")


def main():
    parser = argparse.ArgumentParser(description="Code Evolution Visualizer")
    parser.add_argument("file", help="File to analyze")
    parser.add_argument("--commits", type=int, default=50, help="Number of commits")
    parser.add_argument("--output", default="evolution.html", help="Output HTML file")

    args = parser.parse_args()

    evolution = analyze_evolution(args.file, args.commits)

    if not evolution:
        print("No evolution data to visualize")
        return

    print(f"\n{'='*70}")
    print("EVOLUTION SUMMARY")
    print("=" * 70)
    print(f"File: {args.file}")
    print(f"Commits: {len(evolution)}")
    print(f"Date range: {evolution[0]['date'][:10]} → {evolution[-1]['date'][:10]}")
    print(f"\nFirst commit ({evolution[0]['commit']}):")
    print(f"  Genome: {evolution[0]['genome']}")
    print(f"  Health: {evolution[0]['health']:.1f}/100")
    print(f"\nLatest commit ({evolution[-1]['commit']}):")
    print(f"  Genome: {evolution[-1]['genome']}")
    print(f"  Health: {evolution[-1]['health']:.1f}/100")
    print(f"\nHealth change: {evolution[-1]['health'] - evolution[0]['health']:+.1f} points")

    # Generate HTML
    generate_html(evolution, args.file, args.output)


if __name__ == "__main__":
    main()
