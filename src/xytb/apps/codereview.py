#!/usr/bin/env python

import os
import subprocess
from typing import List

from jinja2 import Template
from litellm import completion
from pydantic_settings import BaseSettings
from rich.console import Console
from rich.markdown import Markdown
import typer


class Settings(BaseSettings):
    chat_model: str = "o4-mini"
    diff_head: str = "HEAD^"



settings = Settings()

tpl = """
You are an expert in coding.

Here is the output of `git --no-pager diff` in your terminal
```
{{ git_diff }}
```

Here is the complete code of all changed files.
{{ related_file_cont }}

Please review the changes. Your have following focuses:
1. Please point out the errors that will certainly introduce bugs in the program.
    - When you point them out, please specify the concrete exception that will be raised or the side effect/consequence.
    - Only point out the errors that are brought about by the changes.
2. Please identify places where the code can be clearly simplified. For example:
    - Remove unnecessary try-except blocks.
        - Follow the principle: `Do not catch unknown exceptions when adding new code. Let errors propagate so they can be detected and fixed quickly.`
3. Please suggest ways to **greatly** improve the design of the changes.
    - The most important thing is making the design clear and easy to follow. Modules should be well separated and independent.
        - some general software engineering tricks are not that important.
    - If you are suggesting design improvements, please provide pseudocode to illustrate your ideas (e.g., better class/interface signatures, conceptual blocks to organize the code).
        - When you are mentioning code more than one line, please use code block to make it more readable.
        - Try to use pseudocode when describing the code. This helps keep the explanation clear and focuses on important ideas, leaving out minor details that are not essential.

If you want to point out other errors or detailed design improvements you find, please use a clear divider like "---" to distinguish the errors brought about by the changes from others.

Plaese make the output nice and clear. Clearly seperate the important parts and non-important ones. Organize different sections clearly.
"""

# 1) run git diff to get the changed code

def run_git_diff() -> str:
    """
    Run `git --no-pager diff` and return the diff as a string.
    The output is formatted with Rich markup for better display.
    """
    from rich.console import Console
    from rich.syntax import Syntax

    cmd = ["git", "--no-pager", "diff", settings.diff_head]
    result = subprocess.run(cmd, capture_output=True, text=True)
    diff_content = result.stdout

    # Print the diff using rich.syntax for better highlighting
    if diff_content.strip():  # Only display if there's diff
        console = Console()
        console.print(Syntax(diff_content, "diff", theme="ansi_dark", line_numbers=False))
    return diff_content


# 2) get all the source code of the changed files
def get_changed_files() -> List[str]:
    result = subprocess.run(["git", "diff", "--name-only", settings.diff_head], capture_output=True, text=True)
    files = result.stdout.strip().splitlines()
    # Determine the repository root:
    try:
        repo_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
    except subprocess.CalledProcessError:
        repo_root = os.getcwd()

    # Build absolute paths from repo root and filter out non-existent files (e.g., deleted/renamed)
    full_paths = [os.path.join(repo_root, f) for f in files]
    return [p for p in full_paths if os.path.isfile(p)]


def get_files_content(files: List[str]) -> str:
    content = []
    for filename in files:
        try:
            with open(filename, "r") as f:
                code = f.read()
            content.append(f"Filename: {filename}\n```\n{code}\n```")
        except Exception as e:
            content.append(f"Filename: {filename}\n[Could not read file: {e}]")
    return "\n\n".join(content)


# 3) get LLM response
def get_review(git_diff: str, related_file_cont: str, model: str) -> str:
    prompt = Template(tpl).render(git_diff=git_diff, related_file_cont=related_file_cont)
    response = completion(model=model, messages=[{"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"]


# 4) display the response in markdown in with rich format


def review(model: str = typer.Option(None, help="Chat model to use (overrides config)")):
    console = Console()
    console.rule("Code Changes")
    diff = run_git_diff()

    changed_files = get_changed_files()
    console.rule("Retrieved files")
    console.print(Markdown(f"**Changed files:**\n{changed_files}"))
    files_content = get_files_content(changed_files)
    console.print("LOC: " + str(len(files_content.splitlines())))
    use_model = model or settings.chat_model
    review_response = get_review(diff, files_content, use_model)
    console.rule("Code Review")
    console.print(Markdown(review_response))
