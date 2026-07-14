# Site Folder Backup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the current `xunfang-baike` project as a directly browsable backup folder without compression or encryption.

**Architecture:** Remove only the abandoned encrypted-archive artifacts, then copy the current source tree to a dated sibling directory. Preserve Git history, ignored configuration, media, mini-program files, documentation, utilities, and untracked presentation material while excluding duplicate worktrees and disposable local caches. Verify the backup with independent source and destination SHA-256 manifests.

**Tech Stack:** PowerShell, Robocopy, Git, SHA-256

## Global Constraints

- Source: `F:\frank第二大脑\xunfang-baike`.
- Destination: `F:\frank第二大脑\xunfang-baike-backup-2026-07-14`.
- Include `.git`, `.env`, all site content, media, mini-program files, documentation, utilities, and untracked presentation files.
- Exclude `.worktrees`, `.netlify`, `.superpowers`, `__pycache__`, `*.pyc`, and `*.pid`.
- Do not upload, push, deploy, compress, or encrypt the backup.
- Do not modify or delete source files.

---

### Task 1: Remove abandoned archive artifacts

**Files:**
- Remove: `F:\frank第二大脑\controlled-archives\xunfang-baike-controlled-archive-2026-07-14.rar`
- Remove: `F:\frank第二大脑\controlled-archives\.staging-2026-07-14`

- [ ] Resolve both paths and verify that they are exactly the expected failed outputs.
- [ ] Remove the failed RAR and staging directory with native PowerShell file operations.
- [ ] Verify that neither failed output remains.

### Task 2: Copy the backup folder

**Files:**
- Create: `F:\frank第二大脑\xunfang-baike-backup-2026-07-14\`

- [ ] Confirm that the destination does not already exist.
- [ ] Copy the source with Robocopy using `/E`, `/COPY:DAT`, `/DCOPY:DAT`, `/R:1`, and `/W:1`.
- [ ] Exclude `.worktrees`, `.netlify`, `.superpowers`, `__pycache__`, `*.pyc`, and `*.pid`.
- [ ] Accept Robocopy exit codes 0 through 7 and treat 8 or greater as failure.

### Task 3: Verify and document the backup

**Files:**
- Create: `F:\frank第二大脑\xunfang-baike-backup-2026-07-14\BACKUP-MANIFEST.tsv`
- Create: `F:\frank第二大脑\xunfang-baike-backup-2026-07-14\BACKUP-NOTES.txt`

- [ ] Select source and destination files using the same exclusion rules.
- [ ] Calculate SHA-256 for every source and copied file and compare relative path, length, and hash.
- [ ] Fail if a source file is missing, a destination file differs, or an unexpected copied file exists.
- [ ] Write the verified manifest and notes with source path, destination path, UTC creation time, Git HEAD, Git status, included categories, and excluded categories.
- [ ] Confirm `.git\HEAD`, `.env`, HTML, media, mini-program files, and both presentation files exist in the backup.
- [ ] Report destination, verified file count, total size, Git HEAD, and exclusion policy.
