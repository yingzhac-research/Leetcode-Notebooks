# Interview Notebook Workspace

This repository tracks structured interview prep notebooks organized by topic. Each topic folder contains LeetCode-focused Jupyter notebooks that follow a shared authoring template and validation workflow.

## Repository Layout
- `BinarySearch/` – search-space reduction patterns, guides, and notebooks.
- `BFS/`, `DFS/`, `Tree/` – graph and tree traversal techniques.
- `Stack/`, `Queue/`, `HashTable/` – core data-structure drills and references.
- `TwoPointers/` – variable-window, opposing-pointer, and related techniques with Chinese guides.
- `DP/`, `Greedy/` – placeholders for upcoming dynamic programming and greedy strategy notebooks.
- `guide_old.md`, `leetcode_notebook_rules.md` – shared writing standards and legacy guidance.

## Working With Notebooks
1. Create an isolated environment: `python -m venv .venv && source .venv/bin/activate`.
2. Open notebooks locally with `jupyter lab <Topic>/LC_<id>_<slug>.ipynb`.
3. Follow the template in `leetcode_notebook_rules.md` for title cells, metadata, analysis blocks, and validation cells.
4. Before committing, execute notebooks or run `jupyter nbconvert --execute <notebook>` to catch syntax issues.

## Contribution Conventions
- Use ASCII in Markdown and code comments unless a notebook already relies on other characters.
- Keep naming consistent: `LC_<problem-number>_<kebab-case-title>.ipynb` inside the appropriate topic directory.
- Add new topics by creating a top-level folder with the canonical English topic name, then author notebooks inside it.
- When the shared template changes, update `leetcode_notebook_rules.md` and any relevant topic guides in tandem.

## Next Steps
- Populate `DP/` and `Greedy/` with curated problem notebooks.
- Continue expanding guides so every topic directory links back to the shared rules.
