"""Regression coverage for the approved ScienceClaw homepage ocean treatment."""

from __future__ import annotations

import hashlib
import unittest
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SWARM = ROOT / "swarm"
INDEX = SWARM / "index.html"
APPLY = SWARM / "apply.html"
SCENE = SWARM / "js" / "scene-ocean.js"
WORDMARK = SWARM / "assets" / "logos" / "scienceclaw-wordmark-white.svg"
MARK = SWARM / "assets" / "logos" / "scienceclaw-mark-official.svg"
EXPECTED_SCENE_SHA256 = (
    "9112c12f37776ab12806faf75613561ba6faee2340a50d8548c9fff5140dbde2"
)
EXPECTED_WORDMARK_SHA256 = (
    "ce132c624972784d1ab72f4114e6659f8bc400735c1bd8a8aee0cb80c68b7863"
)
EXPECTED_MARK_SHA256 = (
    "cb66ea6312ac720199f5d3c6d6a99fcde4ca338885fc1bd08cb496da5a2c4b93"
)
EXPECTED_APPLY_SHA256 = (
    "06a3fbda03c2d7b0eaa9c45caee5676ec5c0ea6f710ef9fd3d6c6acf2d90960d"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HomepageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.scripts: list[str] = []
        self.canvas_ids: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"] or "")
        if tag == "canvas" and attributes.get("id"):
            self.canvas_ids.append(attributes["id"] or "")


class HomepageOceanContractTests(unittest.TestCase):
    def test_homepage_uses_only_the_approved_ocean_scene(self) -> None:
        parser = HomepageParser()
        parser.feed(INDEX.read_text(encoding="utf-8"))
        self.assertIn("js/scene-ocean.js", parser.scripts)
        self.assertNotIn("js/scene.js", parser.scripts)
        self.assertNotIn("js/tentacles.js", parser.scripts)
        self.assertEqual(parser.canvas_ids, ["scene"])
        self.assertFalse((SWARM / "js" / "scene.js").exists())
        self.assertFalse((SWARM / "js" / "tentacles.js").exists())
        self.assertEqual(sha256(SCENE), EXPECTED_SCENE_SHA256)


class HomepageOfficialLogoTests(unittest.TestCase):
    def test_official_assets_have_approved_provenance(self) -> None:
        self.assertTrue(WORDMARK.is_file())
        self.assertTrue(MARK.is_file())
        self.assertEqual(sha256(WORDMARK), EXPECTED_WORDMARK_SHA256)
        self.assertEqual(sha256(MARK), EXPECTED_MARK_SHA256)

    def test_official_identity_is_homepage_only(self) -> None:
        homepage = INDEX.read_text(encoding="utf-8")
        application = APPLY.read_text(encoding="utf-8")
        self.assertIn("assets/logos/scienceclaw-wordmark-white.svg", homepage)
        self.assertIn("assets/logos/scienceclaw-mark-official.svg", homepage)
        self.assertNotIn("scienceclaw-wordmark-white.svg", application)
        self.assertNotIn("scienceclaw-mark-official.svg", application)
        self.assertEqual(sha256(APPLY), EXPECTED_APPLY_SHA256)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


class HomepageOceanRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        handler = partial(QuietHandler, directory=str(SWARM))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}/"
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_reduced_motion_renders_one_static_ocean_frame(self) -> None:
        context = self.browser.new_context(reduced_motion="reduce")
        page = context.new_page()
        page_errors: list[str] = []
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.add_init_script(
            """
            window.__rafCalls = 0;
            const original = window.requestAnimationFrame.bind(window);
            window.requestAnimationFrame = (callback) => {
              window.__rafCalls += 1;
              return original(callback);
            };
            """
        )
        try:
            page.goto(self.base_url, wait_until="networkidle")
            page.wait_for_timeout(500)
            self.assertEqual(page.evaluate("window.__rafCalls"), 0)
            self.assertGreater(
                page.locator("#scene").evaluate("canvas => canvas.width"), 0
            )
            self.assertEqual(page_errors, [])
        finally:
            context.close()

    def test_hero_title_stays_visible_after_compact_resize(self) -> None:
        page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            page.goto(self.base_url, wait_until="networkidle")
            for width in (375, 280):
                with self.subTest(width=width):
                    page.set_viewport_size({"width": width, "height": 300})
                    geometry = page.evaluate(
                        """() => {
                          const nav = document.querySelector('.nav').getBoundingClientRect();
                          const wordmark = document.querySelector(
                            '.identity__scienceclaw-logo'
                          ).getBoundingClientRect();
                          const action = document.querySelector(
                            '.nav__mobile-action'
                          ).getBoundingClientRect();
                          const title = document.querySelector('.hero__title').getBoundingClientRect();
                          return {
                            navBottom: nav.bottom,
                            wordmarkWidth: wordmark.width,
                            wordmarkRight: wordmark.right,
                            actionLeft: action.left,
                            titleTop: title.top,
                            titleBottom: title.bottom,
                            viewportHeight: window.innerHeight
                          };
                        }"""
                    )
                    visible_top = max(
                        geometry["navBottom"], geometry["titleTop"], 0
                    )
                    visible_bottom = min(
                        geometry["titleBottom"], geometry["viewportHeight"]
                    )
                    visible_height = max(0, visible_bottom - visible_top)
                    self.assertGreaterEqual(geometry["wordmarkWidth"], 140)
                    self.assertLessEqual(
                        geometry["wordmarkRight"] + 8, geometry["actionLeft"]
                    )
                    self.assertGreaterEqual(visible_height, 48)
        finally:
            page.close()

    def test_webgl_failure_activates_static_fallback(self) -> None:
        context = self.browser.new_context()
        page = context.new_page()
        page.add_init_script(
            """
            const original = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type, ...args) {
              if (["webgl", "webgl2", "experimental-webgl"].includes(type)) {
                return null;
              }
              return original.call(this, type, ...args);
            };
            """
        )
        try:
            page.goto(self.base_url, wait_until="domcontentloaded")
            page.wait_for_function("document.body.classList.contains(\"no-webgl\")")
            self.assertTrue(
                page.evaluate("document.body.classList.contains(\"no-webgl\")")
            )
        finally:
            context.close()


if __name__ == "__main__":
    unittest.main()
