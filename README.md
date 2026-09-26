# Vexy Screensese

Like Scorsese, but for screen recordings.

Vexy Screensese is a screen recorder with caption and keystroke/click visualisation export, an AGPLv3 fork of [Cap](https://github.com/CapSoftware/Cap).

- **Download:** [GitHub Releases](https://github.com/vexyart/vexy-screensese/releases) (macOS, Windows)
- **Docs:** [vexy.dev/vexy-screensese](http://vexy.dev/vexy-screensese/)
- **App source:** [github.com/vexyart/vexy-screensese-cap](https://github.com/vexyart/vexy-screensese-cap), branch `modified`

This repository holds the documentation site. It is published from `./docs` by GitHub Pages.

## Building the docs

The docs are built with [ProperDocs](https://properdocs.org/) and the [MaterialX](https://jaywhj.github.io/mkdocs-materialx/) theme, both installed on demand via [uv](https://docs.astral.sh/uv/).

```bash
./build.sh build   # import Cap docs, build ./docs, add .nojekyll
./build.sh serve   # local dev server with live reload at localhost:8000
```

The build reads Cap documentation from the sibling `vexy-screensese-cap` checkout. In a standalone checkout it fetches only that documentation into a temporary sparse clone.

Sources live in `src_docs/`:

- `src_docs/properdocs.yml` — site config and navigation
- `src_docs/md/` — Markdown sources; `src_docs/md/cap/` is imported from Cap's own docs
- `src_docs/import_cap_docs.py` — the repeatable import/rebrand script (see its docstring, and [the attribution page](src_docs/md/attribution.md))

`.github/workflows/docs.yml` rebuilds and commits `./docs` automatically on pushes to `main` that touch `src_docs/**`.

## Licence

Vexy Screensese is AGPLv3. See the [attribution page](src_docs/md/attribution.md) for what in this documentation is adapted from Cap's own docs.
