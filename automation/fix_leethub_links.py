import os
import re

ROOT = os.getcwd()

START_MARKER = "<!-- LEETHUB:TABLE:START -->"
END_MARKER = "<!-- LEETHUB:TABLE:END -->"

SEARCH_ROOTS = [
    "algorithms",
    "database",
    "shell",
    "pandas",
    "concurrency",
    "other",
]


def find_problem_paths():
    problem_paths = {}

    for search_root in SEARCH_ROOTS:
        root_path = os.path.join(ROOT, search_root)

        if not os.path.exists(root_path):
            continue

        for current_root, dirs, files in os.walk(root_path):
            for directory in dirs:

                if not re.match(r"^\d+-", directory):
                    continue

                match = re.match(r"^(\d+)-", directory)

                if not match:
                    continue

                problem_number = match.group(1)

                problem_path = os.path.join(
                    current_root,
                    directory
                )

                relative_path = os.path.relpath(
                    problem_path,
                    ROOT
                ).replace(os.sep, "/") + "/"

                problem_paths[problem_number] = relative_path

    return problem_paths


def fix_leethub_links():

    readme_path = os.path.join(ROOT, "README.md")

    if not os.path.exists(readme_path):
        print("README.md not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    if START_MARKER not in content or END_MARKER not in content:
        print("LeetHub table markers not found.")
        return

    problem_paths = find_problem_paths()

    table_pattern = (
        re.escape(START_MARKER)
        + r"(.*?)"
        + re.escape(END_MARKER)
    )

    match = re.search(
        table_pattern,
        content,
        flags=re.DOTALL
    )

    if not match:
        print("LeetHub table not found.")
        return

    table = match.group(1)

    row_pattern = re.compile(
        r"(\|\s*)(\d+)(\s*\|\s*)"
        r"(\[[^\]]+\])"
        r"\(([^)]+)\)"
        r"(\s*\|\s*[^|]+\|\s*[^|]+\|)"
    )

    changes = 0

    def replace_link(row_match):

        nonlocal changes

        problem_number = row_match.group(2)
        current_path = row_match.group(5)

        new_path = problem_paths.get(problem_number)

        if not new_path:
            return row_match.group(0)

        if current_path == new_path:
            return row_match.group(0)

        changes += 1

        return (
            row_match.group(1)
            + problem_number
            + row_match.group(3)
            + row_match.group(4)
            + "("
            + new_path
            + ")"
            + row_match.group(6)
        )

    updated_table = row_pattern.sub(
        replace_link,
        table
    )

    if changes == 0:
        print("No LeetHub link changes needed.")
        return

    updated_content = (
        content[:match.start(1)]
        + updated_table
        + content[match.end(1):]
    )

    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print(f"Updated {changes} LeetHub link(s).")


if __name__ == "__main__":
    fix_leethub_links()
