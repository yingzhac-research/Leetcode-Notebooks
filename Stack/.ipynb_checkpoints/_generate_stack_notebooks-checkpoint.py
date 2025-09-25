import json
from pathlib import Path

NOTEBOOK_METADATA = {
    "kernelspec": {
        "display_name": "Python 3 (ipykernel)",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.13.3",
    },
}


def to_source(text: str):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines(True)
    if not lines:
        return ["\n"]
    if not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def md_cell(text: str):
    return {"cell_type": "markdown", "metadata": {}, "source": to_source(text)}


def code_cell(text: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": to_source(text),
    }


PROBLEMS = []  # TODO: populate with problem dictionaries


def build_notebook(problem):
    cells = []
    cells.append(md_cell(f"# {problem['id']}. {problem['title']}"))
    cells.append(md_cell("## Topic Alignment\n" + problem["topic_alignment"]))
    cells.append(md_cell("## Metadata Summary\n" + problem["metadata_summary"]))
    cells.append(md_cell("## Problem Statement\n" + problem["problem_statement"]))
    cells.append(md_cell("## Progressive Hints\n" + problem["progressive_hints"]))
    cells.append(md_cell("## Solution Overview\n" + problem["solution_overview"]))
    cells.append(md_cell("## Detailed Explanation\n" + problem["detailed_explanation"]))
    cells.append(md_cell("## Complexity Trade-off Table\n" + problem["tradeoffs_table"]))
    cells.append(md_cell("## Reference Implementation"))
    cells.append(code_cell(problem["reference_implementation"]))
    cells.append(md_cell("## Validation"))
    cells.append(code_cell(problem["validation_snippet"]))
    cells.append(md_cell("## Complexity Analysis\n" + problem["complexity_analysis"]))
    cells.append(md_cell("## Edge Cases & Pitfalls\n" + problem["edge_cases"]))
    cells.append(md_cell("## Follow-up Variants\n" + problem["follow_ups"]))
    cells.append(md_cell("## Takeaways\n" + problem["takeaways"]))
    cells.append(md_cell("## Similar Problems\n" + problem["similar_problems_table"]))

    nb_json = {
        "cells": cells,
        "metadata": NOTEBOOK_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    filename = f"Stack/LC_{problem['id']}_{problem['slug']}.ipynb"
    Path(filename).write_text(json.dumps(nb_json, indent=2, ensure_ascii=False))
    print(f"Wrote {filename}")


def main():
    for prob in PROBLEMS:
        build_notebook(prob)


if __name__ == "__main__":
    main()
