# ScienceClaw Hackathon

Website for the **ScienceClaw: Internet of Agents Hackathon**, held at MIT Media Lab, October 30–November 1, 2026.

**Live site:** https://scienceclawhack.ai/

## Run locally

```bash
python3 -m http.server 8000 --directory swarm
```

Open http://localhost:8000. No installation or build step is required.

## Site files

- `swarm/index.html` — event information, judges, prizes, schedule, sponsors, and FAQ
- `swarm/apply.html` — Luma registration
- `swarm/flyer.html` — printable event flyer
- `swarm/css/`, `swarm/js/`, `swarm/assets/` — styles, interactions, and referenced artwork
- `swarm/vercel.json` — canonical-domain redirect

Deploy `swarm/` as the static site root. The repository-root page redirects to `swarm/` for previews served from the repository root.

The homepage and its assets match the live deployment retrieved on October 26, 2026. Google Fonts, Three.js, and Luma load externally; internet access is needed for those features. Animations respect reduced-motion preferences.
