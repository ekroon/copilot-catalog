---
name: create-pr
description: Creates a pull request from current changes. Commits changes logically, finds PR templates, and opens the PR using the gh CLI. Best used after completing work.
user-invocable: true
---

# Pull Request Creator

You are now in PR creation mode. Your job is to take the current uncommitted changes (or unpushed commits), organize them into logical commits, and create a well-structured pull request.

**The user invoking this skill is their confirmation.** Do not ask for additional confirmation before committing, pushing, or creating the PR—just do it.

**Important:** This skill is typically invoked at the end of a session after you've already made changes. You likely already have context about what was changed and why—**use that knowledge** rather than re-analyzing diffs unnecessarily.

## Prerequisites

- The `gh` CLI is installed and authenticated
- You are in a git repository with a remote configured
- There are changes to commit (staged, unstaged, or unpushed commits)

## Workflow

### Step 1: Check Git State

Get the minimal info needed to proceed:

```bash
# Get branch, status, and remote in one command
git rev-parse --abbrev-ref HEAD && git status --short && git remote get-url origin
```

From the remote URL, extract **owner** and **repo**.

### Step 2: Understand the Changes

If you already have context from this session about what changed and why, use it. Otherwise, review the changes:

```bash
git diff --stat                      # Overview of files changed
git diff -- path/to/file.ts          # Full diff for specific files if needed
```

### Step 3: Create Logical Commits

Group related changes into logical commits. Each commit should:

- Represent a single logical change
- Have a clear, descriptive message
- Be atomic (could be reverted independently if needed)

**For a single logical change:**

```bash
git add -A
git commit -m "Add user authentication endpoint"
```

**For multiple logical changes, commit separately:**

```bash
# First logical group
git add src/auth.ts src/types/auth.ts
git commit -m "Add authentication types and handler"

# Second logical group
git add src/routes.ts
git commit -m "Wire up auth routes"

# Third logical group
git add tests/auth.test.ts
git commit -m "Add authentication tests"
```

**Commit message guidelines:**

- Keep the subject line under 72 characters
- Be specific about what changed

### Step 4: Push the Branch

```bash
# Push to remote (set upstream if needed)
git push -u origin HEAD
```

### Step 5: Find PR Template

Look for PR templates in standard locations:

```bash
# Check common template locations
for f in \
  .github/pull_request_template.md \
  .github/PULL_REQUEST_TEMPLATE.md \
  docs/pull_request_template.md \
  pull_request_template.md \
  PULL_REQUEST_TEMPLATE.md \
  .github/PULL_REQUEST_TEMPLATE/*.md; do
  [ -f "$f" ] && echo "Found: $f"
done
```

If a template exists, read it and use its structure. If multiple templates exist (in `.github/PULL_REQUEST_TEMPLATE/`), choose the most appropriate one based on the change type (feature, bugfix, etc.).

### Step 6: Generate PR Title and Body

**Title:** Create a concise title that summarizes the PR:

- For single commits: Use the commit message subject
- For multiple commits: Summarize the overall change
- Follow any repo conventions (e.g., prefixes like `CLI:`, `feat:`)

**Body:** Generate a comprehensive PR description:

1. If a template exists, fill in each section thoughtfully
2. If no template, create a description with:
    - **What**: High-level summary of changes
    - **Why**: Motivation/context (reference issues if branch name suggests one)
    - **How**: Brief technical approach if non-obvious
    - **Testing**: How the changes were verified

Use the commit messages and diff to write accurate, helpful descriptions.

### Step 7: Create the Pull Request

**On Windows:** Backticks in `--body` strings get mangled by PowerShell escaping. Always write the PR body to a temp file and use `--body-file` instead:

```bash
# Write body to temp file, create PR, clean up
gh pr create --title "Your PR title" --body-file pr-body.md --base main
rm pr-body.md
```

**On macOS/Linux:**

```bash
# Create the PR
gh pr create \
  --title "Your PR title" \
  --body "Your PR body" \
  --base main
```

If the base branch is not `main`, detect it:

```bash
# Get default branch
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

After creation, display the PR URL to the user.

## Handling Edge Cases

### No Changes

If there are no uncommitted changes and no unpushed commits:

1. Check if a PR already exists for this branch (`gh pr view`)
2. If no PR exists and branch is not the default branch, proceed to create one (Step 7)
3. If a PR already exists, inform the user there's nothing new to push
4. If on the default branch with no changes, tell the user to make changes first

### Already on Default Branch

If working directly on `main`/`master`:

```bash
# Create a feature branch first
git checkout -b feature/descriptive-name
```

Then proceed with commits.

### PR Already Exists

Check if a PR already exists for this branch:

```bash
gh pr view --json url 2>/dev/null && echo "PR already exists"
```

If so, just push the new commits - the PR will update automatically.

### Merge Conflicts with Base

If the branch is behind the base:

```bash
# Fetch and check
git fetch origin main
git log HEAD..origin/main --oneline
```

If there are upstream changes, prefer merging by default:

```bash
git merge origin/main
```

Only rebase if the user explicitly requests it. After resolving any conflicts, continue with the push.

## Output

After successfully creating the PR, provide:

1. The PR URL
2. A summary of commits created
3. Any warnings (e.g., "branch is behind main by 3 commits")

## Example Session

```
Analyzing changes...
Found 5 modified files across 2 logical changes:

Creating commits:
  ✓ feat: add rate limiting middleware (3 files)
  ✓ test: add rate limiting tests (2 files)

Pushing to origin/feature/rate-limiting...
  ✓ Branch pushed

Finding PR template...
  ✓ Using .github/pull_request_template.md

Creating pull request...
  ✓ PR #142 created: https://github.com/owner/repo/pull/142

Summary:
  - 2 commits pushed
  - PR created against main
```
