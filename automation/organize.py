import os
import re
import shutil
import requests


REPO_ROOT = os.getcwd()


CATEGORY_MAP = {
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


def get_problem_folders():
    folders = []

    for item in os.listdir(REPO_ROOT):
        path = os.path.join(REPO_ROOT, item)

        if not os.path.isdir(path):
            continue

        # Matches folders such as:
        # 1-two-sum
        # 15-3sum
        # 121-best-time-to-buy-and-sell-stock
        if re.match(r"^\d+-", item):
            folders.append(item)

    return folders


def extract_problem_id(folder_name):
    match = re.match(r"^(\d+)-", folder_name)

    if match:
        return int(match.group(1))

    return None


def get_title_from_question(folder_path, folder_name):
    question_file = os.path.join(folder_path, "question.md")

    if os.path.exists(question_file):
        with open(question_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Try to find a markdown heading.
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)

        if match:
            return match.group(1).strip()

    # Fallback to folder name
    name = re.sub(r"^\d+-", "", folder_name)
    return name.replace("-", " ").title()


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


def get_slug(folder_name):
    return re.sub(r"^\d+-", "", folder_name)


def determine_category(tags):
    tag_names = [tag["name"] for tag in tags]

    # Priority order.
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
            return CATEGORY_MAP[tag]

    return "other"


def create_readme(problem, source_folder, destination_folder):
    problem_id = problem["questionFrontendId"]
    title = problem["title"]
    difficulty = problem["difficulty"]
    tags = [tag["name"] for tag in problem["topicTags"]]

    primary_category = determine_category(problem["topicTags"])

    notes_path = os.path.join(source_folder, "notes.md")
    question_path = os.path.join(source_folder, "question.md")

    notes = ""

    if os.path.exists(notes_path):
        with open(notes_path, "r", encoding="utf-8") as file:
            notes = file.read().strip()

    readme = f"""# {problem_id}. {title}

**Difficulty:** {difficulty}  
**Category:** Algorithms  
**Primary Pattern:** {primary_category}  
**Topics:** {", ".join(tags)}

---

## Problem

See [`question.md`](./question.md) for the complete problem statement.

---

## Approach

### Thought Process

Write your reasoning here.

- What was your first idea?
- What observation helped?
- Why does the final approach work?

### Algorithm

1. Identify the key observation.
2. Apply the chosen data structure or algorithm.
3. Process the input.
4. Return the result.

---

## Complexity

**Time:** `O(?)`

**Space:** `O(?)`

---

## Solution

The accepted LeetCode solution is available in the solution file.

---

## My Notes

{notes}

---

## Key Takeaway

Write the main concept or pattern learned from this problem.

---

## Related Topics

{", ".join(f"- {tag}" for tag in tags)}
"""

    os.makedirs(destination_folder, exist_ok=True)

    readme_path = os.path.join(destination_folder, "README.md")

    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(readme)


def process_problem(folder_name):
    source_folder = os.path.join(REPO_ROOT, folder_name)

    problem_id = extract_problem_id(folder_name)

    if problem_id is None:
        return

    slug = get_slug(folder_name)

    print(f"Processing: {folder_name}")

    problem = query_leetcode(slug)

    if not problem:
        print(f"Could not find LeetCode data for {folder_name}")
        return

    category = determine_category(problem["topicTags"])

    destination_parent = os.path.join(
        REPO_ROOT,
        "algorithms",
        category
    )

    os.makedirs(destination_parent, exist_ok=True)

    destination_folder = os.path.join(
        destination_parent,
        f"{problem_id:04d}-{slug}"
    )

    # Already organized.
    if os.path.abspath(source_folder) == os.path.abspath(destination_folder):
        return

    # Move files.
    if not os.path.exists(destination_folder):
        shutil.move(source_folder, destination_folder)
    else:
        # Merge files if destination already exists.
        for item in os.listdir(source_folder):
            source = os.path.join(source_folder, item)
            destination = os.path.join(destination_folder, item)

            if os.path.exists(destination):
                continue

            shutil.move(source, destination)

        shutil.rmtree(source_folder)

    create_readme(
        problem,
        destination_folder,
        destination_folder
    )

    print(
        f"Organized {problem['title']} → "
        f"algorithms/{category}/{problem_id:04d}-{slug}"
    )


def main():
    folders = get_problem_folders()

    if not folders:
        print("No new LeetCode problem folders found.")
        return

    for folder in folders:
        try:
            process_problem(folder)
        except Exception as error:
            print(f"Error processing {folder}: {error}")


if __name__ == "__main__":
    main()
