# Repository Guidelines

## Project Structure & Module Organization
The repository is organized by interview topic directories such as `HashTable` and `TwoPointers`. Each directory stores LeetCode-focused Jupyter notebooks named `LC_<problem-number>_<kebab-case-title>.ipynb`. When adding a new topic, create a top-level folder with the canonical English topic name before saving the notebook. Keep shared authoring rules in sync with `leetcode_notebook_rules.md` and reference it whenever the template evolves.

## Build, Test, and Development Commands
Work in an isolated Python environment to keep dependencies reproducible: `python -m venv .venv && source .venv/bin/activate`. Launch notebooks locally with `jupyter lab HashTable/LC_1_two-sum.ipynb` (or replace with your target path). Use `jupyter nbconvert --execute <notebook>` for a quick smoke run that catches syntax failures before commit.

## Coding Style & Naming Conventions
Notebook code defaults to Python 3. Follow the shared template: begin with a title cell `# <problem-number>. <Official Title>`, include the metadata, hints, and analysis blocks in order, and keep Markdown content in ASCII. Code cells should prefer descriptive helper names (`def find_window(...)`) and inline comments only for non-obvious logic. Reuse consistent section headings so downstream automation can parse them.

## Testing Guidelines
Every notebook must include a dedicated validation cell that exercises the reference implementation against edge, average, and stress cases. Prefer lightweight asserts such as:
```
tests = [...]
for args, expected in tests:
    assert solution(*args) == expected
```
Document additional manual checks (e.g., random test generators) in Markdown. If a problem lacks deterministic answers, describe the acceptance criterion and print representative samples.

## Commit & Pull Request Guidelines
The repository has no published git history; standardize on imperative messages scoped by topic, e.g., `HashTable: add LC 560 notebook`. PRs should summarize the algorithmic insight, list affected notebooks, and note validation evidence (executed notebooks, nbconvert run, screenshots if visual). Link to any tracked prep plan or issue ID so future reviewers know the study context.
