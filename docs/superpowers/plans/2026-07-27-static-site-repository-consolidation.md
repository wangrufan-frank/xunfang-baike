# Static Site Repository Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the static website the repository's only maintained runtime, archive non-runtime deliverables outside the checkout, and add reproducible documentation, dependencies, and CI.

**Architecture:** Update the existing miniprogram-cleanup branch from `master` in a fresh worktree, then add repository-contract tests before each consolidation change. A small Python archiver performs copy-first SHA-256 verification; the Git tree retains only code and small source inputs, while generated media and reports move to `E:\xunfang-baike-deliverables`.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3.12 standard library plus `python-docx`, Node.js 20 built-in test runner, GitHub Actions, GitHub Pages.

## Global Constraints

- The static website is the only maintained runtime product.
- Keep `auth.html`, `js/auth-config.js`, `js/auth-core.js`, `js/auth-guard.js`, `js/auth-page.js`, the cookie gate, and logout behavior unchanged.
- Document the browser-side login as a convenience barrier, not server-side access control.
- Treat website content as public; business and secrecy review are not repository release gates.
- Archive to `E:\xunfang-baike-deliverables` without silently overwriting existing files.
- Do not delete source files until archive path, size, and SHA-256 checks pass.
- Do not rewrite Git history, force-push, push any branch, or delete copied `.worktrees/` directories.
- Preserve historical files under `docs/`.
- Use Python 3.12 and Node.js 20 in CI.
- Use `unittest` and `node:test`; do not introduce `pytest` or a root Node package.
- The workflow uses `actions/checkout@v6`, `actions/setup-python@v6`, and `actions/setup-node@v6`, matching the current official action majors.

---

## File Structure

- Create `tools/archive_deliverables.py`: copy-first archive and manifest verifier.
- Create `tests/test_archive_deliverables.py`: archiver behavior tests.
- Create `tests/test_repository_consolidation.py`: repository, README, dependency, and CI contracts.
- Create `README.md`: maintainer and product documentation.
- Create `requirements.txt`: tracked Python maintenance dependency declaration.
- Create `.github/workflows/validate.yml`: push and pull-request validation.
- Create `docs/deliverables-archive.md`: archive location, verification, and restore guide.
- Generate `docs/deliverables-archive-manifest.tsv`: checked-in copy of the verified external manifest.
- Move `deliverables/xunfang-report-speaker-notes.json` to `data/xunfang-report-speaker-notes.json`.
- Move `deliverables/assets/` to `data/project-report-assets/`.
- Modify `tests/test_xunfang_report_speaker_notes.py`: consume the relocated JSON input.
- Modify `tools/generate_demo_ppt.js`: consume relocated report assets and write to the external archive.
- Modify `tools/visual_acceptance.py`: write generated screenshots to ignored `.artifacts/`.
- Modify `tests/verify_demo_ppt.py`: resolve the presentation from the external archive.
- Modify `.gitignore`: ignore archived output roots and local generated artifacts while allowing root dependency metadata.
- Delete tracked `deliverables/` and `video/` content after verified archive and source-input relocation.
- Retain the two existing miniprogram-retirement commits and their test changes.

### Task 1: Recover the cleanup branch into a fresh isolated worktree

**Files:**
- Verify only; no planned source changes.

**Interfaces:**
- Consumes: `master`, `codex/miniprogram-cleanup`, stale copied worktree registrations.
- Produces: An isolated, updated `codex/miniprogram-cleanup` worktree containing the approved design and plan.

- [ ] **Step 1: Confirm the main worktree is clean and record refs**

Run:

```powershell
git status --short --branch
git rev-parse master
git rev-parse codex/miniprogram-cleanup
git merge-base master codex/miniprogram-cleanup
git worktree list --porcelain
```

Expected: clean `master`; cleanup branch is two commits ahead and behind only by the new `master` documentation commits.

- [ ] **Step 2: Prune only stale worktree registrations**

Run:

```powershell
git worktree prune --verbose
git worktree list --porcelain
```

Expected: registrations pointing to missing `C:`/`F:` paths disappear. No directory under the copied `.worktrees/` folder is deleted.

- [ ] **Step 3: Create the isolated worktree**

Run:

```powershell
git check-ignore -q .worktrees
git worktree add .worktrees/miniprogram-cleanup-consolidation codex/miniprogram-cleanup
```

Expected: the branch is checked out at `E:\xunfang-baike\.worktrees\miniprogram-cleanup-consolidation`.

- [ ] **Step 4: Merge current master into the cleanup branch**

From the isolated worktree, run:

```powershell
git merge --no-edit master
git status --short --branch
```

Expected: a clean merge containing the latest report commit, design, and implementation plan; no remote operation.

- [ ] **Step 5: Verify the retirement baseline**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/auth_core.test.js
python tools/build_search_index.py --check
python tools/check_site_links.py
python tools/public_source_index.py check
```

Expected: all existing tests pass; `miniprogram/` and `parse_html.py` are absent.

### Task 2: Build the verified external archiver

**Files:**
- Create: `tests/test_archive_deliverables.py`
- Create: `tools/archive_deliverables.py`

**Interfaces:**
- Consumes: `--source-root`, `--archive-root`, repeated `--path` values, optional `--manifest-copy`.
- Produces: copied directory trees plus `manifest.tsv` with `sha256`, `bytes`, and POSIX relative path columns; exit `0` only after source/archive equality.

- [ ] **Step 1: Write failing archiver tests**

Create tests covering a successful copy and refusal to overwrite:

```python
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVER = ROOT / "tools" / "archive_deliverables.py"


class ArchiveDeliverablesTests(unittest.TestCase):
    def test_archives_files_and_writes_matching_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            archive = root / "archive"
            manifest_copy = root / "manifest-copy.tsv"
            (source / "deliverables").mkdir(parents=True)
            (source / "video").mkdir()
            (source / "deliverables" / "a.bin").write_bytes(b"alpha")
            (source / "video" / "b.mp4").write_bytes(b"beta")

            result = subprocess.run(
                [
                    sys.executable, str(ARCHIVER),
                    "--source-root", str(source),
                    "--archive-root", str(archive),
                    "--path", "deliverables",
                    "--path", "video",
                    "--manifest-copy", str(manifest_copy),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (archive / "deliverables" / "a.bin").read_bytes(), b"alpha"
            )
            self.assertEqual((archive / "video" / "b.mp4").read_bytes(), b"beta")
            self.assertEqual(
                (archive / "manifest.tsv").read_bytes(),
                manifest_copy.read_bytes(),
            )
            rows = (archive / "manifest.tsv").read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertEqual(rows[0], "sha256\tbytes\tpath")
            self.assertEqual(
                [row.rsplit("\t", 1)[1] for row in rows[1:]],
                ["deliverables/a.bin", "video/b.mp4"],
            )

    def test_refuses_non_empty_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            archive = root / "archive"
            (source / "deliverables").mkdir(parents=True)
            (source / "deliverables" / "a.bin").write_bytes(b"alpha")
            archive.mkdir()
            keep = archive / "keep.txt"
            keep.write_text("preserve", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable, str(ARCHIVER),
                    "--source-root", str(source),
                    "--archive-root", str(archive),
                    "--path", "deliverables",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(keep.read_text(encoding="utf-8"), "preserve")
```

Use `tempfile.TemporaryDirectory`, `subprocess.run`, and real files; do not mock filesystem calls.

- [ ] **Step 2: Run tests and verify RED**

Run:

```powershell
python -m unittest tests.test_archive_deliverables -v
```

Expected: failure because `tools/archive_deliverables.py` does not exist.

- [ ] **Step 3: Implement the minimal archiver**

Implement:

```python
def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path, names: list[str]) -> list[tuple[str, int, str]]:
    rows = []
    for name in names:
        for path in sorted((root / name).rglob("*")):
            if path.is_file():
                rows.append((
                    path.relative_to(root).as_posix(),
                    path.stat().st_size,
                    sha256_file(path),
                ))
    return rows
```

Complete the CLI with these exact behaviors:

- resolve source and archive paths;
- fail if the archive exists and contains any entry;
- require every requested source path to exist;
- copy with `shutil.copytree`;
- compare complete inventories;
- write deterministic UTF-8 `manifest.tsv`;
- optionally copy the same manifest bytes to `--manifest-copy`;
- print `ARCHIVE_OK <count> files`.

- [ ] **Step 4: Run tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_archive_deliverables -v
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: archiver tests and the complete baseline pass.

- [ ] **Step 5: Commit the archiver**

```powershell
git add -- tests/test_archive_deliverables.py tools/archive_deliverables.py
git commit -m "feat: add verified deliverable archiver"
```

### Task 3: Archive outputs and remove them from the runtime tree

**Files:**
- Create: `docs/deliverables-archive.md`
- Generate: `docs/deliverables-archive-manifest.tsv`
- Modify: `.gitignore`
- Move: `deliverables/xunfang-report-speaker-notes.json` to `data/xunfang-report-speaker-notes.json`
- Move: `deliverables/assets/` to `data/project-report-assets/`
- Modify: `tests/test_xunfang_report_speaker_notes.py`
- Modify: `tools/generate_demo_ppt.js`
- Modify: `tools/visual_acceptance.py`
- Modify: `tests/verify_demo_ppt.py`
- Delete: remaining tracked `deliverables/`
- Delete: tracked `video/`
- Modify: `tests/test_repository_consolidation.py`

**Interfaces:**
- Consumes: verified external archive and small report source inputs.
- Produces: a Git tree without runtime-output directories and tools that no longer recreate them.

- [ ] **Step 1: Write failing repository-output contracts**

Create `tests/test_repository_consolidation.py` with:

```python
class RuntimeTreeContractTests(unittest.TestCase):
    def test_generated_output_directories_are_absent(self):
        self.assertFalse((ROOT / "deliverables").exists())
        self.assertFalse((ROOT / "video").exists())

    def test_report_source_inputs_live_under_data(self):
        self.assertTrue((ROOT / "data/xunfang-report-speaker-notes.json").is_file())
        self.assertTrue((ROOT / "data/project-report-assets").is_dir())

    def test_archive_restore_document_and_manifest_exist(self):
        self.assertTrue((ROOT / "docs/deliverables-archive.md").is_file())
        self.assertTrue((ROOT / "docs/deliverables-archive-manifest.tsv").is_file())
```

- [ ] **Step 2: Run the contracts and verify RED**

Run:

```powershell
python -m unittest tests.test_repository_consolidation -v
```

Expected: failures because outputs remain and archive documents do not exist.

- [ ] **Step 3: Verify the external target is safe**

Run a read-only check for `E:\xunfang-baike-deliverables`.

Expected: path absent or empty. If non-empty, stop and compare its manifest before any write.

- [ ] **Step 4: Archive and verify all deliverables**

Run:

```powershell
python tools/archive_deliverables.py `
  --source-root E:\xunfang-baike\.worktrees\miniprogram-cleanup-consolidation `
  --archive-root E:\xunfang-baike-deliverables `
  --path deliverables `
  --path video `
  --manifest-copy docs/deliverables-archive-manifest.tsv
```

Expected: `ARCHIVE_OK` with the exact current file count. Re-run an independent SHA-256/size comparison before deletion.

- [ ] **Step 5: Relocate source inputs and update their consumers**

Move the speaker-notes JSON and four report asset PNGs out of `deliverables/`.
Update:

```python
CONTENT_PATH = ROOT / "data" / "xunfang-report-speaker-notes.json"
```

Update the presentation generator to read `data/project-report-assets/` and to write under the sibling archive root, optionally overridden by `XUNFANG_DELIVERABLES_DIR`. Update visual-acceptance output to `.artifacts/visual-acceptance`, and resolve the optional PPT verifier from `XUNFANG_DELIVERABLES_DIR`.

- [ ] **Step 6: Add archive documentation and ignore rules**

Document the archive path, manifest columns, verification command, restore-by-copy procedure, and Git-history fallback in `docs/deliverables-archive.md`.

Add exact ignore entries:

```gitignore
deliverables/
video/
.artifacts/
```

Remove the broad `package.json` and `package-lock.json` ignore entries only if they block future tracked dependency metadata; do not add a root Node package in this task.

- [ ] **Step 7: Remove verified output trees**

After resolving the exact isolated-worktree paths, run:

```powershell
git rm -r -- deliverables video
```

The moved source files must appear as renames or additions, and the external archive must remain unchanged.

- [ ] **Step 8: Run focused tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_repository_consolidation -v
python -m unittest tests.test_xunfang_report_speaker_notes -v
node --check tools/generate_demo_ppt.js
python tools/check_site_links.py
git diff --check
```

Expected: all checks pass and no runtime page references either removed directory.

- [ ] **Step 9: Commit the archive split**

```powershell
git add -- .gitignore data docs tests tools
git add -u -- deliverables video
git commit -m "refactor: move deliverables outside runtime repository"
```

### Task 4: Add README and dependency declaration

**Files:**
- Create: `README.md`
- Create: `requirements.txt`
- Modify: `tests/test_repository_consolidation.py`

**Interfaces:**
- Consumes: final static-site product and archive boundaries.
- Produces: reproducible local setup and maintenance instructions.

- [ ] **Step 1: Add failing documentation contracts**

Add tests asserting that README contains exact command fragments for local
preview, Python tests, Node tests, search, links, and public-source checks; also
assert it mentions GitHub Pages, `CNAME`, `.nojekyll`, the external archive,
retired miniprogram, public content, and the client-side-only login boundary.

Add a dependency contract:

```python
requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
self.assertIn("python-docx", requirements)
self.assertNotIn("pytest", requirements.lower())
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```powershell
python -m unittest tests.test_repository_consolidation -v
```

Expected: failures because README and requirements do not exist.

- [ ] **Step 3: Write README and requirements**

Use:

```text
python-docx>=1.1,<2
```

README must not include the configured username, digest, password, `.env`
values, or OSS keys. It must clearly distinguish source maintenance from
generated deliverables.

Use these headings and commands:

```markdown
# 巡防百科

## 项目定位
## 目录结构
## 环境要求
## 本地预览
python -m http.server 8000
## 安装维护依赖
python -m pip install -r requirements.txt
## 完整验证
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/auth_core.test.js
python tools/build_search_index.py --check
python tools/check_site_links.py
python tools/public_source_index.py check
## 内容维护
## 部署
## 登录边界
## 外部交付物
## 已退役的小程序
```

- [ ] **Step 4: Run tests and verify GREEN**

Run:

```powershell
python -m unittest tests.test_repository_consolidation -v
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: all tests pass with only the two existing feature-placeholder skips.

- [ ] **Step 5: Commit documentation and dependencies**

```powershell
git add -- README.md requirements.txt tests/test_repository_consolidation.py
git commit -m "docs: add repository setup and maintenance guide"
```

### Task 5: Add GitHub Actions validation

**Files:**
- Create: `.github/workflows/validate.yml`
- Modify: `tests/test_repository_consolidation.py`

**Interfaces:**
- Consumes: README commands and `requirements.txt`.
- Produces: push/PR validation on Python 3.12 and Node.js 20.

- [ ] **Step 1: Add a failing CI structure contract**

Assert the workflow contains:

```python
required = (
    "actions/checkout@v6",
    "actions/setup-python@v6",
    "python-version: '3.12'",
    "actions/setup-node@v6",
    "node-version: '20'",
    'python -m unittest discover -s tests -p "test_*.py" -v',
    "node --test tests/auth_core.test.js",
    "python tools/build_search_index.py --check",
    "python tools/check_site_links.py",
    "python tools/public_source_index.py check",
)
```

Also assert the workflow triggers on both `push` and `pull_request`.

- [ ] **Step 2: Run the contract and verify RED**

Run:

```powershell
python -m unittest tests.test_repository_consolidation -v
```

Expected: failure because `.github/workflows/validate.yml` does not exist.

- [ ] **Step 3: Create the workflow**

Create this workflow:

```yaml
name: Validate

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    env:
      TMPDIR: ${{ runner.temp }}/xunfang-tests
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: '3.12'
          cache: pip
      - name: Install Python dependencies
        run: python -m pip install -r requirements.txt
      - uses: actions/setup-node@v6
        with:
          node-version: '20'
      - name: Prepare test temp directory
        run: mkdir -p "$TMPDIR"
      - name: Run Python tests
        run: python -m unittest discover -s tests -p "test_*.py" -v
      - name: Run Node tests
        run: node --test tests/auth_core.test.js
      - name: Check generated search index
        run: python tools/build_search_index.py --check
      - name: Check local links
        run: python tools/check_site_links.py
      - name: Check public source index
        run: python tools/public_source_index.py check
```

- [ ] **Step 4: Run tests and syntax-oriented checks**

Run:

```powershell
python -m unittest tests.test_repository_consolidation -v
git diff --check
```

Expected: the CI contract passes and YAML has no tab characters or placeholder values.

- [ ] **Step 5: Commit CI**

```powershell
git add -- .github/workflows/validate.yml tests/test_repository_consolidation.py
git commit -m "ci: validate static site content and structure"
```

### Task 6: Full verification and local master integration

**Files:**
- Verify only; no planned source changes.

**Interfaces:**
- Consumes: completed `codex/miniprogram-cleanup`.
- Produces: clean local `master` with the consolidated static-site repository.

- [ ] **Step 1: Verify external archive again**

Compare `E:\xunfang-baike-deliverables\manifest.tsv` with
`docs/deliverables-archive-manifest.tsv`, then independently hash every archived
file.

Expected: identical path, size, hash, and file count; no missing or extra files.

- [ ] **Step 2: Run complete verification**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/auth_core.test.js
python tools/build_search_index.py --check
python tools/check_site_links.py
python tools/public_source_index.py check
git diff --check
git status --short --branch
```

Expected: all tests and checks pass, only the intentional feature-placeholder skips remain, and the cleanup worktree is clean.

- [ ] **Step 3: Review the branch range**

Run:

```powershell
git log --oneline master..codex/miniprogram-cleanup
git diff --stat master..codex/miniprogram-cleanup
git diff --name-status master..codex/miniprogram-cleanup
```

Expected: miniprogram retirement, archive split, documentation, dependencies,
and CI only; no authentication removal and no copied `.worktrees/` deletion.

- [ ] **Step 4: Merge locally into master**

From `E:\xunfang-baike`, run:

```powershell
git status --short --branch
git merge --no-ff codex/miniprogram-cleanup
```

Expected: local merge succeeds. Do not push.

- [ ] **Step 5: Verify merged master fresh**

Repeat the complete verification commands from Step 2 in the main worktree and
verify:

```powershell
Test-Path miniprogram
Test-Path parse_html.py
Test-Path deliverables
Test-Path video
git status --short --branch
```

Expected: all four paths are absent, tests pass, `master` is clean and ahead of
`origin/master`, and the external archive remains verified.
