---
allowed-tools: Bash(git:*), Bash(gh:*), Read, Grep, Glob
description: Create/update issue, feature branch, group changes semantically, commit, optionally create PR
argument-hint: [create-pr: true/false] [issue-id: number]
model: sonnet
---

# Semantic Commit

Analyzes all unstaged changes in the repository, creates or updates a GitHub issue, creates a feature branch linked to the issue (or uses existing branch), groups changes semantically into logical commits, and optionally creates a PR linked to the issue. See `Workflow` for step-by-step execution.

## Variables

CREATE_PR: $1
ISSUE_ID: $2

DEFAULT_CREATE_PR: true

## Workflow

1. Run `git status` to identify all unstaged and staged changes in the repository
2. Run `git diff` to analyze the content of all modified files
3. Run `git diff --cached` to check any already staged changes
4. Determine issue context:
   - If ISSUE_ID is provided, use that issue number
   - Else, check current branch name for issue pattern (e.g., `feat/123-description` -> issue #123)
   - If issue ID found from branch, extract it
   - If no issue ID found, set EXISTING_ISSUE=false
5. Handle issue creation or update:
   - If EXISTING_ISSUE=false (no issue found):
     - Analyze changes to generate descriptive title
     - Create issue body with summary of all changes
     - Use `gh issue create --title "<title>" --body "<description>"`
     - Capture the issue number from output
     - Create feature branch: `git checkout -b <type>/<issue-number>-<short-description>`
   - If issue already exists (from ISSUE_ID or branch name):
     - Stay on current branch (do not create new branch)
     - Add comment to existing issue with summary of NEW changes only
     - Use `gh issue comment <issue-number> --body "<new changes summary>"`
6. Group changes semantically by:
   - Feature additions (new functionality)
   - Bug fixes (corrections to existing code)
   - Refactoring (code improvements without behavior change)
   - Documentation updates
   - Configuration changes
   - Test additions/modifications
   - Style/formatting changes
7. For each semantic group:
   - Stage only the files belonging to that group using `git add <files>`
   - Create a commit with a descriptive message following conventional commits format (feat:, fix:, refactor:, docs:, chore:, test:, style:)
   - Include the standard footer in commit message
8. After all commits are created, check if CREATE_PR is set:
   - If CREATE_PR is empty/unset, use DEFAULT_CREATE_PR (true)
   - If CREATE_PR is "false", skip PR creation and push feature branch directly
   - If CREATE_PR is "true" or default applies, create PR
9. If creating PR:
   - Push feature branch to remote with `git push -u origin <branch-name>`
   - Create PR using `gh pr create` with:
     - Title summarizing all semantic groups
     - Body listing all commits made with their purposes
     - Link to issue with `Closes #<issue-number>` in body
     - Base branch set to main/master
10. If not creating PR:
    - Push feature branch to remote with `git push -u origin <branch-name>`

## Report

Provide a summary including:
- Issue URL (created new or updated existing with comment)
- Feature branch name (created new or using existing)
- Number of semantic groups identified
- List of commits created with their messages
- Files included in each commit
- PR URL if created (linked to issue), or confirmation of direct push
- Any files that were skipped or couldn't be categorized
