# Gold Transparent Flyer QR Design

## Goal

Make the ScienceClaw flyer QR code visually match the event theme while continuing to send scanners to the canonical application page.

## Approved Treatment

- Encode exactly `https://scienceclawhack.ai/apply.html`.
- Render every QR module in the theme accent gold `#d9a038`.
- Keep the SVG background transparent by omitting any background rectangle or fill.
- Preserve a four-module transparent quiet zone around the QR modules.
- Display the transparent QR over the flyer's existing black application panel.

## Generated Artifacts

The existing flyer build remains the single source of truth. Running `scripts/build_social_flyer.py` regenerates and republishes:

- `v2/assets/social/scienceclaw-apply-qr.svg`
- `v2/assets/social/scienceclaw-hackathon-flyer-16x9.png`
- `v2/assets/social/scienceclaw-hackathon-flyer-16x9.pdf`
- `v2/assets/social/social-captions.md`
- the corresponding deployable files under `swarm/`

The sponsor export build is rerun so its generated PDFs remain synchronized with the public application URL and theme assets.

## Verification

Automated verification must establish that:

- the SVG has no background rectangle;
- its module group uses exactly `#d9a038`;
- its module group remains offset by four modules on each side;
- the encoded payload is exactly the canonical application URL;
- the QR can be decoded from its real gold-on-black flyer presentation;
- source and published flyer artifacts match after regeneration;
- the existing flyer, sponsor, identity, and domain regressions still pass.

