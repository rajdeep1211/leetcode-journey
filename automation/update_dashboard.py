import os
import re
from collections import Counter


ROOT = os.getcwd()


# ---------------------------------------------------------
# FIND ALL ORGANIZED PROBLEMS
# ---------------------------------------------------------

def find_problem_folders():

    problems = []

    algorithms_path = os.path.join(
        ROOT,
        "algorithms"
    )

    if os.path.exists(algorithms_path):

        for category in os.listdir(algorithms_path):

            category_path = os.path.join(
                algorithms_path,
                category
            )

            if not os.path.isdir(category_path):
                continue

            for problem in os.listdir(category_path):

                problem_path = os.path.join(
                    category_path,
                    problem
                )

                if not os.path.isdir(problem_path):
                    continue

                if re.match(r"^\d+-", problem):

                    problems.append({
                        "path": problem_path,
                        "category": category,
                        "name": problem
                    })


    # Database
    database_path = os.path.join(
        ROOT,
        "database"
    )

    if os.path.exists(database_path):

        for item in os.listdir(database_path):

            path = os.path.join(
                database_path,
                item
            )

            if os.path.isdir(path) and re.match(
                r"^\d+-",
                item
            ):

                problems.append({
                    "path": path,
                    "category": "database",
                    "name": item
                })


    # Other categories
    for category in [
        "shell",
        "pandas",
        "concurrency",
        "other"
    ]:

        category_path = os.path.join(
            ROOT,
            category
        )

        if not os.path.exists(category_path):
            continue

        for item in os.listdir(category_path):

            path = os.path.join(
                category_path,
                item
            )

            if os.path.isdir(path) and re.match(
                r"^\d+-",
                item
            ):

                problems.append({
                    "path": path,
                    "category": category,
                    "name": item
                })


    return problems


# ---------------------------------------------------------
# READ PROBLEM README
# ---------------------------------------------------------

def read_problem_metadata(problem):

    readme_path = os.path.join(
        problem["path"],
        "README.md"
    )

    metadata = {
        "difficulty": "Unknown",
        "pattern": "Unknown",
        "title": problem["name"]
    }

    if not os.path.exists(readme_path):
        return metadata

    with open(
        readme_path,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()


    # Difficulty
    match = re.search(
        r"\*\*Difficulty:\*\*\s*(.+)",
        content
    )

    if match:
        metadata["difficulty"] = (
            match.group(1).strip()
        )


    # Pattern
    match = re.search(
        r"\*\*Primary Pattern:\*\*\s*(.+)",
        content
    )

    if match:
        metadata["pattern"] = (
            match.group(1).strip()
        )


    # Title
    match = re.search(
        r"^#\s+(.+)$",
        content,
        re.MULTILINE
    )

    if match:
        metadata["title"] = (
            match.group(1).strip()
        )


    return metadata


# ---------------------------------------------------------
# GENERATE DASHBOARD
# ---------------------------------------------------------

def generate_dashboard(problems):

    difficulty_counter = Counter()
    pattern_counter = Counter()
    category_counter = Counter()

    for problem in problems:

        metadata = read_problem_metadata(
            problem
        )

        difficulty_counter[
            metadata["difficulty"]
        ] += 1

        pattern_counter[
            metadata["pattern"]
        ] += 1

        category_counter[
            problem["category"]
        ] += 1


    total = len(problems)

    easy = difficulty_counter["Easy"]
    medium = difficulty_counter["Medium"]
    hard = difficulty_counter["Hard"]


    # -----------------------------------------------------
    # TOP PATTERNS
    # -----------------------------------------------------

    pattern_rows = ""

    for pattern, count in pattern_counter.most_common():

        pattern_rows += (
            f"| {pattern} | {count} |\n"
        )


    if not pattern_rows:
        pattern_rows = "| No problems yet | 0 |\n"


    # -----------------------------------------------------
    # CATEGORIES
    # -----------------------------------------------------

    category_rows = ""

    for category, count in sorted(
        category_counter.items()
    ):

        display_name = category.replace(
            "-",
            " "
        ).title()

        category_rows += (
            f"| {display_name} | {count} |\n"
        )


    if not category_rows:
        category_rows = "| No problems yet | 0 |\n"


    # -----------------------------------------------------
    # RECENT PROBLEMS
    # -----------------------------------------------------

    recent = sorted(
        problems,
        key=lambda x: x["name"],
        reverse=True
    )[:10]


    recent_rows = ""

    for problem in recent:

        metadata = read_problem_metadata(
            problem
        )

        recent_rows += (
            f"| {metadata['title']} "
            f"| {metadata['difficulty']} "
            f"| {metadata['pattern']} |\n"
        )


    if not recent_rows:
        recent_rows = (
            "| No problems yet | - | - |\n"
        )


    dashboard = f"""
## 📊 Progress Dashboard

### Problems Solved

| Difficulty | Solved |
|---|---:|
| 🟢 Easy | {easy} |
| 🟡 Medium | {medium} |
| 🔴 Hard | {hard} |
| **Total** | **{total}** |

---

### 🧠 Problem Categories

| Category | Solved |
|---|---:|
{category_rows}

---

### 🔥 Patterns Practiced

| Pattern | Problems |
|---|---:|
{pattern_rows}

---

### 📝 Recent Problems

| Problem | Difficulty | Pattern |
|---|---|---|
{recent_rows}

---

> Statistics are automatically generated from the solutions in this repository.
"""


    return dashboard


# ---------------------------------------------------------
# UPDATE ROOT README
# ---------------------------------------------------------

def update_readme(dashboard):

    readme_path = os.path.join(
        ROOT,
        "README.md"
    )

    if not os.path.exists(readme_path):

        print("README.md not found.")

        return


    with open(
        readme_path,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()


    start_marker = (
        "<!-- AUTO-DASHBOARD-START -->"
    )

    end_marker = (
        "<!-- AUTO-DASHBOARD-END -->"
    )


    block = (
        f"{start_marker}\n"
        f"{dashboard}\n"
        f"{end_marker}"
    )


    pattern = (
        re.escape(start_marker)
        + r".*?"
        + re.escape(end_marker)
    )


    if re.search(
        pattern,
        content,
        re.DOTALL
    ):

        content = re.sub(
            pattern,
            block,
            content,
            flags=re.DOTALL
        )

    else:

        content += (
            "\n\n"
            + block
            + "\n"
        )


    with open(
        readme_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    problems = find_problem_folders()

    print(
        f"Found {len(problems)} organized problems."
    )

    dashboard = generate_dashboard(
        problems
    )

    update_readme(
        dashboard
    )

    print(
        "Dashboard updated successfully."
    )


if __name__ == "__main__":
    main()
