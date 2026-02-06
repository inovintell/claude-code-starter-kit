---
allowed-tools: Bash(git ls-files:*), Read, Bash(gh: *), Write
description: Write HTML report about recent progress on the projects
---

# Biweekly review report

List github issues and/or pull requests created and closed between current date and `LOOKBACK_DAYS` days before. Follow `Instructions` , take care of `Standards` and than use `Report` section to shape up the report and store it on locally.

# Variables
LOOKBACK_DAYS: $1 (default 7 days)
OUTPUT_PATH: ~/Desktop
FILENAME_FORMATTED: `biweekly-issue-report-{YYYY-MM-DD}.html` (use current date)
REPOSITORIES:
  - owner/repo-1
  - owner/repo-2

# Instructions
- For each repository in REPOSITORIES, use `gh issue list --repo <owner>/<repo>` with `--state`, `--json`, and `--search` flags to query issues by creation/closure dates
- Combine results from all repositories into a single report
- Use `gh issue view --repo <owner>/<repo>` to get detailed issue information including body content
- Use `gh pr list --repo <owner>/<repo>` with similar flags to query pull requests
- Filter by date using `--search "created:>=YYYY-MM-DD"` or `--search "closed:>=YYYY-MM-DD"`
- When displaying issues in the report, include the repository name/source for each issue
- When there is no issue associated with pull request, report on it same way you would on issue
- When issue has multiple PRs, briefly mention each one of them
- Filter out PRs not merged/created by me, ie. renovate dependency updates are out of scope

# Standards

Format all responses as clean, semantic HTML using modern HTML5 standards:

## Document Structure
- Wrap the entire response in `<article>` tags
- Use `<header>` for introductory content
- Use `<main>` for primary content
- Use `<section>` to group related content

## Headings and Text
- Use `<h2>` for main sections
- Use `<h3>` for subsections
- Use `<strong>` for emphasis and important text
- Use `<p>` for paragraphs

## Lists and Tables
- Use `<ul>` for unordered lists, `<ol>` for ordered lists
- Structure tables with `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`

# Report

- Write report to the location `OUTPUT_PATH`/`FILENAME_FORMATTED`
- open the report in the browser
  - Run `open {OUTPUT_PATH}/{FILENAME_FORMATTED}`

## Output Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Biweekly Issue Report: {Date Range}</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.6;
      max-width: 1200px;
      margin: 0 auto;
      padding: 2em;
      background: #ffffff;
      color: #333;
    }
    h2, h3, h4 { color: #1a1a1a; }
    a { color: #0066cc; text-decoration: none; }
    a:hover { text-decoration: underline; }
    table { border-collapse: collapse; width: 100%; margin: 1em 0; }
    th, td { padding: 0.75em; border: 1px solid #ddd; }
    th { background: #f5f5f5; text-align: left; }
    code { font-family: monospace; background: #f5f5f5; padding: 2px 4px; }
  </style>
</head>
<body>
<article>
  <header>
    <h2>Biweekly Issue Report: {Date Range}</h2>
  </header>
  <main>
    <section>
      <h3>Executive Summary</h3>
      <!-- Summary content -->
    </section>
    <section>
      <h3>Activity Metrics</h3>
      <!-- Metrics table -->
    </section>
    <section>
      <h3>Open Issues</h3>
      <!-- Open issues -->
    </section>
    <section>
      <h3>Closed Issues</h3>
      <!-- Closed issues -->
    </section>
  </main>
  <footer>
    <p>Generated: {date}</p>
  </footer>
</article>
</body>
</html>
```
