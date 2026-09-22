"""Regression coverage for the approved ScienceClaw homepage ocean treatment."""

from __future__ import annotations

import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
