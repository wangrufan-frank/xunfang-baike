# Controlled Site Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create an encrypted, integrity-verifiable archive of the existing `xunfang-baike` project for controlled preservation and later intranet migration.

**Architecture:** Build a file-level SHA-256 manifest outside the source tree, then use the locally installed WinRAR CLI to create a RAR5 archive with AES-256 encryption for both file data and file names. Preserve the complete site, media, mini-program, untracked presentation material, `.env`, and Git history while excluding disposable caches and duplicate worktrees. Verify the encrypted archive with its password, generate an external SHA-256 checksum, and remove temporary manifest material after verification.

**Tech Stack:** PowerShell 7/Windows PowerShell, WinRAR 6.11 CLI (`F:\WinRAR\Rar.exe`), Git, SHA-256

## Global Constraints

- Source: `F:\frank第二大脑\xunfang-baike`.
- Output directory: `F:\frank第二大脑\controlled-archives`.
- Output name: `xunfang-baike-controlled-archive-2026-07-14.rar`.
- The archive must use RAR5 AES-256 encryption and encrypted file names through WinRAR's `-hp` switch.
- Include `.git`, `.env`, all website content, media, mini-program files, documentation, utilities, and the untracked presentation file.
- Exclude `.worktrees`, `.netlify`, `.superpowers`, `__pycache__`, `*.pyc`, and `*.pid`.
- Do not upload, push, deploy, or otherwise transmit the archive.
- Do not print the archive password until archive creation and verification succeed.
- Do not commit the archive, checksum, manifest, password, or untracked presentation file.

---

### Task 1: Preflight and archive manifest

**Files:**
- Create temporarily: `F:\frank第二大脑\controlled-archives\.staging-2026-07-14\ARCHIVE-MANIFEST.tsv`
- Create temporarily: `F:\frank第二大脑\controlled-archives\.staging-2026-07-14\ARCHIVE-NOTES.txt`

**Interfaces:**
- Consumes: the current filesystem state of `F:\frank第二大脑\xunfang-baike`.
- Produces: a manifest containing `RelativePath`, `Length`, and `SHA256`, plus notes recording source, UTC creation time, Git HEAD, Git status, inclusions, and exclusions.

- [ ] **Step 1: Confirm prerequisites and free space**

Run:

```powershell
Test-Path -LiteralPath 'F:\WinRAR\Rar.exe'
cmd /c dir F:\
git -C 'F:\frank第二大脑\xunfang-baike' rev-parse --verify HEAD
git -C 'F:\frank第二大脑\xunfang-baike' status --short
```

Expected: WinRAR reports `True`, F: has at least 1 GiB free, Git returns a commit hash, and status shows no unexpected tracked modifications.

- [ ] **Step 2: Select included files with explicit exclusions**

Use `Get-ChildItem -Force -Recurse -File` under the source and exclude paths matching `.worktrees`, `.netlify`, `.superpowers`, `__pycache__`, plus extensions `.pyc` and `.pid`. Sort by normalized relative path.

Expected: the selection includes `.git`, `.env`, HTML, JavaScript, CSS, media, mini-program data, documentation, utilities, and the untracked presentation.

- [ ] **Step 3: Generate the manifest and notes**

For every selected file, calculate SHA-256 with `Get-FileHash -Algorithm SHA256`. Write UTF-8 tab-separated rows to `ARCHIVE-MANIFEST.tsv`. Write the source path, UTC time, Git HEAD, Git status, inclusion policy, and exclusion policy to `ARCHIVE-NOTES.txt`.

Expected: both temporary files exist, the manifest has one data row per selected file, and neither file is inside the source repository.

### Task 2: Encrypted archive creation

**Files:**
- Create: `F:\frank第二大脑\controlled-archives\xunfang-baike-controlled-archive-2026-07-14.rar`

**Interfaces:**
- Consumes: the source tree and Task 1 manifest files.
- Produces: a RAR5 archive with AES-256 encrypted contents and encrypted file names.

- [ ] **Step 1: Generate a strong one-time password in memory**

Generate 24 cryptographically random bytes with `System.Security.Cryptography.RandomNumberGenerator`, encode them with Base64, and replace `/`, `+`, and `=` with filename- and shell-safe letters. Keep the value only in the active PowerShell process.

Expected: a password of at least 32 printable characters exists in memory and has not been printed or written to disk.

- [ ] **Step 2: Create the encrypted RAR5 archive**

From `F:\frank第二大脑`, run `F:\WinRAR\Rar.exe a` with `-ma5`, `-m5`, `-htb`, `-hp<password>`, the output archive, the `xunfang-baike` directory, and both staging files. Pass explicit `-x` exclusions for `.worktrees`, `.netlify`, `.superpowers`, `__pycache__`, `*.pyc`, and `*.pid`.

Expected: WinRAR exits with code `0`, reports `All OK`, and creates a non-empty archive outside the source repository.

- [ ] **Step 3: Verify archive integrity and encrypted headers**

Run `Rar.exe t -p<password> <archive>` and require exit code `0`. Then run `Rar.exe lb -p- <archive>` without the password.

Expected: the test command reports `All OK`; listing without a password fails to reveal file names, confirming header encryption.

### Task 3: Checksum, cleanup, and handoff

**Files:**
- Create: `F:\frank第二大脑\controlled-archives\xunfang-baike-controlled-archive-2026-07-14.rar.sha256.txt`
- Remove after verification: `F:\frank第二大脑\controlled-archives\.staging-2026-07-14`

**Interfaces:**
- Consumes: the verified encrypted archive and in-memory password.
- Produces: a portable archive checksum and the one-time handoff password shown to the user exactly once.

- [ ] **Step 1: Generate the external archive checksum**

Run `Get-FileHash -Algorithm SHA256` on the RAR file and write `<hash>  <filename>` to the checksum text file.

Expected: the checksum file contains one 64-character hexadecimal SHA-256 digest and the exact archive filename.

- [ ] **Step 2: Remove temporary plaintext metadata safely**

Resolve the staging directory to an absolute path and confirm it equals `F:\frank第二大脑\controlled-archives\.staging-2026-07-14`. Only after that equality check, remove the staging directory recursively with native PowerShell `Remove-Item -LiteralPath`.

Expected: the staging directory no longer exists; the RAR and checksum remain.

- [ ] **Step 3: Perform final verification**

Run the archive test again with the in-memory password, verify the external checksum by recalculating SHA-256, list output sizes, and run `git status --short` in the source repository.

Expected: archive test returns `All OK`, recalculated and recorded checksums match, the archive is outside the repository, and the only untracked source item remains the pre-existing presentation file.

- [ ] **Step 4: Handoff**

Report the archive path, checksum path, archive size, included/excluded categories, verification result, and the generated password. Instruct the user to store the password separately in a unit-approved location and not in the same folder as the archive.
