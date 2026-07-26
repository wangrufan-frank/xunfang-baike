# Static Site Repository Consolidation Design

## Goal

Consolidate the repository around the static website as its only maintained
runtime product, preserve the existing public-facing login gate, move
non-runtime deliverables out of the code checkout, and add reproducible
maintenance and continuous-integration entry points.

## Product Boundary

The static HTML/CSS/JavaScript website is the only maintained runtime product.
The WeChat miniprogram and its website-to-miniprogram conversion script are
retired. Historical design and implementation documents remain in Git.

The website is treated as public content. Business and secrecy review are not
release gates for this repository. The existing browser-side login page,
credential digest, cookie, guard, and logout control remain unchanged because
the owner wants to retain the login experience. Repository documentation must
state that this client-side gate is a convenience barrier rather than
server-side access control.

## Branch Integration

The existing `codex/miniprogram-cleanup` branch contains two commits that
retire `miniprogram/`, remove `parse_html.py`, and clean active tooling
references. It is two commits ahead of its merge base and one commit behind
`master`.

Copied Git metadata contains stale worktree registrations whose original paths
no longer exist. Implementation will prune only those stale registrations,
create a fresh isolated worktree for `codex/miniprogram-cleanup`, merge the
current `master` into that branch, and run the complete baseline verification.
No copied `.worktrees/` directory will be deleted because it may contain
uncommitted files from the old computer.

All new repository-consolidation changes will be made on
`codex/miniprogram-cleanup`. After verification, the branch will be merged
locally into `master`. Remote pushing is outside this scope.

## Deliverable Archive

The runtime site does not reference files under `deliverables/` or `video/`.
Both directories will be archived outside the repository at:

```text
E:\xunfang-baike-deliverables
```

The archive process is copy-first:

1. Refuse to overwrite an existing non-empty archive without an explicit,
   verified merge strategy.
2. Copy the complete `deliverables/` and `video/` directory trees.
3. Produce a UTF-8 manifest containing relative path, byte size, and SHA-256
   digest for every archived file.
4. Compare source and archive manifests byte-for-byte.
5. Only after the comparison succeeds, remove the two directories from the
   current Git tree.
6. Keep a repository document that records the archive location, manifest
   format, restoration procedure, and the fact that old Git commits still
   contain the files.
7. Ignore `deliverables/` and `video/` so archived outputs are not accidentally
   recommitted.

This change does not rewrite Git history. It prevents continued growth and
removes the files from future checkouts after a fresh clone, but the current
`.git` object database will remain large until a separately approved history
rewrite and garbage-collection operation is performed.

## Repository Documentation

A root `README.md` will document:

- the public static-site product boundary;
- the six content modules and major data stores;
- supported local runtime versions;
- local preview using Python's standard HTTP server;
- the complete test and validation commands;
- content, search-index, legal-library, and public-source maintenance flow;
- GitHub Pages publishing files (`CNAME` and `.nojekyll`);
- the retained client-side login gate and its security limitation;
- the external deliverable archive and restoration process;
- the retired miniprogram and its recovery through Git history.

The README must not include passwords, credential digests, `.env` values, or
OSS credentials.

## Dependency Declaration

The site itself has no build-time or runtime package dependency. Maintenance
tools use Python 3.12 and Node.js 20.

A root Python requirements file will declare only third-party packages needed
by tracked maintenance and verification scripts. Core tests continue to use
`unittest`; `pytest` is not required. Node tests continue to use the built-in
`node:test` runner, so no root `package.json` is introduced.

Dependency versions will use bounded compatible ranges rather than unbounded
latest versions. The existing ignored local `oss_upload.py` helper and its
credentials are outside the tracked project and do not determine repository
dependencies.

## Continuous Integration

Create a GitHub Actions workflow triggered for pushes and pull requests. It
will use Ubuntu, Python 3.12, and Node.js 20, install the root Python
requirements, and run:

1. `python -m unittest discover -s tests -p "test_*.py" -v`
2. `node --test tests/auth_core.test.js`
3. `python tools/build_search_index.py --check`
4. `python tools/check_site_links.py`
5. `python tools/public_source_index.py check`

The workflow will use a repository-local temporary directory for tests that
generate legal pages. It must not regenerate tracked outputs or modify the
external archive.

## Tests and Repository Contracts

Tests will define the intended repository state before implementation:

- `miniprogram/` and `parse_html.py` remain absent;
- active tooling no longer targets the miniprogram;
- `deliverables/` and `video/` remain absent from the Git working tree;
- archive documentation and the external manifest contract exist;
- README includes setup, testing, deployment, public-access, login-boundary,
  archive, and retirement guidance;
- the CI workflow contains every required validation command;
- declared dependencies cover imports used by tracked maintenance scripts.

Configuration-only GitHub Actions syntax will be checked structurally by a
Python repository-contract test. The full existing test suite, Node tests,
search-index check, link checker, public-source check, and `git diff --check`
must pass before local integration into `master`.

## Safety and Recovery

- The source worktree must be clean before branch integration.
- Existing files in `E:\xunfang-baike-deliverables` are never overwritten
  silently.
- File removal occurs only after SHA-256 and size verification.
- No `.env` file or credential value is copied into documentation or CI.
- No Git history rewrite, force push, remote push, or deletion of copied stale
  worktree directories occurs in this work.
- Removed runtime and deliverable files remain recoverable from Git history;
  archived deliverables also remain recoverable from the external verified
  copy.

## Success Criteria

The work is complete when:

- `master` contains the verified miniprogram-retirement commits;
- the static website is the only maintained runtime product;
- the login experience remains unchanged and is accurately documented;
- `deliverables/` and `video/` are present in the verified external archive and
  absent from the current Git tree;
- README, dependency declaration, and GitHub Actions CI are present;
- all repository and content validation commands pass;
- the local `master` worktree is clean;
- no remote push has occurred.
