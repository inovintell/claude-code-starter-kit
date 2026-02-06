---
allowed-tools: Bash, Read, Write, Glob
description: Onboard ML assessment candidate - create repo, add collaborator, generate HTML email
argument-hint: [first-name] [repo-suffix] [github-username] [email] [deadline-date]
model: sonnet
---

# Onboard ML Assessment Candidate

Create a private assessment repository for a candidate, add them as collaborator, and generate a professional HTML email ready for Outlook.

## Variables

CANDIDATE_FIRST_NAME: $1
CANDIDATE_REPO_SUFFIX: $2
CANDIDATE_GITHUB: $3
CANDIDATE_EMAIL: $4
DEADLINE_DATE: $5
SENDER_NAME: Your Name
SENDER_TITLE: Your Title
COMPANY: Your Company
BASE_REPO: org/assessment-template
OUTPUT_DIR: ~/Downloads/assessments

## Workflow

1. Create private GitHub repository:
   ```
   gh repo create org/assessment-$2 --private --description "Assessment for candidate"
   ```

2. Add remote, push code, and remove remote:
   ```
   git remote add candidate-temp https://github.com/org/assessment-$2.git
   git push candidate-temp main
   git remote remove candidate-temp
   ```

3. Add candidate as collaborator (if GitHub username provided):
   ```
   gh api repos/org/assessment-$2/collaborators/$3 -X PUT
   ```

4. Generate HTML email file at `OUTPUT_DIR/email-$2.html` with:
   - Professional styling (Calibri font, proper headers)
   - Dark code blocks (#1e1e1e background, #d4d4d4 text) for visibility in Outlook
   - Repository URL and clone instructions
   - Timeline with today as start date and $5 as deadline
   - Evaluation criteria
   - Submission instructions (feature branch, PR to main)
   - If no GitHub username provided, include ACTION REQUIRED callout box asking for it

5. Use this HTML template structure:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
   <style>
   body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #333; }
   h2 { color: #2c3e50; font-size: 14pt; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
   code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: Consolas, monospace; font-size: 10pt; }
   pre { background: #1e1e1e; color: #d4d4d4; border: 1px solid #333; padding: 12px; border-radius: 5px; font-family: Consolas, monospace; font-size: 10pt; }
   .action { background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0; }
   </style>
   </head>
   <body>
   <!-- Email content here -->
   </body>
   </html>
   ```

## Report

After completion, provide:
- Repository URL
- Collaborator status (invited or needs GitHub username)
- HTML email path
- Candidate email address for reference
