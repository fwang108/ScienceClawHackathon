# Ocean Background and Official Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace only the ScienceClaw homepage animation with the approved lobster ocean network and use the supplied transparent SVG identity in the homepage header and hero.

**Architecture:** `swarm/index.html` remains the homepage and keeps its current content/layout, but loads a pinned upstream `scene-ocean.js` instead of the legacy crane and tentacle systems. New homepage-only logo classes consume byte-identical supplied SVGs without affecting `swarm/apply.html`; focused provenance/runtime tests protect the scene, official assets, fallbacks, and responsive geometry.

**Tech Stack:** Static HTML/CSS/SVG, JavaScript ES modules, Three.js 0.160.0, Python `unittest`, Playwright Chromium, Vercel

**Spec:** `docs/superpowers/specs/2026-09-22-ocean-background-official-logo-design.md`

## Global Constraints

- Preserve all homepage copy, title, typography, spacing, navigation, calls to action, content sections, and responsive behavior.
- Change only the homepage background and homepage ScienceClaw logo treatments.
- Keep `swarm/apply.html`, flyer artifacts, sponsor materials, `v1/`, and `v2/` byte-for-byte unchanged.
- Use upstream commit `be3ccab40ec2fd3a16f9c21548d6ca39edcb4c81` for `v3/js/scene-ocean.js`.
- Require scene SHA-256 `9112c12f37776ab12806faf75613561ba6faee2340a50d8548c9fff5140dbde2`.
- Require wordmark SHA-256 `ce132c624972784d1ab72f4114e6659f8bc400735c1bd8a8aee0cb80c68b7863`.
- Require mark SHA-256 `cb66ea6312ac720199f5d3c6d6a99fcde4ca338885fc1bd08cb496da5a2c4b93`.
- Preserve the existing Three.js import map; add no build system or runtime dependency.
- Preserve user-owned `sponsor_pitches/examples/` and ignored `.superpowers/` preview files.

---

### Task 1: Replace the active homepage scene

**Files:**
- Create: `scripts/test_homepage_ocean_background.py`
- Create: `swarm/js/scene-ocean.js`
- Modify: `scripts/verify_pr1_swarm_refresh.py`
- Modify: `swarm/index.html`
- Modify: `swarm/css/styles.css`
- Delete: `swarm/js/scene.js`
- Delete: `swarm/js/tentacles.js`

**Interfaces:**
- Consumes: the existing `<canvas id="scene">`, Three.js import map, `body.no-webgl`, `prefers-reduced-motion`, pointer events, and document scroll.
- Produces: one active homepage module at `js/scene-ocean.js` with fixed-canvas rendering and no tentacle canvas/script.

- [ ] **Step 1: Add failing scene provenance and markup tests**

Create `scripts/test_homepage_ocean_background.py` with the focused contract below:

```python
from __future__ import annotations

import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SWARM = ROOT / "swarm"
INDEX = SWARM / "index.html"
SCENE = SWARM / "js" / "scene-ocean.js"
EXPECTED_SCENE_SHA256 = "9112c12f37776ab12806faf75613561ba6faee2340a50d8548c9fff5140dbde2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HomepageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.scripts: list[str] = []
        self.canvas_ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
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
```

- [ ] **Step 2: Run the focused test and verify the red phase**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_homepage_ocean_background.py \
  HomepageOceanContractTests.test_homepage_uses_only_the_approved_ocean_scene
```

Expected: FAIL because the homepage still loads `js/scene.js` and `js/tentacles.js`, includes the tentacle canvas, and has no `scene-ocean.js`.

- [ ] **Step 3: Retrieve and verify the pinned upstream scene**

Run:

```bash
scene_tmp=$(mktemp -d)
curl -fsS \
  https://raw.githubusercontent.com/MaxwellBauer/Hackathon_Demo_Page/be3ccab40ec2fd3a16f9c21548d6ca39edcb4c81/v3/js/scene-ocean.js \
  -o "$scene_tmp/scene-ocean.js"
test "$(sha256sum "$scene_tmp/scene-ocean.js" | awk '{print $1}')" = \
  9112c12f37776ab12806faf75613561ba6faee2340a50d8548c9fff5140dbde2
mv "$scene_tmp/scene-ocean.js" swarm/js/scene-ocean.js
rmdir "$scene_tmp"
```

Expected: the hash comparison succeeds and the exact 837-line source becomes `swarm/js/scene-ocean.js`.

- [ ] **Step 4: Switch homepage markup and remove the legacy systems**

In `swarm/index.html`, remove:

```html
<canvas id="tentacles" class="tentacle-layer" aria-hidden="true"></canvas>
```

Replace:

```html
<script type="module" src="js/scene.js"></script>
<script src="js/tentacles.js" defer></script>
```

with:

```html
<script type="module" src="js/scene-ocean.js"></script>
```

Delete the inactive files with:

```bash
git rm swarm/js/scene.js swarm/js/tentacles.js
```

Remove the `.tentacle-layer` block from `swarm/css/styles.css`; retain `#scene`, `.grain`, `.scene-veil`, and `body.no-webgl` unchanged.

- [ ] **Step 5: Point the upstream verifier at the active scene**

In `scripts/verify_pr1_swarm_refresh.py`, change the model path and expected hash to:

```python
MODEL = ROOT / "swarm" / "js" / "scene-ocean.js"
EXPECTED_MODEL_SHA256 = (
    "9112c12f37776ab12806faf75613561ba6faee2340a50d8548c9fff5140dbde2"
)
```

Update its module docstring and model failure messages from “Swarm model” to “approved ocean scene”; keep the LAMM and application-header checks unchanged.

- [ ] **Step 6: Verify scene green phase and syntax**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_homepage_ocean_background.py
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/verify_pr1_swarm_refresh.py --model-only
node --check swarm/js/scene-ocean.js
```

Expected: the focused test and verifier pass, and Node reports no syntax error.

- [ ] **Step 7: Commit the scene replacement**

```bash
git add scripts/test_homepage_ocean_background.py \
  scripts/verify_pr1_swarm_refresh.py swarm/index.html swarm/css/styles.css \
  swarm/js/scene-ocean.js
git commit -m "feat: replace homepage scene with lobster ocean"
```

---

### Task 2: Install and render the official transparent SVG identity

**Files:**
- Create: `swarm/assets/logos/scienceclaw-wordmark-white.svg`
- Create: `swarm/assets/logos/scienceclaw-mark-official.svg`
- Modify: `scripts/test_homepage_ocean_background.py`
- Modify: `scripts/test_scienceclaw_rebrand.py`
- Modify: `swarm/index.html`
- Modify: `swarm/css/styles.css`

**Interfaces:**
- Consumes: supplied `SVG/white on clear.svg`, supplied `SVG/no_text.svg`, `.identity--scienceclaw`, `.hero__title`, and the existing 280–1500px header regression widths.
- Produces: `.identity__scienceclaw-logo` for the accessible header wordmark and `.hero__official-mark` for the decorative hero symbol.

- [ ] **Step 1: Add failing official-asset and homepage-isolation tests**

Extend `scripts/test_homepage_ocean_background.py` with:

```python
APPLY = SWARM / "apply.html"
WORDMARK = SWARM / "assets" / "logos" / "scienceclaw-wordmark-white.svg"
MARK = SWARM / "assets" / "logos" / "scienceclaw-mark-official.svg"
EXPECTED_WORDMARK_SHA256 = "ce132c624972784d1ab72f4114e6659f8bc400735c1bd8a8aee0cb80c68b7863"
EXPECTED_MARK_SHA256 = "cb66ea6312ac720199f5d3c6d6a99fcde4ca338885fc1bd08cb496da5a2c4b93"
EXPECTED_APPLY_SHA256 = "06a3fbda03c2d7b0eaa9c45caee5676ec5c0ea6f710ef9fd3d6c6acf2d90960d"


class HomepageOfficialLogoTests(unittest.TestCase):
    def test_official_assets_have_approved_provenance(self) -> None:
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
```

Update `test_public_wordmarks_use_full_scienceclaw_name` in `scripts/test_scienceclaw_rebrand.py` so the homepage assertion reads the `.identity__scienceclaw-logo` image `alt`, while application and flyer assertions continue reading visible text. Update the shared-header geometry helper to measure every visible child of `.identity--scienceclaw` instead of assuming both `.identity__scienceclaw-mark` and `.identity__scienceclaw-word` exist on every page.

- [ ] **Step 2: Run focused tests and verify the red phase**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_homepage_ocean_background.py HomepageOfficialLogoTests
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_scienceclaw_rebrand.py \
  ScienceClawRenderedIdentityTests.test_public_wordmarks_use_full_scienceclaw_name
```

Expected: FAIL because the official public assets and new homepage selectors do not exist.

- [ ] **Step 3: Copy the supplied SVGs byte-for-byte**

Run:

```bash
cp '/home/fiona/LAMM/hackathon_fall26/scienceclaw_logos_09_21_26/SVG/white on clear.svg' \
  swarm/assets/logos/scienceclaw-wordmark-white.svg
cp '/home/fiona/LAMM/hackathon_fall26/scienceclaw_logos_09_21_26/SVG/no_text.svg' \
  swarm/assets/logos/scienceclaw-mark-official.svg
sha256sum swarm/assets/logos/scienceclaw-wordmark-white.svg \
  swarm/assets/logos/scienceclaw-mark-official.svg
```

Expected: hashes exactly match the Global Constraints.

- [ ] **Step 4: Replace only the homepage logo markup**

Replace the two homepage header children with:

```html
<img class="identity__scienceclaw-logo"
  src="assets/logos/scienceclaw-wordmark-white.svg" alt="ScienceClaw" />
```

Replace the homepage hero image with:

```html
<img class="hero__official-mark" src="assets/logos/scienceclaw-mark-official.svg"
  alt="" aria-hidden="true" />
```

Do not edit `swarm/apply.html`.

- [ ] **Step 5: Add homepage-only responsive logo presentation**

Add these rules to `swarm/css/styles.css` while retaining the application page’s existing `.identity__scienceclaw-mark` and `.identity__scienceclaw-word` rules:

```css
.identity__scienceclaw-logo {
  display: block;
  width: 176px;
  max-width: 100%;
  height: auto;
  max-height: 44px;
}

.hero__official-mark {
  display: block;
  width: clamp(82px, 8vw, 120px);
  height: auto;
  margin-bottom: 0.55rem;
  animation: scienceclaw-float 3.2s ease-in-out infinite;
  filter: invert(1) drop-shadow(0 0 16px rgba(217, 160, 56, 0.28));
}
```

Inside `@media (max-width: 1240px)`, set `.identity__scienceclaw-logo { width: 152px; }`. Inside `@media (max-width: 820px)`, replace the old `.hero__claw` rule with `.hero__official-mark { width: 76px; margin-bottom: 0.35rem; }`. In the reduced-motion query, replace `.hero__claw` with `.hero__official-mark`; the official header wordmark remains static.

- [ ] **Step 6: Pass focused logo and responsive geometry tests**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_homepage_ocean_background.py
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_scienceclaw_rebrand.py \
  ScienceClawRenderedIdentityTests.test_public_wordmarks_use_full_scienceclaw_name \
  ScienceClawRenderedIdentityTests.test_shared_header_identities_keep_visible_wordmark_clear_of_action
```

Expected: all focused tests pass on homepage and application page across every existing viewport.

- [ ] **Step 7: Commit the official homepage identity**

```bash
git add scripts/test_homepage_ocean_background.py \
  scripts/test_scienceclaw_rebrand.py swarm/index.html swarm/css/styles.css \
  swarm/assets/logos/scienceclaw-wordmark-white.svg \
  swarm/assets/logos/scienceclaw-mark-official.svg
git commit -m "feat: use official SVG identity on homepage"
```

---

### Task 3: Runtime resilience, visual approval, and production cutover

**Files:**
- Modify: `scripts/test_homepage_ocean_background.py`
- Generate ignored preview: `.superpowers/scienceclaw-ocean-final.png`
- Temporary ignored linkage: `swarm/.vercel/project.json`

**Interfaces:**
- Consumes: the completed homepage, the existing Vercel project `prj_YnKzgJhfHfCbgWpYBcMRrUXWYKcg`, and apex alias `scienceclawhack.ai`.
- Produces: runtime evidence for reduced motion/WebGL fallback and a verified production deployment; no new public API.

- [ ] **Step 1: Add real-browser reduced-motion and WebGL fallback tests**

Extend `scripts/test_homepage_ocean_background.py` with a `ThreadingHTTPServer` serving `swarm/` on port `0` and Playwright tests that:

```python
context = self.browser.new_context(reduced_motion="reduce")
page = context.new_page()
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
page.goto(self.base_url, wait_until="networkidle")
page.wait_for_timeout(500)
self.assertEqual(page.evaluate("window.__rafCalls"), 0)
self.assertGreater(page.locator("#scene").evaluate("canvas => canvas.width"), 0)
```

For the fallback test, add an initialization script that returns `None` for `webgl`, `webgl2`, and `experimental-webgl` canvas contexts, navigate to the same URL, and assert `document.body.classList.contains('no-webgl')` becomes true. Close every page/context and stop the local HTTP server in `tearDownClass`.

- [ ] **Step 2: Run the runtime tests and verify the green phase**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python \
  scripts/test_homepage_ocean_background.py
```

Expected: all provenance, isolation, reduced-motion, renderer, and fallback tests pass without uncaught page errors in the normal WebGL case.

- [ ] **Step 3: Run the full regression suite and unchanged-artifact checks**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python -m unittest \
  discover -s scripts -p 'test_*.py'
for verifier in scripts/verify_*.py; do
  if [ "$verifier" = scripts/verify_pr1_swarm_refresh.py ]; then
    PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python "$verifier" \
      --logo-source /home/fiona/LAMM/hackathon_fall26/logos/LOGO_LAMM_full_black.svg
  else
    PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python "$verifier"
  fi
done
node --check swarm/js/main.js
node --check swarm/js/scene-ocean.js
test "$(sha256sum swarm/apply.html | awk '{print $1}')" = \
  06a3fbda03c2d7b0eaa9c45caee5676ec5c0ea6f710ef9fd3d6c6acf2d90960d
test "$(sha256sum swarm/flyer.html | awk '{print $1}')" = \
  867ccec225446819ba0b365ac9c6399c161880691d07fd1fd90d18bde2151220
test "$(sha256sum sponsor_pitches/deck.html | awk '{print $1}')" = \
  af9dd3a0fb5a08b8ed19949e0791d43fbd4ce8c93151433c818bd9b6dd4f87aa
test "$(sha256sum sponsor_pitches/one-pager.html | awk '{print $1}')" = \
  444762f2e92823c619438f72fcf5b9d564ccea455063bfdce4828df4e8c0a6e8
git diff --check -- . ':(exclude)**/*.pdf'
```

Expected: every test and verifier exits zero, JavaScript syntax is valid, and every unchanged-file hash matches.

- [ ] **Step 4: Generate and inspect the final local screenshot**

Serve `swarm/` locally, open the homepage at 1440 × 900 in Playwright, wait for fonts/images and the first rendered ocean frame, then save `.superpowers/scienceclaw-ocean-final.png`. Compare it with `.superpowers/scienceclaw-ocean-logo-preview.png` using the image viewer and require the same approved hierarchy: official white header wordmark, official white hero mark, unchanged title/copy/spacing, and readable content over the lobster ocean scene.

- [ ] **Step 5: Commit runtime coverage after fresh verification**

```bash
git add scripts/test_homepage_ocean_background.py
git commit -m "test: verify ocean scene runtime fallbacks"
```

- [ ] **Step 6: Deploy only the existing Vercel project**

Create ignored `swarm/.vercel/project.json` with exactly:

```json
{"projectId":"prj_YnKzgJhfHfCbgWpYBcMRrUXWYKcg","orgId":"team_qLFUoQHuDL5pBWs1imuYbgh1","projectName":"infinite-hackathon"}
```

From `swarm/`, capture and inspect the exact production URL before aliasing:

```bash
deployment_url=$(vercel deploy --prod --yes)
test -n "$deployment_url"
vercel inspect "$deployment_url" --scope lamm
vercel alias set "$deployment_url" scienceclawhack.ai --scope lamm
```

Remove only the temporary `swarm/.vercel/project.json` after the deployment reports `READY`. Do not create a project and do not modify `www` or `swarmhack.ai` aliases.

- [ ] **Step 7: Verify the live apex and unchanged application**

Require HTTP 200 for `/`, `/apply.html`, `/js/scene-ocean.js`, `/assets/logos/scienceclaw-wordmark-white.svg`, and `/assets/logos/scienceclaw-mark-official.svg`. Download the three new assets and compare them byte-for-byte with the repository copies. Compare the live application HTML byte-for-byte with `swarm/apply.html`. Run Playwright at the regression viewport widths against `https://scienceclawhack.ai/`, require no header/hero overlaps, and confirm the scene canvas has nonzero dimensions and no uncaught page errors.
