"""全站学习页面配图视觉验收。

默认从配图评估台账中为每个模块选择三页：视觉基线代表页、图片最多页、
以及 SVG 图内文字最长页。脚本会在 1440×900 和 390×900 两个视口截图，
并把机器可判定的布局结果写入忽略版本控制的 ``.artifacts`` 目录。

退出码：0=浏览器验收通过；1=发现视觉/结构缺陷；2=浏览器运行环境不可用。
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import sys
import threading
import time
from typing import Iterable
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "data" / "image-optimization-plan.json"
OUTPUT_DIR = ROOT / ".artifacts" / "visual-acceptance-sitewide"
MODULES = ("zhuangbei", "xunlian", "jingqing", "qinwu", "fagui", "zoufang")
VIEWPORTS = ((1440, 900, "desktop"), (390, 900, "mobile"))
THEMES = ("warm-police-blue", "classic-warm-brown", "daylight", "night")

BASELINE_PAGES = {
    "zhuangbei": "zhuangbei/zhifa-jiuyi.html",
    "xunlian": "xunlian/geren-fanghu-anquan.html",
    "jingqing": "jingqing/zuijiu-lei.html",
    "qinwu": "qinwu/gonggong-zhixu-goutong-jilu.html",
    "fagui": "fagui/panwen-shenfenzheng.html",
    "zoufang": "zoufang/changsuo-aed-jiancha.html",
}


@dataclass(frozen=True)
class PageMetrics:
    path: str
    module: str
    figure_count: int
    image_count: int
    svg_text_length: int


@dataclass(frozen=True)
class Sample:
    path: str
    module: str
    reason: str
    figure_count: int
    image_count: int
    svg_text_length: int


class AuthAwareHandler(SimpleHTTPRequestHandler):
    """仅供本地验收：用仓库已有摘要写入会话 Cookie。"""

    auth_cookie = ""

    def end_headers(self) -> None:
        if self.auth_cookie:
            self.send_header("Set-Cookie", self.auth_cookie)
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, _format: str, *_args: object) -> None:
        return


def _configure_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")


def _class_contains(tag: str, class_name: str) -> bool:
    match = re.search(r"\bclass\s*=\s*(['\"])(.*?)\1", tag, flags=re.I | re.S)
    return bool(match and class_name in match.group(2).split())


def _image_sources(html: str) -> list[str]:
    return [
        match.group(2)
        for match in re.finditer(
            r"<img\b[^>]*?\bsrc\s*=\s*(['\"])(.*?)\1", html, flags=re.I | re.S
        )
    ]


def _svg_text_length(page_path: Path, sources: Iterable[str]) -> int:
    total = 0
    for source in sources:
        parsed = urlparse(source)
        if parsed.scheme or parsed.netloc or not parsed.path.lower().endswith(".svg"):
            continue
        asset_path = (page_path.parent / parsed.path).resolve()
        try:
            asset_path.relative_to(ROOT.resolve())
            root = ET.parse(asset_path).getroot()
        except (OSError, ValueError, ET.ParseError):
            continue
        for node in root.iter():
            if node.tag.rsplit("}", 1)[-1] in {"text", "tspan"}:
                total += len("".join(node.itertext()).strip())
    return total


def page_metrics(path: str, module: str) -> PageMetrics:
    page_path = ROOT / path
    html = page_path.read_text(encoding="utf-8")
    figure_count = sum(
        1
        for match in re.finditer(r"<figure\b[^>]*>", html, flags=re.I | re.S)
        if _class_contains(match.group(0), "learning-figure")
    )
    sources = _image_sources(html)
    return PageMetrics(
        path=path,
        module=module,
        figure_count=figure_count,
        image_count=len(sources),
        svg_text_length=_svg_text_length(page_path, sources),
    )


def select_samples() -> list[Sample]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    by_module: dict[str, list[PageMetrics]] = {module: [] for module in MODULES}
    for record in plan["pages"]:
        module = record["module"]
        if module in by_module:
            by_module[module].append(page_metrics(record["path"], module))

    samples: list[Sample] = []
    for module in MODULES:
        candidates = [metric for metric in by_module[module] if metric.figure_count > 0]
        baseline_path = BASELINE_PAGES[module]
        baseline = next((item for item in candidates if item.path == baseline_path), None)
        if baseline is None:
            raise RuntimeError(f"代表页缺少 .learning-figure：{baseline_path}")

        chosen: list[tuple[PageMetrics, str]] = [(baseline, "六模块视觉基线代表页")]
        remaining = [item for item in candidates if item.path != baseline_path]
        most_images = max(
            remaining,
            key=lambda item: (
                item.figure_count,
                item.image_count,
                item.svg_text_length,
                item.path,
            ),
            default=None,
        )
        if most_images:
            chosen.append((most_images, "模块内学习图/图片数量最高样本"))

        used = {item.path for item, _reason in chosen}
        longest_text = max(
            (item for item in remaining if item.path not in used),
            key=lambda item: (item.svg_text_length, item.figure_count, item.path),
            default=None,
        )
        if longest_text:
            chosen.append((longest_text, "排除最高图量页后的补充长图文样本"))

        if len(chosen) < 3:
            raise RuntimeError(f"{module} 可验收的独立学习配图页不足 3 页")

        samples.extend(
            Sample(reason=reason, **asdict(metric)) for metric, reason in chosen
        )
    return samples


def source_audit(samples: Iterable[Sample]) -> list[str]:
    errors: list[str] = []
    for sample in samples:
        page_path = ROOT / sample.path
        html = page_path.read_text(encoding="utf-8")
        figures = [
            match.group(0)
            for match in re.finditer(
                r"<figure\b[^>]*>.*?</figure>", html, flags=re.I | re.S
            )
            if _class_contains(match.group(0).split(">", 1)[0] + ">", "learning-figure")
        ]
        if not figures:
            errors.append(f"{sample.path}: 缺少 .learning-figure")
            continue
        for index, figure in enumerate(figures, start=1):
            if not re.search(r"<figcaption\b[^>]*>\s*\S", figure, flags=re.I | re.S):
                errors.append(f"{sample.path}: 第 {index} 张学习图缺少非空图注")
            image_match = re.search(r"<img\b[^>]*>", figure, flags=re.I | re.S)
            if not image_match:
                errors.append(f"{sample.path}: 第 {index} 张学习图缺少图片")
                continue
            image_tag = image_match.group(0)
            src_match = re.search(r"\bsrc\s*=\s*(['\"])(.*?)\1", image_tag, flags=re.I | re.S)
            alt_match = re.search(r"\balt\s*=\s*(['\"])(.*?)\1", image_tag, flags=re.I | re.S)
            if not src_match:
                errors.append(f"{sample.path}: 第 {index} 张学习图缺少 src")
            else:
                asset = (page_path.parent / urlparse(src_match.group(2)).path).resolve()
                if not asset.exists():
                    errors.append(f"{sample.path}: 图片不存在：{src_match.group(2)}")
            if not alt_match or not alt_match.group(2).strip():
                errors.append(f"{sample.path}: 第 {index} 张学习图缺少非空 alt")
    return errors


def _load_auth_cookie() -> str:
    config = (ROOT / "js" / "auth-config.js").read_text(encoding="utf-8")
    name = re.search(r"cookieName:\s*['\"]([^'\"]+)", config)
    digest = re.search(r"digest:\s*['\"]([0-9a-f]{64})", config)
    if not name or not digest:
        raise RuntimeError("无法从 js/auth-config.js 读取本地验收会话配置")
    return f"{name.group(1)}={digest.group(1)}; Path=/; SameSite=Lax"


def start_server(port: int = 0) -> tuple[ThreadingHTTPServer, str]:
    handler = partial(AuthAwareHandler, directory=str(ROOT))
    AuthAwareHandler.auth_cookie = _load_auth_cookie()
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, f"http://{host}:{port}"


def _theme_script(theme: str) -> str:
    if theme == "warm-police-blue":
        return "document.documentElement.removeAttribute('data-theme')"
    return f"document.documentElement.setAttribute('data-theme', {json.dumps(theme)})"


def _runtime_checks(page, sample: Sample, viewport: tuple[int, int, str]) -> dict:
    width, height, label = viewport
    page.locator("details").evaluate_all("nodes => nodes.forEach(node => node.open = true)")
    page.wait_for_timeout(100)
    figures = page.locator(".learning-figure")
    figure_count = figures.count()
    if figure_count < 1:
        raise AssertionError("页面没有 .learning-figure")

    first_figure = figures.first
    first_figure.scroll_into_view_if_needed()
    page.wait_for_timeout(150)
    page.evaluate("window.scrollTo(0, Math.max(0, window.scrollY - 48))")

    layout = page.evaluate(
        r"""() => {
          const viewport = {width: window.innerWidth, height: window.innerHeight};
          const doc = document.documentElement;
          const figures = [...document.querySelectorAll('.learning-figure')];
          const box = element => {
            const rect = element.getBoundingClientRect();
            return {
              left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom,
              width: rect.width, height: rect.height,
              clientWidth: element.clientWidth, scrollWidth: element.scrollWidth,
              clientHeight: element.clientHeight, scrollHeight: element.scrollHeight
            };
          };
          return {
            finalPath: location.pathname.replace(/^\//, ''),
            authPending: doc.classList.contains('auth-pending'),
            pageScrollWidth: doc.scrollWidth,
            pageClientWidth: doc.clientWidth,
            viewport,
            titleVisible: !!document.querySelector('h1'),
            articleTextLength: (document.querySelector('.article-content')?.innerText || '').trim().length,
            figures: figures.map(figure => ({
              figure: box(figure),
              media: figure.querySelector('.learning-figure__media') ? box(figure.querySelector('.learning-figure__media')) : null,
              image: figure.querySelector('img') ? box(figure.querySelector('img')) : null,
              caption: figure.querySelector('figcaption') ? box(figure.querySelector('figcaption')) : null,
              imageLoaded: !!figure.querySelector('img') && figure.querySelector('img').complete && figure.querySelector('img').naturalWidth > 0
            }))
          };
        }"""
    )

    errors: list[str] = []
    if layout["finalPath"] != sample.path:
        errors.append(f"认证后路径不符：{layout['finalPath']}")
    if layout["authPending"]:
        errors.append("页面仍处于 auth-pending")
    if not layout["titleVisible"]:
        errors.append("H1 不可用")
    if layout["articleTextLength"] < 100:
        errors.append("正文长度异常，可能未进入真实学习页")
    if layout["pageScrollWidth"] > layout["viewport"]["width"] + 5:
        errors.append(
            f"页面横向溢出：scrollWidth={layout['pageScrollWidth']}，innerWidth={layout['viewport']['width']}"
        )

    for index, item in enumerate(layout["figures"], start=1):
        for name in ("figure", "media", "image", "caption"):
            box = item[name]
            if not box or box["width"] <= 0 or box["height"] <= 0:
                errors.append(f"第 {index} 张图的 {name} 为零尺寸或不可见")
                continue
            if box["left"] < -1 or box["right"] > layout["viewport"]["width"] + 1:
                errors.append(
                    f"第 {index} 张图的 {name} 超出视口：left={box['left']:.1f}, right={box['right']:.1f}"
                )
            if box["scrollWidth"] > box["clientWidth"] + 1:
                errors.append(f"第 {index} 张图的 {name} 内容横向裁剪")
        if not item["imageLoaded"]:
            errors.append(f"第 {index} 张图片未加载")

    theme_results = {}
    for theme in THEMES:
        page.evaluate(_theme_script(theme))
        theme_results[theme] = page.evaluate(
            """() => {
              const caption = document.querySelector('.learning-figure figcaption');
              const figure = document.querySelector('.learning-figure');
              const style = caption ? getComputedStyle(caption) : null;
              return {
                captionColor: style?.color || '',
                captionBackground: style?.backgroundColor || '',
                figureBackground: figure ? getComputedStyle(figure).backgroundColor : ''
              };
            }"""
        )
    page.evaluate(_theme_script("warm-police-blue"))

    first_box = layout["figures"][0]["figure"]
    first_screen_visible = first_box["bottom"] > 0 and first_box["top"] < height
    if not first_screen_visible:
        errors.append("滚入配图后首张学习图仍未进入截图视口")

    return {
        "page": sample.path,
        "module": sample.module,
        "sampleReason": sample.reason,
        "viewport": {"width": width, "height": height, "label": label},
        "layout": layout,
        "themeStyles": theme_results,
        "firstScreenFigureVisible": first_screen_visible,
        "errors": errors,
    }


def run_browser_acceptance(samples: list[Sample]) -> tuple[list[dict], list[str]]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError(
            "Python Playwright 未安装；无法在当前解释器执行真实浏览器截图"
        ) from error

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    server, base_url = start_server()
    results: list[dict] = []
    errors: list[str] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for sample in samples:
                    for viewport in VIEWPORTS:
                        width, height, label = viewport
                        context = browser.new_context(
                            viewport={"width": width, "height": height},
                            device_scale_factor=1,
                        )
                        page = context.new_page()
                        try:
                            page.goto(
                                f"{base_url}/{sample.path}",
                                wait_until="domcontentloaded",
                                timeout=20_000,
                            )
                            page.wait_for_timeout(250)
                            result = _runtime_checks(page, sample, viewport)
                            screenshot_name = (
                                f"{sample.module}-{Path(sample.path).stem}-{width}x{height}.png"
                            )
                            screenshot_path = OUTPUT_DIR / screenshot_name
                            page.screenshot(path=str(screenshot_path), full_page=False)
                            result["screenshot"] = screenshot_name
                            results.append(result)
                            for message in result["errors"]:
                                errors.append(f"{sample.path} [{width}x{height}]: {message}")
                        except Exception as error:  # Playwright errors are evidence, not skips.
                            errors.append(f"{sample.path} [{width}x{height}]: {error}")
                        finally:
                            context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return results, errors


def write_report(
    samples: list[Sample],
    results: list[dict],
    errors: list[str],
    *,
    status: str,
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": status,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "viewports": [
            {"width": width, "height": height, "label": label}
            for width, height, label in VIEWPORTS
        ],
        "samples": [asdict(sample) for sample in samples],
        "results": results,
        "errors": errors,
    }
    (OUTPUT_DIR / "report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list-samples",
        action="store_true",
        help="仅列出并检查本轮 18 个抽样页，不启动浏览器",
    )
    parser.add_argument(
        "--serve",
        type=int,
        metavar="PORT",
        help="在指定端口启动本地 auth-aware 验收服务器，供受控浏览器复核",
    )
    return parser.parse_args()


def main() -> int:
    _configure_console()
    args = parse_args()
    if args.serve is not None:
        server, base_url = start_server(args.serve)
        print(f"本地验收服务器：{base_url}", flush=True)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            server.shutdown()
            server.server_close()
        return 0

    try:
        samples = select_samples()
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"FAIL：无法建立抽样清单：{error}")
        return 1

    print(f"抽样页：{len(samples)}（每模块 3 页，含 6 个基线代表页）")
    for sample in samples:
        print(
            f"- {sample.module}: {sample.path}｜{sample.reason}｜"
            f"learning figures={sample.figure_count}, images={sample.image_count}, "
            f"SVG text={sample.svg_text_length}"
        )

    source_errors = source_audit(samples)
    if source_errors:
        print("FAIL：源文件结构检查发现问题")
        for error in source_errors:
            print(f"- {error}")
        return 1
    print("PASS：18 个抽样页的学习图、图片路径、alt 与图注结构有效")

    if args.list_samples:
        return 0

    try:
        results, browser_errors = run_browser_acceptance(samples)
    except RuntimeError as error:
        write_report(samples, [], [str(error)], status="blocked")
        print(f"BLOCKED：{error}")
        print(f"报告：{OUTPUT_DIR / 'report.json'}")
        return 2

    write_report(
        samples,
        results,
        browser_errors,
        status="failed" if browser_errors else "passed",
    )
    if browser_errors:
        print(f"FAIL：浏览器视觉验收发现 {len(browser_errors)} 个问题")
        for error in browser_errors:
            print(f"- {error}")
        return 1

    expected = len(samples) * len(VIEWPORTS)
    if len(results) != expected:
        print(f"FAIL：预期 {expected} 份浏览器结果，实际 {len(results)}")
        return 1
    print(f"PASS：{len(results)} 个视口截图及布局检查通过")
    print(f"截图与报告：{OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
