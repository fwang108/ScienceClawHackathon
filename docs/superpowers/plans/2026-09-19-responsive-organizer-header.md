# Responsive Organizer Header Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep the phone-style ScienceClaw wordmark and organizer identities separate and visible within the shared header when it narrows.

**Architecture:** Preserve the existing shared HTML and responsive breakpoint. Add one real-browser geometry regression to the identity suite, then add a narrow-screen CSS refinement that lets the organizer group wrap and lets the header derive its height from that content.

**Tech Stack:** Static HTML/CSS, Python `unittest`, Playwright Chromium

**Spec:** `docs/superpowers/specs/2026-09-19-responsive-organizer-header-design.md`

## Global Constraints

- Apply the change only to the shared headers in `swarm/index.html` and `swarm/apply.html` through their common stylesheet.
- Preserve the existing compact phone wordmark, full `ScienceClaw` text, and desktop layout.
- Keep MIT, LAMM, and E14 at their established mobile sizes; wrap rather than shrink when space is insufficient.
- Support viewport widths of 280px and wider without header identity/action overlap and with their bounds inside the viewport; unrelated pre-existing main-content document overflow is outside this task's scope.
- Keep main content visibly below the fixed header when organizer identities wrap.
- Do not change flyer or sponsor-material layouts.

---

### Task 1: Make the shared organizer header wrap safely

**Files:**
- Modify: `scripts/test_scienceclaw_rebrand.py`
- Modify: `swarm/css/styles.css`

**Interfaces:**
- Consumes: Existing `.nav`, `.nav__identity-row`, `.identity--scienceclaw`, `.identity__institutions`, `.identity--mit`, `.identity--lamm`, `.identity--e14`, `.nav__mobile-action`, `.hero`, and `.apply-main` selectors.
- Produces: Responsive browser behavior with no new JavaScript or HTML interface.

- [ ] **Step 1: Add a failing real-browser header-geometry regression**

Add this method to `ScienceClawRenderedIdentityTests` in `scripts/test_scienceclaw_rebrand.py`:

```python
    def test_shared_header_identities_keep_visible_wordmark_clear_of_action(self) -> None:
        pages = (
            (ROOT / "swarm" / "index.html", ".hero__meta"),
            (ROOT / "swarm" / "apply.html", ".apply-shell"),
        )
        widths = (280, 320, 375, 768, 1240, 1440)

        for path, content_selector in pages:
            for width in widths:
                with self.subTest(page=path.relative_to(ROOT), width=width):
                    page = self.browser.new_page(
                        viewport={"width": width, "height": 900}
                    )
                    page.goto(path.as_uri(), wait_until="domcontentloaded")
                    geometry = page.evaluate(
                        """({ contentSelector }) => {
                          const selectors = [
                            '.identity--scienceclaw',
                            '.identity--mit',
                            '.identity--lamm',
                            '.identity--e14'
                          ];
                          const boxes = selectors.map((selector) => {
                            const rect = document.querySelector(selector).getBoundingClientRect();
                            return {
                              selector,
                              left: rect.left,
                              right: rect.right,
                              top: rect.top,
                              bottom: rect.bottom
                            };
                          });
                          const intersects = (a, b) =>
                            a.left < b.right && a.right > b.left &&
                            a.top < b.bottom && a.bottom > b.top;
                          const overlaps = [];
                          for (let first = 0; first < boxes.length; first += 1) {
                            for (let second = first + 1; second < boxes.length; second += 1) {
                              if (intersects(boxes[first], boxes[second])) {
                                overlaps.push([boxes[first].selector, boxes[second].selector]);
                              }
                            }
                          }
                          const header = document.querySelector('.nav').getBoundingClientRect();
                          const content = document.querySelector(contentSelector).getBoundingClientRect();
                          return {
                            boxes,
                            overlaps,
                            headerBottom: header.bottom,
                            contentTop: content.top,
                            wordmark: document.querySelector('.identity__scienceclaw-word').textContent.trim()
                          };
                        }""",
                        {"contentSelector": content_selector},
                    )
                    page.close()

                    self.assertEqual(geometry["wordmark"], "ScienceClaw")
                    self.assertEqual(geometry["overlaps"], [])
                    for box in geometry["boxes"]:
                        self.assertGreaterEqual(box["left"], 0, box)
                        self.assertLessEqual(box["right"], width, box)
                    if width <= 375:
                        self.assertGreaterEqual(
                            geometry["contentTop"], geometry["headerBottom"]
                        )
```

This regression covers header identity bounds and the mobile wordmark/action geometry. It does not make an assertion about unrelated main-content document overflow.

- [ ] **Step 2: Run the focused test and verify the red phase**

Run:

```bash
python scripts/test_scienceclaw_rebrand.py \
  ScienceClawRenderedIdentityTests.test_shared_header_identities_keep_visible_wordmark_clear_of_action
```

Expected: FAIL at the reported narrow collision widths while the rendered wordmark intersects the mobile action.

- [ ] **Step 3: Add the minimal narrow-screen wrapping CSS**

Add this block immediately after the existing `@media (max-width: 1240px)` block in `swarm/css/styles.css`:

```css
@media (max-width: 480px) {
  .nav__identity-row {
    min-height: 0;
    grid-template-columns: minmax(0, 1fr) auto;
    grid-template-rows: 42px auto;
    gap: 0.55rem 0.8rem;
    padding-bottom: 0.75rem;
  }

  .identity--scienceclaw {
    grid-column: 1;
  }

  .identity__institutions {
    grid-column: 1 / -1;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .nav__mobile-action {
    grid-column: 2;
  }

  .hero,
  .apply-main {
    padding-top: 12rem;
  }
}
```

The first row continues to use the established phone wordmark styles from the 1240px breakpoint. At 280px, the organizer group wraps while retaining the existing 96px MIT, 145px LAMM, and 27px E14 treatments.

- [ ] **Step 4: Run the focused test and verify the green phase**

Run:

```bash
python scripts/test_scienceclaw_rebrand.py \
  ScienceClawRenderedIdentityTests.test_shared_header_identities_keep_visible_wordmark_clear_of_action
```

Expected: `Ran 1 test` and `OK`.

- [ ] **Step 5: Run the complete local regression suite**

Run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/verify_mit_footer.py
python scripts/verify_scienceclaw_headline.py
```

Expected: all unit/browser tests report `OK`; both verifiers print `PASS` results.

- [ ] **Step 6: Inspect the final diff for scope and whitespace errors**

Run:

```bash
git diff --check
git diff -- scripts/test_scienceclaw_rebrand.py swarm/css/styles.css
```

Expected: no `git diff --check` output; the diff contains only the responsive regression and narrow-screen CSS refinement for this feature.

- [ ] **Step 7: Commit the responsive header change**

```bash
git add scripts/test_scienceclaw_rebrand.py swarm/css/styles.css
git commit -m "fix: wrap organizer logos on narrow screens"
```
