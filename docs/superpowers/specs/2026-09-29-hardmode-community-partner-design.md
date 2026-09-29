# Hardmode Community Partner Feature

## Goal

Feature Hardmode as a community partner on the ScienceClaw hackathon production homepage at `swarm/`.

## Design

Add a compact, dedicated Community Partner section between the final content section and the existing Apply callout. The section will show the supplied square Hardmode logo, identify Hardmode as a community partner, and link the logo to `https://hardmode.media.mit.edu/`. Keep the section consistent with the live page's black-and-gold visual system while preserving the logo's original colors. Do not label Hardmode as an organizer or sponsor.

The requested source image is `logos/HARD/HARD_MODE_Logo_Sq.png`. Once available in the workspace, copy it into `swarm/assets/logos/` so the static production page can load it using a path inside its published root.

## Scope

- Change the production `swarm/index.html` and add only the styling needed in `swarm/css/styles.css`.
- Add the copied logo under `swarm/assets/logos/`.
- Keep the existing navigation and Apply callout behavior unchanged.
- Do not change the alternate themes, sponsor materials, or deployment configuration.

## Review criteria

- The production homepage has a clearly labeled Community Partner feature above the Apply callout.
- The logo loads from a relative path within `swarm/`, remains legible at desktop and mobile widths, and has accessible text.
- Activating the logo opens Hardmode's website safely in a new tab.
- The feature does not describe Hardmode as an organizer or event sponsor.
