import os
import re
from collections import Counter


ROOT = os.getcwd()


# ---------------------------------------------------------
# FIND ALL ORGANIZED PROBLEMS
# ---------------------------------------------------------

def find_problem_folders():
    """
    Recursively find all organized LeetCode problem folders.

    Supported structures:

    algorithms/
        arrays/
            0001-two-sum/
            0121-best-time-to-buy-and-sell-stock/
            0217-contains-duplicate/

    database/
        sql/
            0175-combine-two-tables/

    shell/
        0192-word-frequency/

    pandas/
        0179-largest-number/

    concurrency/
        1226-the-dining-philosophers/

    Returns a list of dictionaries containing:
        path
        category
        name
    """

    problems = []

    # -----------------------------------------------------
    # Scan algorithms recursively
    # -----------------------------------------------------

    algorithms_path = os.path.join(
        ROOT,
        "algorithms"
    )

    if os.path.exists(algorithms_path):

        for current_root, dirs, files in os.walk(
            algorithms_path
        ):

            problem_dirs = []

            for directory in dirs:

                if re.match(
                    r"^\d+-",
                    directory
                ):

                    problem_dirs.append(
                        directory
                    )

            for directory in problem_dirs:

                problem_path = os.path.join(
                    current_root,
                    directory
                )

                # Determine the algorithm category.
                relative_path = os.path.relpath(
                    problem_path,
                    algorithms_path
                ).replace(
                    os.sep,
                    "/"
                )

                parts = relative_path.split("/")

                if len(parts) >= 2:
                    category = parts[0]
                else:
                    category = "other"

                problems.append({
                    "path": problem_path,
                    "category": category,
                    "name": directory
                })

            # Do not search inside an already detected
            # problem folder.
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in problem_dirs
            ]

    # -----------------------------------------------------
    # Scan database recursively
    # -----------------------------------------------------

    database_path = os.path.join(
        ROOT,
        "database"
    )

    if os.path.exists(database_path):

        for current_root, dirs, files in os.walk(
            database_path
        ):

            problem_dirs = []

            for directory in dirs:

                if re.match(
                    r"^\d+-",
                    directory
                ):

                    problem_dirs.append(
                        directory
                    )

            for directory in problem_dirs:

                problem_path = os.path.join(
                    current_root,
                    directory
                )

                problems.append({
                    "path": problem_path,
                    "category": "database",
                    "name": directory
                })

            # Do not search inside problem folders.
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in problem_dirs
            ]

    # -----------------------------------------------------
    # Scan Shell / Pandas / Concurrency / Other recursively
    # -----------------------------------------------------

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

        for current_root, dirs, files in os.walk(
            category_path
        ):

            problem_dirs = []

            for directory in dirs:

                if re.match(
                    r"^\d+-",
                    directory
                ):

                    problem_dirs.append(
                        directory
                    )

            for directory in problem_dirs:

                problem_path = os.path.join(
                    current_root,
                    directory
                )

                problems.append({
                    "path": problem_path,
                    "category": category,
                    "name": directory
                })

            # Do not search inside problem folders.
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in problem_dirs
            ]

    # -----------------------------------------------------
    # Remove duplicate problem paths
    # -----------------------------------------------------

    unique_problems = {}

    for problem in problems:

        normalized_path = os.path.normpath(
            problem["path"]
        )

        unique_problems[
            normalized_path
        ] = problem

    return list(
        unique_problems.values()
    )


# ---------------------------------------------------------
# READ PROBLEM README
# ---------------------------------------------------------

def read_problem_metadata(problem):
    """
    Read metadata from a problem README.

    Expected format:

    **Difficulty:** Easy

    **Primary Pattern:** Hash Table
    """

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

    try:

        with open(
            readme_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except OSError as error:

        print(
            f"Could not read {readme_path}: {error}"
        )

        return metadata

    # -----------------------------------------------------
    # Difficulty
    # -----------------------------------------------------

    match = re.search(
        r"\*\*Difficulty:\*\*\s*(.+)",
        content
    )

    if match:

        metadata["difficulty"] = (
            match.group(1).strip()
        )

    # -----------------------------------------------------
    # Primary Pattern
    # -----------------------------------------------------

    match = re.search(
        r"\*\*Primary Pattern:\*\*\s*(.+)",
        content
    )

    if match:

        metadata["pattern"] = (
            match.group(1).strip()
        )

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

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
# GET PROBLEM NUMBER
# ---------------------------------------------------------

def get_problem_number(problem_name):
    """
    Extract numeric LeetCode problem number.

    Examples:

        0001-two-sum
        -> 1

        0121-best-time-to-buy-and-sell-stock
        -> 121

        0217-contains-duplicate
        -> 217
    """

    match = re.match(
        r"^(\d+)-",
        problem_name
    )

    if not match:
        return 0

    return int(
        match.group(1)
    )


# ---------------------------------------------------------
# GENERATE DASHBOARD
# ---------------------------------------------------------

def generate_dashboard(problems):

    difficulty_counter = Counter()
    pattern_counter = Counter()
    category_counter = Counter()

    # -----------------------------------------------------
    # Collect statistics
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Difficulty
    # -----------------------------------------------------

    total = len(problems)

    easy = difficulty_counter[
        "Easy"
    ]

    medium = difficulty_counter[
        "Medium"
    ]

    hard = difficulty_counter[
        "Hard"
    ]

    # -----------------------------------------------------
    # Patterns
    # -----------------------------------------------------

    pattern_rows = ""

    for pattern, count in (
        pattern_counter.most_common()
    ):

        pattern_rows += (
            f"| {pattern} | {count} |\n"
        )

    if not pattern_rows:

        pattern_rows = (
            "| No problems yet | 0 |\n"
        )

    # -----------------------------------------------------
    # Categories
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

        category_rows = (
            "| No problems yet | 0 |\n"
        )

    # -----------------------------------------------------
    # Recent Problems
    # -----------------------------------------------------

    recent = sorted(
        problems,
        key=lambda problem: get_problem_number(
            problem["name"]
        ),
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

    # -----------------------------------------------------
    # Build dashboard
    # -----------------------------------------------------

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

        print(
            "README.md not found."
        )

        return

    try:

        with open(
            readme_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except OSError as error:

        print(
            f"Could not read README.md: {error}"
        )

        return

    start_marker = (
        "<!-- AUTO-DASHBOARD-START -->"
    )

    end_marker = (
        "<!-- AUTO-DASHBOARD-END -->"
    )

    block = (
        f"{start_marker}\n"
        f"{dashboard}"
        f"{end_marker}"
    )

    pattern = (
        re.escape(start_marker)
        + r".*?"
        + re.escape(end_marker)
    )

    # -----------------------------------------------------
    # Replace existing dashboard
    # -----------------------------------------------------

    if re.search(
        pattern,
        content,
        flags=re.DOTALL
    ):

        content = re.sub(
            pattern,
            block,
            content,
            flags=re.DOTALL
        )

    # -----------------------------------------------------
    # Create dashboard if missing
    # -----------------------------------------------------

    else:

        content += (
            "\n\n"
            + block
            + "\n"
        )

    try:

        with open(
            readme_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

    except OSError as error:

        print(
            f"Could not write README.md: {error}"
        )

        return

    print(
        "Progress dashboard updated successfully."
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print(
        "Scanning organized LeetCode problems..."
    )

    problems = find_problem_folders()

    print(
        f"Found {len(problems)} organized problems."
    )

    # -----------------------------------------------------
    # Print detected problems
    # -----------------------------------------------------

    for problem in sorted(
        problems,
        key=lambda problem: get_problem_number(
            problem["name"]
        )
    ):

        print(
            f"  {problem['name']} "
            f"-> {problem['category']}"
        )

    # -----------------------------------------------------
    # Generate dashboard
    # -----------------------------------------------------

    dashboard = generate_dashboard(
        problems
    )

    # -----------------------------------------------------
    # Update README
    # -----------------------------------------------------

    update_readme(
        dashboard
    )


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
