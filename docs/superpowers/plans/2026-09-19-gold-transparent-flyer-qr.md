# Gold Transparent Flyer QR Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and publish a transparent, theme-gold flyer QR code that encodes the canonical ScienceClaw application URL.

**Architecture:** Keep `scripts/build_social_flyer.py` as the only QR and flyer asset generator. Extend `scripts/verify_flyer_application.py` to validate SVG presentation semantics and decode the actual light-on-dark color composition with polarity normalization, then regenerate and republish all flyer outputs through the existing build.

**Tech Stack:** Python 3, OpenCV, NumPy, XML/SVG, Playwright, static HTML, PNG, PDF

**Spec:** `docs/superpowers/specs/2026-09-19-gold-transparent-flyer-qr-design.md`

## Global Constraints

- Encode exactly `https://scienceclawhack.ai/apply.html`.
- Use exactly `#d9a038` for QR modules.
- Add no SVG background rectangle or background fill.
- Preserve the four-module transparent quiet zone.
- Keep `v2/` and `swarm/` flyer artifacts synchronized.
- Preserve untracked sponsor examples and unrelated worktree changes.

---

### Task 1: Gold transparent QR generation and verification

**Files:**
- Modify: `scripts/verify_flyer_application.py`
- Modify: `scripts/build_social_flyer.py`
- Regenerate: `v2/assets/social/scienceclaw-apply-qr.svg`
- Regenerate: `v2/assets/social/scienceclaw-hackathon-flyer-16x9.png`
- Regenerate: `v2/assets/social/scienceclaw-hackathon-flyer-16x9.pdf`
- Regenerate: `v2/assets/social/social-captions.md`
- Regenerate: `swarm/assets/social/scienceclaw-apply-qr.svg`
- Regenerate: `swarm/assets/social/scienceclaw-hackathon-flyer-16x9.png`
- Regenerate: `swarm/assets/social/scienceclaw-hackathon-flyer-16x9.pdf`
- Regenerate: `swarm/flyer.html`

**Interfaces:**
- Consumes: `APPLICATION_URL: str`, OpenCV QR matrix values, and the existing SVG `<g transform="translate(4 4)">` representation.
- Produces: `QR_MODULE_COLOR = "#d9a038"`, `build_qr_svg() -> str`, and `decode_qr_svg(path: Path) -> str` with transparent/gold presentation checks.

- [x] **Step 1: Add failing presentation assertions**

In `scripts/verify_flyer_application.py`, inspect the SVG root children before decoding. Require that the root has exactly one element child, that child is the QR module group, the group fill is `#d9a038`, and the four-module translation and field dimensions leave exactly four modules on every edge. Rasterize on black using the parsed gold fill, invert the image for light-on-dark QR polarity, and decode the result.

The key assertions are:

```python
children = list(root)
if children != [group]:
    raise AssertionError("application QR SVG must contain only its module group")
if group.attrib.get("fill") != QR_MODULE_COLOR:
    raise AssertionError("application QR modules do not use the theme gold")
if offset_x != 4 or offset_y != 4:
    raise AssertionError("application QR must retain a four-module quiet zone")
```

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python scripts/verify_flyer_application.py
```

Expected: FAIL because the current SVG contains a cream background rectangle and black modules.

- [x] **Step 2: Generate transparent gold SVG markup**

In `scripts/build_social_flyer.py`, add:

```python
QR_MODULE_COLOR = "#d9a038"
```

Update `build_qr_svg()` so the SVG contains no background rectangle and its sole child is:

```python
f'  <g transform="translate(4 4)" fill="{QR_MODULE_COLOR}">{qr_row_runs(matrix)}</g>'
```

Keep the existing `modules + 8` field dimensions so the transparent quiet zone stays four modules wide.

- [x] **Step 3: Regenerate flyer and published artifacts**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python scripts/build_social_flyer.py
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python scripts/build_sponsor_pitches.py
```

Expected: both commands exit zero and rewrite the generated flyer and sponsor PDF outputs.

- [x] **Step 4: Verify focused behavior and generated parity**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python scripts/verify_flyer_application.py
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python scripts/verify_published_flyer.py
PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python scripts/test_sponsor_pitches.py
```

Expected: every verifier exits zero; the QR decodes to the canonical application URL; source/public flyer outputs are byte-identical; sponsor exports pass their content and geometry checks.

- [x] **Step 5: Run the complete repository regression suite**

Run every tracked Python verifier/test under `scripts/`, plus JavaScript syntax checks and generated-file metadata checks:

```bash
for test in scripts/test_*.py; do PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python "$test"; done
for verifier in scripts/verify_*.py; do
  if [ "$verifier" = scripts/verify_pr1_swarm_refresh.py ]; then
    PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python "$verifier" \
      --logo-source /home/fiona/LAMM/hackathon_fall26/logos/LOGO_LAMM_full_black.svg
  else
    PYTHONDONTWRITEBYTECODE=1 /home/fiona/miniconda3/bin/python "$verifier"
  fi
done
node --check swarm/js/main.js
node --check swarm/js/scene.js
node --check swarm/js/tentacles.js
file v2/assets/social/scienceclaw-hackathon-flyer-16x9.png
pdfinfo v2/assets/social/scienceclaw-hackathon-flyer-16x9.pdf
git diff --check -- . ':(exclude)**/*.pdf'
```

Expected: all commands exit zero; PNG is 1600 × 900; PDF has one 16:9 page; no source-file whitespace errors are reported. Generated PDFs are excluded from the Git text-whitespace check because Chromium's binary cross-reference rows end in spaces.

- [ ] **Step 6: Commit the implementation**

```bash
git add scripts/build_social_flyer.py scripts/verify_flyer_application.py \
  v2/assets/social/scienceclaw-apply-qr.svg \
  v2/assets/social/scienceclaw-hackathon-flyer-16x9.png \
  v2/assets/social/scienceclaw-hackathon-flyer-16x9.pdf \
  v2/assets/social/social-captions.md \
  swarm/flyer.html swarm/assets/social \
  sponsor_pitches/exports/scienceclaw-founding-partnership-deck.pdf \
  sponsor_pitches/exports/scienceclaw-sponsorship-opportunity.pdf
git commit -m "feat: style flyer QR in transparent gold"
```
