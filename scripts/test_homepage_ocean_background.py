"""Regression coverage for the approved ScienceClaw homepage ocean treatment."""

from __future__ import annotations

import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SWARM = ROOT / "swarm"
INDEX = SWARM / "index.html"
SCENE = SWARM / "js" / "scene-ocean.js"
EXPECTED_SCENE_SHA256 = (
    "9112c12f37776ab12806faf75613561ba6faee2340a50d8548c9fff5140dbde2"
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


if __name__ == "__main__":
    unittest.main()
