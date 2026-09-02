import os
import re
import shutil
import requests


ROOT = os.getcwd()


# =========================================================
# CATEGORY CONFIGURATION
# =========================================================

ALGORITHM_CATEGORIES = {
    "Array": "arrays",
    "String": "strings",
    "Hash Table": "hashing",
    "Two Pointers": "two-pointers",
    "Sliding Window": "sliding-window",
    "Binary Search": "binary-search",
    "Linked List": "linked-list",
    "Stack": "stack",
    "Queue": "queue",
    "Tree": "trees",
    "Binary Tree": "trees",
    "Binary Search Tree": "trees",
    "Graph": "graphs",
    "Heap": "heap",
    "Priority Queue": "heap",
    "Greedy": "greedy",
    "Backtracking": "backtracking",
    "Dynamic Programming": "dynamic-programming",
    "Bit Manipulation": "bit-manipulation",
    "Math": "math",
    "Matrix": "arrays",
}


DATABASE_TAGS = {
    "Database",
}


OTHER_CATEGORIES = {
    "Shell": "shell",
    "Pandas": "pandas",
    "Concurrency": "concurrency",
}


# =========================================================
# FIND RAW LEETCODE FOLDERS
# =========================================================

def get_problem_folders():

    folders = []

    for item in os.listdir(ROOT):

        path = os.path.join(ROOT, item)

        if not os.path.isdir(path):
            continue

        if re.match(r"^\d+-", item):
            folders.append(item)

    return folders


# =========================================================
# PROBLEM ID
# =========================================================

def extract_problem_id(folder_name):

    match = re.match(r"^(\d+)-", folder_name)

    if match:
        return int(match.group(1))

    return None


# =========================================================
# SLUG
# =========================================================

def get_slug(folder_name):

    return re.sub(r"^\d+-", "", folder_name)


# =========================================================
# LEETCODE API
# =========================================================

def query_leetcode(title_slug):

    url = "https://leetcode.com/graphql/"

    query = """
    query questionData($titleSlug: String!) {

        question(titleSlug: $titleSlug) {

            questionFrontendId
            title
            titleSlug
            difficulty

            topicTags {
                name
                slug
            }
        }
    }
    """

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": {
                "titleSlug": title_slug
            }
        },
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/"
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data.get("data", {}).get("question")


# =========================================================
# CATEGORY
# =========================================================

def determine_category(tags):

    tag_names = {tag["name"] for tag in tags}

    # Database
    if tag_names.intersection(DATABASE_TAGS):
        return "database/sql"

    # Other categories
    for tag, folder in OTHER_CATEGORIES.items():

        if tag in tag_names:
            return folder

    # Algorithms
    priority = [
        "Array",
        "String",
        "Hash Table",
        "Two Pointers",
        "Sliding Window",
        "Binary Search",
        "Linked List",
        "Stack",
        "Queue",
        "Tree",
        "Binary Tree",
        "Binary Search Tree",
        "Graph",
        "Heap",
        "Priority Queue",
        "Greedy",
        "Backtracking",
        "Dynamic Programming",
        "Bit Manipulation",
        "Math",
        "Matrix",
    ]

    for tag in priority:

        if tag in tag_names:
            return f"algorithms/{ALGORITHM_CATEGORIES[tag]}"

    return "other"


# =========================================================
# PRIMARY PATTERN
# =========================================================

def determine_primary_pattern(tags):

    tag_names = {tag["name"] for tag in tags}

    # Database / SQL problems
    if "Database" in tag_names:
        return "SQL"

    priority = [
        "Hash Table",
        "Two Pointers",
        "Sliding Window",
        "Binary Search",
        "Dynamic Programming",
        "Backtracking",
        "Graph",
        "Tree",
        "Heap",
        "Linked List",
        "Stack",
        "Queue",
        "Array",
        "String",
        "Greedy",
        "Bit Manipulation",
        "Math",
    ]

    for tag in priority:

        if tag in tag_names:
            return tag

    return "Other"

# =========================================================
# README GENERATOR
# =========================================================

def create_readme(problem, destination_folder):

    readme_path = os.path.join(
        destination_folder,
        "README.md"
    )

    # Don't overwrite an existing README.
    if os.path.exists(readme_path):
        print(
            f"README already exists: {readme_path}"
        )
        return

    problem_id = problem["questionFrontendId"]
    title = problem["title"]
    difficulty = problem["difficulty"]

    tags = [
        tag["name"]
        for tag in problem["topicTags"]
    ]

    primary_pattern = determine_primary_pattern(
        problem["topicTags"]
    )

    category = determine_category(
        problem["topicTags"]
    )

    if category.startswith("algorithms/"):
        display_category = "Algorithms"
    elif category.startswith("database"):
        display_category = "Database"
    else:
        display_category = category.title()

    related_topics = "\n".join(
        f"- {tag}"
        for tag in tags
    )

    readme = f"""# {problem_id}. {title}

**Difficulty:** {difficulty}  
**Category:** {display_category}  
**Primary Pattern:** {primary_pattern}  
**Topics:** {", ".join(tags)}

---

## 🧩 Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## 💭 My Solving Notes

<!-- AUTO-NOTES-START -->

Complete `notes.md` after solving the problem.

<!-- AUTO-NOTES-END -->

---

## 🔎 Algorithm

The algorithm is documented in the solving notes above.

---

## ⏱️ Complexity

See the complexity section in `notes.md`.

---

## 💻 Solution

The accepted solution is available in the solution file.

---

## 🧠 Key Takeaway

See the key learning in `notes.md`.

---

## 🔗 Related Topics

{related_topics}
"""

    with open(
        readme_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(readme)


# =========================================================
# PROCESS PROBLEM
# =========================================================

def process_problem(folder_name):

    source_folder = os.path.join(
        ROOT,
        folder_name
    )

    problem_id = extract_problem_id(
        folder_name
    )

    if problem_id is None:
        return

    slug = get_slug(folder_name)

    print(f"Processing: {folder_name}")

    problem = query_leetcode(slug)

    if not problem:

        print(
            f"Could not retrieve LeetCode data "
            f"for {folder_name}"
        )

        return

    category = determine_category(
        problem["topicTags"]
    )

    destination_parent = os.path.join(
        ROOT,
        category
    )

    os.makedirs(
        destination_parent,
        exist_ok=True
    )

    destination_folder = os.path.join(
        destination_parent,
        f"{problem_id:04d}-{slug}"
    )

    # -----------------------------------------------------
    # MOVE RAW PROBLEM
    # -----------------------------------------------------

    if os.path.abspath(source_folder) != os.path.abspath(
        destination_folder
    ):

        if not os.path.exists(destination_folder):

            shutil.move(
                source_folder,
                destination_folder
            )

        else:

            for item in os.listdir(source_folder):

                source = os.path.join(
                    source_folder,
                    item
                )

                destination = os.path.join(
                    destination_folder,
                    item
                )

                if not os.path.exists(destination):

                    shutil.move(
                        source,
                        destination
                    )

            shutil.rmtree(
                source_folder
            )

    # -----------------------------------------------------
    # CREATE README
    # -----------------------------------------------------

    create_readme(
        problem,
        destination_folder
    )

    print(
        f"Organized: {problem['title']}"
    )

    print(
        f"Location: {category}/"
        f"{problem_id:04d}-{slug}"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    folders = get_problem_folders()

    if not folders:

        print(
            "No raw LeetCode problem folders found."
        )

        return

    for folder in folders:

        try:

            process_problem(folder)

        except Exception as error:

            print(
                f"Error processing {folder}: {error}"
            )


if __name__ == "__main__":
    main()
