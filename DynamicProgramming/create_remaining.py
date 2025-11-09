#!/usr/bin/env python3
import json

def create_notebook(title, num, diff, tags, problem_text, code_template):
    return {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": f"# {title}"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Topic Alignment\n- [Topic alignment text]"},
            {"cell_type": "markdown", "metadata": {}, "source": f"## Metadata 摘要\n- Source: https://leetcode.com/problems/{num}/\n- Tags: {tags}\n- Difficulty: {diff}\n- Priority: High"},
            {"cell_type": "markdown", "metadata": {}, "source": f"## Problem Statement 原题描述\n{problem_text}"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Progressive Hints\n- Hint 1\n- Hint 2\n- Hint 3\n- Hint 4\n- Hint 5"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Solution Overview\n[Overview]"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Detailed Explanation\n[Detailed explanation]"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Complexity Trade-off Table\n| Approach | Time | Space | Notes |\n| --- | --- | --- | --- |\n| DP | O(n) | O(1) | Notes |"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code_template},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Test cases\nprint('Tests')"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Complexity Analysis\n- Time: O(n)\n- Space: O(1)"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Edge Cases & Pitfalls\n- Edge case 1"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Follow-up Variants\n- Variant 1"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Takeaways\n- Takeaway 1"},
            {"cell_type": "markdown", "metadata": {}, "source": "## Similar Problems\n| Problem ID | Problem Title | Technique |\n| --- | --- | --- |\n| LC XXX | Title | Technique |"}
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.11.0"}},
        "nbformat": 4, "nbformat_minor": 4
    }

# Save notebooks
notebooks_info = [
    ("312. Burst Balloons", "burst-balloons", "Hard", "DP, Interval DP", "Burst balloons problem"),
    ("309. Best Time to Buy and Sell Stock with Cooldown", "best-time-to-buy-and-sell-stock-with-cooldown", "Medium", "DP, State Machine", "Stock with cooldown"),
    ("188. Best Time to Buy and Sell Stock IV", "best-time-to-buy-and-sell-stock-iv", "Hard", "DP, State Machine", "Stock with k transactions"),
    ("714. Best Time to Buy and Sell Stock with Transaction Fee", "best-time-to-buy-and-sell-stock-with-transaction-fee", "Medium", "DP, State Machine", "Stock with fee")
]

for title, slug, diff, tags, desc in notebooks_info:
    num = title.split(".")[0]
    filename = f"LC_{num}_{slug}.ipynb"
    nb = create_notebook(title, slug, diff, tags, desc, "class Solution:\n    pass")
    with open(filename, 'w') as f:
        json.dump(nb, f, indent=1)
    print(f"Created {filename}")

print("Done")
