# Auth and Learning Modules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a 24-hour client-side common login, an original patrol-themed login background, and three independently displayed static learning modules for onboarding, assessment standards, and discipline study.

**Architecture:** Keep the existing static HTML/CSS/vanilla-JavaScript site. Isolate authentication into a small browser core plus page guard, and generate only the three new modules from one validated UTF-8 JSON catalog so their page structure, sources, search records, and previous/next links remain consistent. Commit generated HTML because the current deployment serves repository files directly.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, Node.js 26 built-in test runner, Python 3.12 standard library, `unittest`, ImageGen

## Global Constraints

- Repository root: `F:\frank第二大脑\xunfang-baike`.
- Preserve the existing HTML/CSS/vanilla-JavaScript architecture; do not rebuild old modules.
- Do not modify the WeChat mini-program in this work.
- Do not publish or change external deployment state.
- The login is a convenience gate, not a confidentiality or security boundary.
- The common username is `xunfang`; do not store the agreed plaintext password in any new source, test, plan, or generated file.
- The accepted credential digest is SHA-256 of `username + ':' + password`: `41a633bb0a7ccf378ce69ee4ecea91239f04c3a69d3e567dc23bddcbfeae840e`.
- The session lifetime is exactly 86,400 seconds, with `Path=/`, `SameSite=Lax`, and `Secure` on HTTPS.
- After successful login, return only to a validated same-origin page; reject external, protocol-relative, script, and malformed redirects.
- Show `rumen`, `kaohe`, and `jilv` as three independent homepage cards and three independent navigation links; do not group them.
- Onboarding has five ordered stages and no saved progress, score, ranking, or personal data.
- Assessment and discipline each contain exactly six first-release pages, within the approved range of four to six.
- New factual content must use verified public authoritative sources, source cards, HTTPS links, publisher, title, publication date, verification date, and update date.
- Do not invent or publish non-public municipal or detachment thresholds, scoring tables, processes, training material, tactical steps, deployment patterns, or sensitive equipment detail.
- Use no third-party runtime libraries, remote fonts, analytics, trackers, or external scripts.
- Keep the user's untracked `公安警察工作汇报PPT.pptx` untouched.

---

## File Responsibility Map

- `js/auth-core.js`: pure hashing, cookie, session, and redirect helpers usable by browser and Node tests.
- `js/auth-config.js`: non-secret common username, accepted digest, cookie name, and 86,400-second lifetime.
- `js/auth-guard.js`: early protected-page redirect and content reveal.
- `js/auth-page.js`: login form behavior and validated return navigation.
- `tools/inject_auth_guard.py`: idempotently inserts root-aware guard tags into existing HTML.
- `auth.html`: accessible login markup only; no embedded credential logic.
- `img/auth-patrol-night.webp` and `img/auth-patrol-night.jpg`: generated responsive background assets.
- `data/learning-modules.json`: sources and all copy for the three new modules.
- `tools/learning_modules.py`: validation, safe rendering, generated-page writing, and search-record creation.
- `tools/build_learning_modules.py`: CLI entry point for catalog validation and page generation.
- `rumen/`, `kaohe/`, `jilv/`: generated static module indexes and article pages.
- `tools/update_search_index.py`: idempotently replaces generated-module records in `search-index.json`.
- `js/nav.js`, `js/search.js`, `index.html`, `css/style.css`: shared navigation, search depth, homepage entries, route and article styling.
- `tests/auth_core.test.js`: executable JavaScript unit tests.
- `tests/test_auth_integration.py`: login and protected-page HTML contracts.
- `tests/test_learning_modules.py`: catalog, rendering, source, content-safety, and search contracts.
- `tests/test_auth_background.py`: background file and fallback-style contract.

---

### Task 1: Authentication core

**Files:**
- Create: `js/auth-core.js`
- Create: `js/auth-config.js`
- Create: `tests/auth_core.test.js`

**Interfaces:**
- Produces: `XunfangAuth.sha256(text) -> Promise<string>`, `digestCredentials(username, password) -> Promise<string>`, `sanitizeRedirect(value, origin) -> string`, `hasSession(cookieText, config) -> boolean`, `buildSessionCookie(config, secure) -> string`, and `buildExpiredCookie(config, secure) -> string`.
- Consumes: `XunfangAuthConfig = { username, digest, cookieName, maxAgeSeconds }`.

- [ ] **Step 1: Write failing JavaScript unit tests**

Create tests using only `node:test` and `node:assert/strict`:

```js
const test = require('node:test');
const assert = require('node:assert/strict');
const auth = require('../js/auth-core.js');
const config = require('../js/auth-config.js');

test('hashes username and password with an unambiguous separator', async () => {
    const digest = await auth.digestCredentials('demo', 'value');
    assert.equal(digest, await auth.sha256('demo:value'));
});

test('accepts only same-origin redirects', () => {
    const origin = 'https://www.xunfangbk.cn';
    assert.equal(auth.sanitizeRedirect('/kaohe/index.html?q=1#top', origin), '/kaohe/index.html?q=1#top');
    for (const value of ['https://example.com/', '//example.com/', 'javascript:alert(1)', '%%%']) {
        assert.equal(auth.sanitizeRedirect(value, origin), '/index.html');
    }
});

test('session cookie lasts one day and expires cleanly', () => {
    assert.match(auth.buildSessionCookie(config, true), /Max-Age=86400; Path=\/; SameSite=Lax; Secure/);
    assert.match(auth.buildExpiredCookie(config, false), /Max-Age=0; Path=\/; SameSite=Lax/);
});

test('session requires the exact configured token', () => {
    assert.equal(auth.hasSession('other=1; xunfang_auth=' + config.digest, config), true);
    assert.equal(auth.hasSession('xunfang_auth=wrong', config), false);
});
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `node --test tests/auth_core.test.js`  
Expected: FAIL because `js/auth-core.js` and `js/auth-config.js` do not exist.

- [ ] **Step 3: Implement the pure authentication core and immutable config**

Use a UMD-style export so the same functions are available as `window.XunfangAuth` in browsers and `module.exports` in Node. `sha256` must call `globalThis.crypto.subtle.digest('SHA-256', new TextEncoder().encode(text))`. `sanitizeRedirect` must construct `new URL(value, origin)`, require `target.origin === origin`, require `http:` or `https:`, and return `pathname + search + hash`; every exception returns `/index.html`. Cookie builders URL-encode the configured digest and include the exact attributes tested above.

`js/auth-config.js` must contain only:

```js
var XunfangAuthConfig = Object.freeze({
    username: 'xunfang',
    digest: '41a633bb0a7ccf378ce69ee4ecea91239f04c3a69d3e567dc23bddcbfeae840e',
    cookieName: 'xunfang_auth',
    maxAgeSeconds: 86400
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = XunfangAuthConfig;
}
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run: `node --test tests/auth_core.test.js`  
Expected: 4 tests pass, 0 fail.

- [ ] **Step 5: Commit**

```powershell
git add js/auth-core.js js/auth-config.js tests/auth_core.test.js
git commit -m "feat: add client auth core"
```

### Task 2: Protected-page guard and login behavior

**Files:**
- Create: `js/auth-guard.js`
- Create: `js/auth-page.js`
- Create: `tools/inject_auth_guard.py`
- Create: `tests/test_auth_integration.py`
- Modify: `auth.html`
- Modify: every runtime `.html` file except `auth.html` by running the injector
- Modify: `js/nav.js`

**Interfaces:**
- Consumes: `XunfangAuth`, `XunfangAuthConfig`, and `data-root` on the guard script.
- Produces: early same-site redirect, 24-hour login, `window.XunfangLogout()`, and idempotent HTML injection.

- [ ] **Step 1: Write failing integration tests**

The Python test must discover runtime HTML while excluding `.git`, `.worktrees`, `.superpowers`, `deliverables`, and `docs`. Assert:

```python
def test_every_runtime_page_except_auth_loads_guard_in_head(self):
    for page in runtime_html_pages():
        if page.name == 'auth.html' and page.parent == ROOT:
            continue
        html = page.read_text(encoding='utf-8')
        head = html.split('</head>', 1)[0]
        self.assertIn('auth-config.js', head, page)
        self.assertIn('auth-core.js', head, page)
        self.assertIn('auth-guard.js', head, page)

def test_auth_page_has_accessible_account_password_controls(self):
    html = (ROOT / 'auth.html').read_text(encoding='utf-8')
    for value in ('id="username"', 'id="password"', 'id="toggle-password"',
                  'id="submit"', 'aria-live="polite"', 'js/auth-page.js'):
        self.assertIn(value, html)

def test_plaintext_password_is_absent_from_new_runtime_sources(self):
    for path in [ROOT / 'js' / name for name in ('auth-config.js', 'auth-core.js', 'auth-guard.js', 'auth-page.js')]:
        self.assertNotIn('150225', path.read_text(encoding='utf-8'))
```

Also unit-test `inject_html(html, root_prefix)` using a temporary HTML string: root pages receive `js/...`, nested pages receive `../js/...`, reinjection is byte-identical, and `auth.html` is skipped by the CLI.

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m unittest tests.test_auth_integration -v`  
Expected: failures for missing guard, form controls, scripts, and injector.

- [ ] **Step 3: Implement the early guard and idempotent injector**

The injector adds these synchronous scripts before `</head>` and computes `data-root=""` for root pages and `data-root="../"` for one-level module pages:

```html
<script src="ROOTjs/auth-config.js"></script>
<script src="ROOTjs/auth-core.js"></script>
<script src="ROOTjs/auth-guard.js" data-root="ROOT"></script>
```

`auth-guard.js` must immediately set `document.documentElement.classList.add('auth-pending')`. If `hasSession(document.cookie, config)` is true, remove the class; otherwise build `root + 'auth.html?redirect=' + encodeURIComponent(location.pathname + location.search + location.hash)` and call `location.replace(...)`.

- [ ] **Step 4: Replace embedded login logic with form-only markup and `auth-page.js`**

`auth-page.js` must compare the trimmed username to `config.username`, compare `await digestCredentials(username, password)` to `config.digest`, write `buildSessionCookie(config, location.protocol === 'https:')`, sanitize the `redirect` query value against `location.origin`, and call `location.replace(target)`. It must disable the button while hashing, use the single error text `账号或密码错误`, clear only the password on failure, support Enter, toggle `type="password"`/`type="text"`, and display a compatibility error when Web Crypto is unavailable.

- [ ] **Step 5: Add logout to shared navigation**

Expose this exact behavior from `js/nav.js`:

```js
window.XunfangLogout = function() {
    document.cookie = window.XunfangAuth.buildExpiredCookie(
        window.XunfangAuthConfig,
        window.location.protocol === 'https:'
    );
    window.location.replace(rootPrefix + 'auth.html');
};
```

Render a `<button type="button" class="logout-button">退出登录</button>` next to the theme control. Derive `rootPrefix` from the same module-depth logic used for links.

- [ ] **Step 6: Run the injector, then verify GREEN**

Run:

```powershell
python tools/inject_auth_guard.py
python -m unittest tests.test_auth_integration -v
node --test tests/auth_core.test.js
```

Expected: injector reports every protected runtime page once; all Python and Node tests pass. Running the injector again reports 0 changes.

- [ ] **Step 7: Commit**

```powershell
git add auth.html js/auth-guard.js js/auth-page.js js/nav.js tools/inject_auth_guard.py tests/test_auth_integration.py index.html search.html fagui jingqing meiyueyixue qinwu xunlian zhuangbei zoufang
git commit -m "feat: protect static pages with common login"
```

### Task 3: Original patrol login background

**Files:**
- Create: `img/auth-patrol-night.webp`
- Create: `img/auth-patrol-night.jpg`
- Create: `tests/test_auth_background.py`
- Modify: `auth.html`

**Interfaces:**
- Produces: responsive login artwork with WebP, JPEG, and CSS gradient fallback.

- [ ] **Step 1: Write a failing asset contract test**

```python
def test_login_background_has_two_nonempty_formats_and_fallback(self):
    webp = ROOT / 'img' / 'auth-patrol-night.webp'
    jpeg = ROOT / 'img' / 'auth-patrol-night.jpg'
    self.assertGreater(webp.stat().st_size, 50_000)
    self.assertGreater(jpeg.stat().st_size, 50_000)
    html = (ROOT / 'auth.html').read_text(encoding='utf-8')
    self.assertIn("url('img/auth-patrol-night.webp')", html)
    self.assertIn("url('img/auth-patrol-night.jpg')", html)
    self.assertIn('linear-gradient(', html)
    self.assertIn('@media (prefers-reduced-motion: reduce)', html)
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python -m unittest tests.test_auth_background -v`  
Expected: file-not-found failure.

- [ ] **Step 3: Use the `imagegen` skill to generate the original artwork**

Use this prompt without adding real insignia or text:

```text
Create a cinematic 16:9 website login background for a Chinese public-safety patrol learning site. Nighttime modern city street after light rain, a generic patrol vehicle with soft police-blue reflected light, and several special-police patrol silhouettes walking calmly on the right third of the frame. Keep the left third visually quiet and dark for a login card. Deep navy, cool white, subtle warm amber streetlights, realistic but restrained documentary mood. No readable text, no logos, no real unit insignia, no license plates, no identifiable faces, no close-up weapons, no tactical formation diagram, no violence. Wide composition, strong negative space, web-background friendly.
```

Inspect the result before accepting it. Export the accepted image to WebP quality 82 and JPEG quality 86, keeping the same dimensions and sRGB color space.

- [ ] **Step 4: Implement responsive login styling**

Use layered backgrounds in this order: dark left-to-right gradient, WebP, JPEG, and solid police-blue. Place the card left on screens wider than 760px and center it below that breakpoint. Add `backdrop-filter: blur(14px)` with an opaque `rgba(255,255,255,.94)` fallback, visible focus outlines, minimum 44px controls, and no repeating animation.

- [ ] **Step 5: Run the test and visually verify**

Run: `python -m unittest tests.test_auth_background -v`  
Expected: PASS. Open `auth.html` through a local HTTP server at desktop width and 390px width; confirm the figures remain on the right, the form is readable, and disabling either image URL still leaves a usable gradient.

- [ ] **Step 6: Commit**

```powershell
git add auth.html img/auth-patrol-night.webp img/auth-patrol-night.jpg tests/test_auth_background.py
git commit -m "feat: add patrol login artwork"
```

### Task 4: Validated learning catalog and static renderer

**Files:**
- Create: `data/learning-modules.json`
- Create: `tools/learning_modules.py`
- Create: `tools/build_learning_modules.py`
- Create: `tests/test_learning_modules.py`

**Interfaces:**
- Produces: `load_catalog(path: Path) -> dict`, `validate_catalog(catalog: dict) -> list[str]`, `render_module_index(module: dict) -> str`, `render_article(module: dict, article: dict, previous: dict | None, next_: dict | None) -> str`, `build_pages(root: Path, catalog: dict) -> list[Path]`, and `generated_search_records(catalog: dict) -> list[dict]`.
- Consumes: UTF-8 JSON with `version`, `verified_at`, `sources`, and `modules`.

- [ ] **Step 1: Write failing catalog and rendering tests**

The fixture catalog must contain one source, one module, and one article. Tests must reject missing fields, non-HTTPS sources, duplicate source IDs, duplicate module/article slugs, dangling `source_ids`, invalid ISO dates, empty sections, raw HTML in content strings, and unknown module slugs. Assert HTML escaping, semantic `header/nav/main/footer`, guard scripts in `<head>`, source cards, safe external-link attributes, breadcrumb, update date, quiz markup, and previous/next links.

```python
def test_renderer_escapes_catalog_text_and_adds_source_disclosure(self):
    article = valid_article()
    article['summary'] = '<script>alert(1)</script>'
    html = MODULE.render_article(valid_module(article), article, None, None)
    self.assertNotIn('<script>alert(1)</script>', html)
    self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)
    self.assertIn('公开资料来源', html)
    self.assertIn('target="_blank" rel="noopener noreferrer"', html)
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m unittest tests.test_learning_modules -v`  
Expected: import failure because `tools/learning_modules.py` does not exist.

- [ ] **Step 3: Implement strict validation and escaped templates**

Allow only module slugs `rumen`, `kaohe`, and `jilv`. Article fields are exactly `slug`, `number`, `title`, `stage`, `summary`, `reading_minutes`, `tags`, `keywords`, `updated_at`, `source_ids`, `sections`, and `quiz`. A section has `title`, `lead`, and `body`; a quiz has `question`, `options`, `answer_index`, and `explanation`. Escape every string with `html.escape`; never accept raw HTML from JSON.

All generated pages must load `../css/style.css`, the three auth scripts in `<head>`, then `theme.js`, `nav.js`, `main.js`, and `search.js` at the end of `<body>`. `build_pages` writes atomically through sibling temporary files and removes only stale generated `.html` files listed in a `.generated-learning-pages.json` manifest.

- [ ] **Step 4: Implement the CLI and minimal valid seed catalog**

`python tools/build_learning_modules.py --check` validates without writing. The normal command validates, writes pages, writes the generated-file manifest, and prints counts. Seed the catalog with the exact source records listed in Task 5 and empty module article arrays only long enough for the renderer unit tests; Task 5 immediately adds the required real records before any release build.

- [ ] **Step 5: Run renderer tests and verify GREEN**

Run: `python -m unittest tests.test_learning_modules -v`  
Expected: renderer and validation unit tests pass.

- [ ] **Step 6: Commit**

```powershell
git add data/learning-modules.json tools/learning_modules.py tools/build_learning_modules.py tests/test_learning_modules.py
git commit -m "feat: add learning module generator"
```

### Task 5: Public source records and five-stage onboarding guide

**Files:**
- Modify: `data/learning-modules.json`
- Modify: `tests/test_learning_modules.py`
- Generate: `rumen/index.html`
- Generate: `rumen/01-gangwei-renshi.html`
- Generate: `rumen/02-zhize-bianjie.html`
- Generate: `rumen/03-jilv-baomi.html`
- Generate: `rumen/04-qinwu-goutong.html`
- Generate: `rumen/05-fuxi-zice.html`

**Interfaces:**
- Produces: five ordered onboarding records and reusable verified source metadata.

- [ ] **Step 1: Add failing exact-coverage tests**

Assert `rumen` has exactly five articles with numbers `01` through `05`, stages 1 through 5, the exact slugs above, nonempty quiz data, at least one source per article, and complete previous/next navigation after rendering.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_learning_modules.LearningCatalogInventoryTests.test_onboarding_has_five_ordered_stages -v`  
Expected: FAIL because the guide articles are absent.

- [ ] **Step 3: Add these exact authoritative source records**

Use verification date `2026-07-16`:

| Source ID | Title | Publisher/platform | Publication date | HTTPS URL |
|---|---|---|---|---|
| `official-peoples-police-law-2012` | 中华人民共和国人民警察法（2012年修正本） | 全国人大常委会 / 武汉市公安局 | 2019-08-09 | `https://gaj.wuhan.gov.cn/zwgk_12/zcfg/flfg/202001/t20200108_659553.html` |
| `official-training-regulation-2024` | 公安机关人民警察训练条令 | 公安部 / 司法部 | 2024-12-06 | `https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/202510/t20251021_526539.html` |
| `official-internal-affairs-regulation-2021` | 公安机关人民警察内务条令（公安部令第161号） | 公安部 / 中国政府网国务院公报 | 2021-10-28 | `https://www.gov.cn/gongbao/content/2022/content_5671112.htm` |
| `official-discipline-regulation-2010` | 公安机关人民警察纪律条令 | 监察部、人社部、公安部 / 司法部 | 2010-04-21 | `https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/201007/t20100728_144862.html` |
| `official-secrecy-law-2024` | 中华人民共和国保守国家秘密法（2024修订） | 全国人大常委会 / 中国人大网 | 2024-02-27 | `https://www.npc.gov.cn/npc/c2/c30834/202402/t20240227_434859.html` |
| `official-police-ethics` | 公安机关人民警察职业道德规范 | 公安部 / 上海市公安局 | leave the source's absent publication date as `null` | `https://gaj.sh.gov.cn/shga/qlqd/listDetail?pa=27cfd74b74a643431d6156e2523ce5313e1d3df707e0accfcf7db2c1d1be1d0cce7860a72f32e44f4f8d5649415718f5` |

Validation must allow `published_at: null` only when the official page does not expose a date; the rendered source card displays `发布日期：页面未标注`.

- [ ] **Step 4: Add the five guide records with bounded content**

Use these titles and learning outcomes:

| No. | Title | Required content boundary |
|---|---|---|
| 01 | 认识巡防岗位 | Explain public-service purpose, lawful duty, teamwork, and the guide's limits; no deployment or patrol-pattern detail. |
| 02 | 明确职责与权限边界 | Explain acting under law, identity, rights protection, requesting instruction, and not extending powers by assumption. |
| 03 | 纪律要求与保密意识 | Explain discipline, work-secret aggregation risk, social-media caution, and the rule that public fragments are not automatically safe to compile. |
| 04 | 勤务基础与群众沟通 | Explain preparation principles, listening, calm explanation, respectful language, accurate recording, and timely reporting; no operational procedure. |
| 05 | 综合复习与入门自测 | Summarize the first four lessons and provide a five-question non-tactical self-test with explanations. |

Every article must include sections named `学习目标`, `核心要点`, `常见误区`, and `请示与正式培训边界`, plus one quiz. Use original paraphrase, not copied regulatory paragraphs.

- [ ] **Step 5: Build pages and verify GREEN**

Run:

```powershell
python tools/build_learning_modules.py
python -m unittest tests.test_learning_modules -v
```

Expected: six `rumen` HTML files generated; all catalog tests pass.

- [ ] **Step 6: Commit**

```powershell
git add data/learning-modules.json rumen tests/test_learning_modules.py .generated-learning-pages.json
git commit -m "feat: add patrol onboarding guide"
```

### Task 6: Assessment standards module

**Files:**
- Modify: `data/learning-modules.json`
- Modify: `tests/test_learning_modules.py`
- Generate: `kaohe/index.html` and six `kaohe/*.html` article pages

**Interfaces:**
- Produces: six public-source assessment articles without unpublished thresholds.

- [ ] **Step 1: Add a failing assessment inventory and safety test**

Assert these exact slugs exist: `mokuai-shuoming`, `xunlian-guifan-daodu`, `lilun-kaohe-renzhi`, `tineng-kaohe-renzhi`, `jineng-kaohe-renzhi`, `richang-xunlian-zhunbei`. Assert each record cites `official-training-regulation-2024`, and scan all assessment text to reject `市局统一分值`, `支队内部标准`, `内部评分表`, `秘密`, any `及格线` followed by a number, and any unreferenced numeric performance threshold.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_learning_modules.LearningCatalogInventoryTests.test_assessment_has_six_safe_articles -v`  
Expected: FAIL because the assessment records are absent.

- [ ] **Step 3: Add six articles with exact scope**

- `考核标准模块说明`: explain that the module is a public-document orientation and local current formal rules prevail.
- `公开训练规范导读`: explain training types, rights and duties, management, examination, and training records from the 2024 regulation.
- `理论学习考核认知`: explain why political theory, law/policy application, and professional knowledge may be assessed; publish no question bank.
- `基础体能考核认知`: explain safe preparation, gradual practice, health reporting, warm-up, recovery, and organization-specific standards; publish no threshold.
- `警务技能考核认知`: explain safety, legality, standardization, judgment, and formal instructor assessment; publish no tactical instructions or scoring rubric.
- `日常训练与考核准备`: explain attendance, honest records, reflection, equipment checks at principle level, rest, injury reporting, and following organizers' notices.

Each page uses the approved uniform article sections, an original non-tactical quiz, `updated_at: 2026-07-16`, and the visible statement `具体要求以本单位最新正式规定和组织安排为准`.

- [ ] **Step 4: Build and verify GREEN**

Run:

```powershell
python tools/build_learning_modules.py
python -m unittest tests.test_learning_modules -v
```

Expected: seven `kaohe` pages generated and all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add data/learning-modules.json kaohe tests/test_learning_modules.py .generated-learning-pages.json
git commit -m "feat: add assessment standards module"
```

### Task 7: Discipline study module

**Files:**
- Modify: `data/learning-modules.json`
- Modify: `tests/test_learning_modules.py`
- Generate: `jilv/index.html` and six `jilv/*.html` article pages

**Interfaces:**
- Produces: six public-source discipline articles with source and update disclosures.

- [ ] **Step 1: Add a failing discipline inventory test**

Assert these exact slugs exist: `mokuai-shuoming`, `zhiye-jilv-daodu`, `neiwu-xingwei-guifan`, `baomi-wangluo-jilv`, `zhiqin-lvzhi-jilv`, `wuru-zice`. Assert each article has at least one of the discipline, internal-affairs, secrecy, ethics, or People's Police Law source IDs and contains no copied paragraph longer than 80 Chinese characters from any source summary stored in the fixture.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_learning_modules.LearningCatalogInventoryTests.test_discipline_has_six_sourced_articles -v`  
Expected: FAIL because discipline records are absent.

- [ ] **Step 3: Add six articles with exact scope**

- `纪律学习模块说明`: explain public-source scope, learning purpose, and the need to follow current unit rules.
- `人民警察职业纪律导读`: explain loyalty to law and duty, impartiality, obedience to lawful orders, integrity, and accountability at a principle level.
- `内务与日常行为规范`: explain order, appearance, professional language, public service, frugality, and collective responsibility using the current public internal-affairs regulation.
- `保密与网络使用纪律`: explain state secrets, work secrets, minimum-necessary sharing, social-media caution, metadata, and aggregation risk; include no hidden security measure.
- `执勤履职纪律`: explain lawful, standardized, fair, and civilized performance; accurate reporting; accepting supervision; and refusing improper benefit.
- `典型认识误区与自测`: correct the ideas that login equals secrecy, public equals freely compilable, experience can replace procedure, and informal forwarding has no consequence.

Every record uses original concise paraphrase, the approved article structure, one non-tactical quiz, and `updated_at: 2026-07-16`.

- [ ] **Step 4: Build and verify GREEN**

Run:

```powershell
python tools/build_learning_modules.py
python -m unittest tests.test_learning_modules -v
```

Expected: seven `jilv` pages generated and all tests pass.

- [ ] **Step 5: Commit**

```powershell
git add data/learning-modules.json jilv tests/test_learning_modules.py .generated-learning-pages.json
git commit -m "feat: add discipline study module"
```

### Task 8: Independent homepage cards, five-stage route, and responsive navigation

**Files:**
- Modify: `index.html`
- Modify: `js/nav.js`
- Modify: `css/style.css`
- Modify: `tests/test_brand_styles.py`
- Modify: `tests/test_learning_modules.py`

**Interfaces:**
- Consumes: generated module paths.
- Produces: three independent cards, five-stage route, independent navigation links, and responsive layouts.

- [ ] **Step 1: Write failing homepage/navigation contract tests**

Assert homepage links separately to `rumen/index.html`, `kaohe/index.html`, and `jilv/index.html`; route labels exactly `认识岗位`, `纪律与规范`, `勤务基础`, `训练考核`, `复习自测`; and `js/nav.js` contains three separate module objects while containing neither `学习中心` nor grouped submenu markup.

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m unittest tests.test_brand_styles tests.test_learning_modules -v`  
Expected: failures for missing cards, route, links, and styles.

- [ ] **Step 3: Add the five-stage route and three independent cards**

Place a `<section class="learning-route" aria-labelledby="learning-route-title">` after the search bar and before the existing monthly hero. Each numbered stage links to the matching `rumen` page. Add three `.module-card` entries to the existing grid with article counts `5篇`, `6篇`, and `6篇`.

- [ ] **Step 4: Add three independent navigation entries and responsive layout**

Add `rumen`, `kaohe`, and `jilv` directly to `MODULES`. Desktop `.topnav` must allow a brand row plus wrapping `.nav-links`; at `max-width: 900px`, keep the current hamburger and render each link as a full-width row. Add route grid styling with five columns above 900px, three-plus-two wrapping at tablet width, and one column below 600px. Maintain minimum 44px interactive targets and visible focus.

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m unittest tests.test_brand_styles tests.test_learning_modules -v`  
Expected: all tests pass.

- [ ] **Step 6: Commit**

```powershell
git add index.html js/nav.js css/style.css tests/test_brand_styles.py tests/test_learning_modules.py
git commit -m "feat: surface independent learning modules"
```

### Task 9: Search-index integration and failure feedback

**Files:**
- Create: `tools/update_search_index.py`
- Modify: `tools/learning_modules.py`
- Modify: `search-index.json`
- Modify: `js/search.js`
- Modify: `search.html`
- Modify: `tests/test_learning_modules.py`

**Interfaces:**
- Consumes: `generated_search_records(catalog)`.
- Produces: idempotent merged `search-index.json` and visible index-load errors.

- [ ] **Step 1: Write failing search tests**

Assert there are exactly 17 generated article records, paths exactly match generated detail pages, modules are `巡防入门指南`, `考核标准`, or `纪律学习`, every record has `title`, `module`, `path`, `desc`, `tags`, and `keywords`, auth is absent, and merging twice yields identical bytes. Assert `js/search.js` recognizes all three new directories and includes the visible text `搜索索引加载失败，请稍后重试`.

- [ ] **Step 2: Run the focused tests and verify RED**

Run: `python -m unittest tests.test_learning_modules.LearningSearchTests -v`  
Expected: failure for missing tool and records.

- [ ] **Step 3: Implement idempotent search merging**

Read the existing JSON, remove only records whose path begins `rumen/`, `kaohe/`, or `jilv/`, append the 17 catalog-derived records in module order and article number order, and write UTF-8 JSON with `ensure_ascii=False`, two-space indentation, and one trailing newline. The CLI supports `--check`, which exits nonzero when the file differs without writing.

- [ ] **Step 4: Add visible browser failure feedback**

Add the three new directory names to `getDepth()`. When XHR, HTTP status, or JSON parsing fails, render a `.search-error` element with `role="status"` and text `搜索索引加载失败，请稍后重试`; the full search page uses the same message. Navigation must remain functional.

- [ ] **Step 5: Generate and verify GREEN**

Run:

```powershell
python tools/update_search_index.py
python tools/update_search_index.py --check
python -m unittest tests.test_learning_modules -v
```

Expected: 44 total search records (27 existing + 17 new), check mode exits 0, and all tests pass.

- [ ] **Step 6: Commit**

```powershell
git add tools/update_search_index.py tools/learning_modules.py search-index.json js/search.js search.html tests/test_learning_modules.py
git commit -m "feat: index learning modules in search"
```

### Task 10: Full verification and local handoff

**Files:**
- Modify only if verification finds a defect: files from Tasks 1–9

**Interfaces:**
- Produces: a locally verified, unpublised static site.

- [ ] **Step 1: Rebuild deterministically**

Run:

```powershell
python tools/build_learning_modules.py
python tools/inject_auth_guard.py
python tools/update_search_index.py --check
git diff --check
```

Expected: build succeeds, injector reports 0 changes, search check exits 0, and diff check prints nothing.

- [ ] **Step 2: Run every automated test**

Run:

```powershell
node --test tests/auth_core.test.js
python -m unittest discover -s tests -v
```

Expected: all Node and Python tests pass with zero failures and zero errors.

- [ ] **Step 3: Scan the new runtime surface for prohibited material and plaintext credentials**

Run a scoped scan across `js/auth-*.js`, `data/learning-modules.json`, `rumen`, `kaohe`, and `jilv`. Expected: no plaintext common password, `内部评分表`, tactical-step instructions, deployment patterns, non-public thresholds, real unit identifiers, or external-script tags.

- [ ] **Step 4: Perform browser acceptance checks through local HTTP**

Start `python -m http.server 8000` in the repository. In a clean browser session verify:

1. direct access to one old page and one page in each new module redirects to login;
2. wrong and empty credentials fail with the unified message;
3. the agreed common credential returns to the exact original page;
4. the Cookie has `Max-Age=86400`, `Path=/`, and `SameSite=Lax`;
5. logout removes the session and returns to login;
6. an external `redirect` query returns to `/index.html`;
7. the background, form, route, cards, navigation, source links, quiz, previous/next links, search dropdown, and full search page work at desktop and 390px widths;
8. disabling the background request leaves a readable gradient fallback;
9. keyboard focus is visible and reduced-motion mode has no continuous animation;
10. the browser console contains no new errors.

- [ ] **Step 5: Confirm no external publication occurred and inspect Git state**

Run: `git status --short`  
Expected: only the user's pre-existing untracked PPT remains; no deployment command or remote mutation has been performed.

- [ ] **Step 6: Commit any verification-only corrections**

If Step 1–5 required a correction, stage only the corrected scoped files and commit:

```powershell
git commit -m "fix: complete learning module verification"
```

If no correction was required, do not create an empty commit.
