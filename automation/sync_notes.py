import os
import re


ROOT = os.getcwd()


START_MARKER = "<!-- AUTO-NOTES-START -->"
END_MARKER = "<!-- AUTO-NOTES-END -->"


def find_problem_folders():

    problems = []

    search_roots = [
        os.path.join(ROOT, "algorithms"),
        os.path.join(ROOT, "database"),
        os.path.join(ROOT, "shell"),
        os.path.join(ROOT, "pandas"),
        os.path.join(ROOT, "concurrency"),
        os.path.join(ROOT, "other"),
    ]

    for root in search_roots:

        if not os.path.exists(root):
            continue

        for current_root, directories, files in os.walk(root):

            folder_name = os.path.basename(current_root)

            if re.match(r"^\d+-", folder_name):

                problems.append(current_root)

    return problems


def read_notes(notes_path):

    with open(
        notes_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read().strip()


def update_readme(problem_folder):

    notes_path = os.path.join(
        problem_folder,
        "notes.md"
    )

    readme_path = os.path.join(
        problem_folder,
        "README.md"
    )

    if not os.path.exists(notes_path):
        return

    if not os.path.exists(readme_path):
        return

    notes = read_notes(notes_path)

    if not notes:
        return

    notes_block = (
        f"{START_MARKER}\n\n"
        f"## 💭 My Solving Notes\n\n"
        f"{notes}\n\n"
        f"{END_MARKER}"
    )

    with open(
        readme_path,
        "r",
        encoding="utf-8"
    ) as file:

        readme = file.read()

    pattern = (
        re.escape(START_MARKER)
        + r".*?"
        + re.escape(END_MARKER)
    )

    if re.search(
        pattern,
        readme,
        re.DOTALL
    ):

        readme = re.sub(
            pattern,
            notes_block,
            readme,
            flags=re.DOTALL
        )

    else:

        readme = (
            readme.rstrip()
            + "\n\n"
            + notes_block
            + "\n"
        )

    with open(
        readme_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(readme)

    print(
        f"Updated README: {problem_folder}"
    )


def main():

    problems = find_problem_folders()

    print(
        f"Found {len(problems)} problem folders."
    )

    for problem in problems:

        try:

            update_readme(problem)

        except Exception as error:

            print(
                f"Error processing {problem}: {error}"
            )


if __name__ == "__main__":
    main()
