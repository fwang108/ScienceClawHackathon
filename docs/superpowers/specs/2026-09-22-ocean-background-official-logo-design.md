# Ocean Background and Official Logo Design

## Goal

Replace only the ScienceClaw homepage background with the approved animated ocean-floor lobster network from `maxbauer.dev/hackathon`, and replace the homepage header and hero marks with the supplied transparent SVG identity assets.

## Approved Visual Direction

The approved preview is:

`/home/fiona/LAMM/hackathon_fall26/Hackathon_Demo_Page/.superpowers/scienceclaw-ocean-logo-preview.png`

The finished homepage must preserve the current ScienceClaw header layout, hero copy, title, typography, spacing, navigation, calls to action, content sections, and responsive behavior. Only the animated background and the two homepage ScienceClaw logo treatments change.

## Scope

### Homepage

- Use the source-faithful ocean scene from the public `add-lobster-v3` branch at `v3/js/scene-ocean.js`.
- Include its abyssal ocean floor, gold grid, sea grass, low-poly lobsters, network links, moving packets, pointer parallax, and scroll drift.
- Replace the current crane scene and tentacle overlay rather than combining animation systems.
- Keep the existing grain and scroll veil used for content readability.
- Use the supplied `SVG/white on clear.svg` as the full transparent header wordmark.
- Use the supplied `SVG/no_text.svg` as the transparent hero mark, rendered white so the existing `ScienceClaw` hero title remains readable and is not duplicated.

### Explicitly Unchanged

- `swarm/apply.html` and its visual treatment
- flyer HTML, QR, PNG, and PDF artifacts
- sponsor HTML and PDF artifacts
- all ScienceClaw homepage text and section order
- domain and Vercel configuration

## Asset Strategy

Copy the supplied SVG files byte-for-byte into `swarm/assets/logos/` using stable, space-free public filenames:

- `scienceclaw-wordmark-white.svg`
- `scienceclaw-mark-official.svg`

The homepage header references the wordmark asset directly through a new homepage-only image class. The hero references the mark-only asset through a new homepage-only image class and uses CSS presentation to render its black paths white over the dark scene. Existing `.identity__scienceclaw-mark` rules remain available to the unchanged application header. Accessible naming remains on the homepage header link and full wordmark image; the decorative hero mark remains hidden from assistive technology.

## Scene Integration

Add the approved source scene as `swarm/js/scene-ocean.js` and load it from `swarm/index.html` through the existing Three.js import map. Remove the homepage references to the legacy `scene.js` and `tentacles.js`, remove the tentacle canvas, delete `swarm/js/scene.js` and `swarm/js/tentacles.js`, and update the existing scene verifier to validate the new active file and approved upstream hash. The historical `v1/` and `v2/` trees remain unchanged.

The scene remains a fixed canvas beneath the existing document. Pointer movement and document scroll update only the scene camera; `swarm/js/main.js` continues to control navigation state, reveal behavior, and the existing readability veil independently.

## Resilience and Performance

- Preserve the scene's reduced mobile object counts at viewports up to 820px.
- Respect `prefers-reduced-motion` by rendering a stable frame without scheduling continuous animation.
- Preserve the existing `no-webgl` static fallback if renderer creation fails.
- Cap renderer pixel ratio as the source scene does.
- Do not add a build system or runtime dependency; Three.js continues to use the existing import map.

## Verification

Test-first verification must cover:

- the homepage loads only `js/scene-ocean.js` and no legacy scene or tentacle script;
- the homepage has no tentacle canvas;
- the active ocean scene matches the approved upstream source hash;
- the two copied SVGs match the supplied source hashes;
- the header renders the full official SVG and the hero renders the mark-only SVG;
- the visible hero title remains exactly `ScienceClaw` with the approved subtitle and actions;
- homepage header and hero geometry remain valid across the existing 280–1600px viewport regression range;
- the application page remains free of the new ocean scene and official homepage logo references;
- JavaScript syntax, WebGL fallback, reduced-motion behavior, and the complete existing regression suite pass;
- a final local screenshot matches the approved visual direction before deployment;
- after deployment, the live homepage serves the new scene and logos while the application page remains unchanged.

