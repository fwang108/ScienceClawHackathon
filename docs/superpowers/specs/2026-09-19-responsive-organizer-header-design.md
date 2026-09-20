# Responsive Organizer Header Design

## Goal

Keep the ScienceClaw wordmark and organizer logos readable and separate at every supported viewport width, including when a desktop browser is narrowed to phone dimensions.

## Scope

Apply the behavior to the shared header on:

- `swarm/index.html`
- `swarm/apply.html`

The flyer header and sponsor materials are unchanged.

## Responsive Behavior

At the existing mobile/tablet breakpoint, the ScienceClaw identity remains on the first header row with the Apply action aligned to its right. The identity uses the existing phone treatment: a smaller pincer mark, compact ScienceClaw lettering, and left alignment.

The MIT, LAMM, and E14 identities occupy a separate organizer region below the first row. On narrow screens, that region may wrap onto additional centered rows. The logos retain their established mobile sizes rather than shrinking to force all three onto one line.

The header grows vertically when the organizer region wraps. Homepage hero and application-page top spacing must account for that growth so the fixed header never covers page content.

## Layout Constraints

- The ScienceClaw identity and MIT identity must never intersect.
- Organizer identities must not intersect each other.
- Every header identity and the mobile action must remain fully inside the viewport.
- Verification covers header/identity viewport bounds; unrelated pre-existing main-content document overflow is outside this task's scope.
- The full wordmark text remains `ScienceClaw` at all widths.
- Desktop layout above the existing responsive breakpoint remains visually unchanged.

## Implementation Approach

Use CSS layout behavior rather than JavaScript measurement:

- Preserve the existing two-level mobile header structure.
- Allow the organizer container to wrap with centered alignment and explicit row and column gaps.
- Allow the identity grid and fixed header to derive their height from wrapped content.
- Add a narrow-screen content offset that matches the maximum wrapped header height.

No HTML restructuring or duplicated mobile markup is needed.

## Verification

Add a browser regression test for both public pages at the narrow collision range, breakpoint edges, and desktop widths. At each width, assert:

- ScienceClaw and MIT rectangles do not overlap.
- Organizer rectangles do not overlap one another.
- Header identity and mobile-action rectangles stay within the viewport.
- The rendered pincer and wordmark do not intersect the mobile action.
- Main content begins below the fixed header at narrow widths.

Run the complete existing identity and layout test suite after the focused regression passes.
