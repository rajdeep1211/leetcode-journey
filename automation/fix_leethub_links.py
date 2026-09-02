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
    """
    Find all organized LeetCode problem folders and map
    their problem number to the actual repository path.

    Example:
        0121-best-time-to-buy-and-sell-stock
        becomes:
        121 -> algorithms/arrays/0121-best-time-to-buy-and-sell-stock/
    """

    problem_paths = {}

    for search_root in SEARCH_ROOTS:

        root_path = os.path.join(ROOT, search_root)

        if not os.path.exists(root_path):
            continue

        for current_root, dirs, files in os.walk(root_path):

            for directory in dirs:

                match = re.match(r"^(\d+)-", directory)

                if not match:
                    continue

                # Remove leading zeros.
                # 0001 -> 1
                # 0121 -> 121
                # 0217 -> 217
                # 0175 -> 175
                problem_number = str(int(match.group(1)))

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

    with open(
        readme_path,
        "r",
        encoding="utf-8"
    ) as file:
        content = file.read()

    # Check that the LeetHub table exists.
    if (
        START_MARKER not in content
        or END_MARKER not in content
    ):
        print("LeetHub table markers not found.")
        return

    # Find all organized problem folders.
    problem_paths = find_problem_paths()

    if not problem_paths:
        print("No organized LeetCode problem folders found.")
        return

    print("Found organized problem paths:")

    for number, path in sorted(
        problem_paths.items(),
        key=lambda item: int(item[0])
    ):
        print(f"  {number} -> {path}")

    # Locate the LeetHub table.
    pattern = (
        re.escape(START_MARKER)
        + r"(.*?)"
        + re.escape(END_MARKER)
    )

    match = re.search(
        pattern,
        content,
        flags=re.DOTALL
    )

    if not match:
        print("LeetHub table not found.")
        return

    table = match.group(1)

    # Match a complete LeetHub table row.
    #
    # Example:
    #
    # | 121 | [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock/) | Easy | 2026-09-02 |
    #
    row_pattern = re.compile(
        r"(\|\s*)"                 # Start of row
        r"(\d+)"                   # Problem number
        r"(\s*\|\s*)"              # Separator
        r"(\[[^\]]+\])"            # Problem title
        r"\(([^)]+)\)"             # Current link
        r"(\s*\|\s*[^|]+\|\s*[^|]+\s*\|)"  # Difficulty + solved date
    )

    changes = 0

    def replace_link(row_match):

        nonlocal changes

        problem_number = row_match.group(2)
        current_path = row_match.group(5)

        # Find the actual organized folder.
        new_path = problem_paths.get(problem_number)

        # Problem folder doesn't exist.
        if not new_path:
            return row_match.group(0)

        # Link is already correct.
        if current_path == new_path:
            return row_match.group(0)

        changes += 1

        print(
            f"Fixing problem {problem_number}: "
            f"{current_path} -> {new_path}"
        )

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

    # Replace incorrect links.
    updated_table = row_pattern.sub(
        replace_link,
        table
    )

    # Nothing changed.
    if changes == 0:
        print("No LeetHub link changes needed.")
        return

    # Replace only the LeetHub table.
    updated_content = (
        content[:match.start(1)]
        + updated_table
        + content[match.end(1):]
    )

    with open(
        readme_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(updated_content)

    print(
        f"Updated {changes} LeetHub link(s)."
    )


if __name__ == "__main__":
    fix_leethub_links()
