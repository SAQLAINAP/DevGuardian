import os
import openai
import json
from github import Github

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# GitHub Token for making comments
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo("SAQLAINAP/AutomatnfraMan")

# Fetch latest PR
pull_requests = repo.get_pulls(state='open', sort='created', base='main')

if pull_requests.totalCount > 0:
    pr = pull_requests[0]  # Get latest PR
    pr_files = pr.get_files()

    review_comments = []

    for file in pr_files:
        code_content = repo.get_contents(file.filename).decoded_content.decode()

        prompt = f"Review this code for best practices, bugs, and security flaws:\n\n{code_content}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a senior code reviewer."},
                      {"role": "user", "content": prompt}]
        )

        review = response["choices"][0]["message"]["content"]
        review_comments.append(f"File: {file.filename}\nReview:\n{review}")

    pr.create_issue_comment("\n\n".join(review_comments))
