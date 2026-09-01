import os
import re
import shutil
import requests


REPO_ROOT = os.getcwd()


# ---------------------------------------------------------
# CATEGORY CONFIGURATION
# ---------------------------------------------------------

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
    "SQL",
}


NON_ALGORITHM_CATEGORIES = {
    "Shell": "shell",
    "Pandas": "pandas",
    "Concurrency": "concurrency",
}


# ---------------------------------------------------------
# FIND RAW LEETCODE FOLDERS
# ---------------------------------------------------------

def get_problem_folders():

    folders = []

    for item in os.listdir(REPO_ROOT):

        path = os.path.join(REPO_ROOT, item)

        if not os.path.isdir(path):
            continue

        # Example:
        # 1-two-sum
        # 15-3sum
        # 121-best-time-to-buy-and-sell-stock

        if re.match(r"^\d+-", item):
            folders.append(item)

    return folders


# ---------------------------------------------------------
# EXTRACT PROBLEM ID
# ---------------------------------------------------------

def extract_problem_id(folder_name):

    match = re.match(r"^(\d+)-", folder_name)

    if match:
        return int(match.group(1))

    return None


# ---------------------------------------------------------
# GET SLUG
# ---------------------------------------------------------

def get_slug(folder_name):

    return re.sub(r"^\d+-", "", folder_name)


# ---------------------------------------------------------
# QUERY LEETCODE
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# DETERMINE CATEGORY
# ---------------------------------------------------------

def determine_category(tags):

    tag_names = {tag["name"] for tag in tags}

    # Database
    if tag_names.intersection(DATABASE_TAGS):
        return "database"

    # Other LeetCode categories
    for tag in NON_ALGORITHM_CATEGORIES:

        if tag in tag_names:
            return NON_ALGORITHM_CATEGORIES[tag]

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


# ---------------------------------------------------------
# PRIMARY PATTERN
# ---------------------------------------------------------

def determine_primary_pattern(tags):

    tag_names = {tag["name"] for tag in tags}

    priority = [
        "Array",
        "Hash Table",
        "String",
        "Two Pointers",
        "Sliding Window",
        "Binary Search",
        "Linked List",
        "Stack",
        "Queue",
        "Tree",
        "Graph",
        "Heap",
        "Greedy",
        "Backtracking",
        "Dynamic Programming",
        "Bit Manipulation",
        "Math",
    ]

    for tag in priority:

        if tag in tag_names:
            return tag

    return "Other"


# ---------------------------------------------------------
# CREATE README
# ---------------------------------------------------------

def create_readme(problem, destination_folder):

    readme_path = os.path.join(
        destination_folder,
        "README.md"
    )

    # NEVER overwrite an existing README.
    if os.path.exists(readme_path):

        print(
            f"README already exists. "
            f"Keeping existing README: {readme_path}"
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

    readme = f"""# {problem_id}. {title}

**Difficulty:** {difficulty}  
**Category:** {category}  
**Primary Pattern:** {primary_pattern}  
**Topics:** {", ".join(tags)}

---

## Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## My Thought Process

### 1. Initial Approach

<!--
What was your first idea?

Example:
I initially considered using...
-->

Write your initial thinking here.

---

### 2. Observation

<!--
What important observation helped you solve the problem?
-->

Write the key observation here.

---

### 3. Optimized Approach

<!--
Explain why the final approach is better.
-->

Explain your optimized approach here.

---

## Algorithm

1. Identify the important condition.
2. Select the appropriate data structure or algorithm.
3. Process the input.
4. Return the result.

---

## Complexity

**Time:** `O(?)`

**Space:** `O(?)`

---

## Solution

The accepted solution is available in:

- `solution.*`

---

## Key Takeaway

<!--
What did you learn from this problem?

Example:
Hash maps can reduce repeated searching from O(n)
to O(1) average lookup.
-->

Write your key takeaway here.

---

## Related Topics

{chr(10).join(f"- {tag}" for tag in tags)}
"""

    with open(
        readme_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(readme)


# ---------------------------------------------------------
# PROCESS PROBLEM
# ---------------------------------------------------------

def process_problem(folder_name):

    source_folder = os.path.join(
        REPO_ROOT,
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
        REPO_ROOT,
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
    # ALREADY ORGANIZED
    # -----------------------------------------------------

    if os.path.abspath(source_folder) == os.path.abspath(
        destination_folder
    ):

        create_readme(
            problem,
            destination_folder
        )

        return

    # -----------------------------------------------------
    # MOVE PROBLEM
    # -----------------------------------------------------

    if not os.path.exists(destination_folder):

        shutil.move(
            source_folder,
            destination_folder
        )

    else:

        # Merge files if destination exists.
        for item in os.listdir(source_folder):

            source = os.path.join(
                source_folder,
                item
            )

            destination = os.path.join(
                destination_folder,
                item
            )

            if os.path.exists(destination):
                continue

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


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

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
                f"Error processing {folder}: "
                f"{error}"
            )


if __name__ == "__main__":
    main()
