# Vexy Screensese

*Like Scorsese, but for screen recordings.*

Vexy Screensese is a screen recorder that captures your screen, camera, and microphone, then shows what happened while you were recording: every keystroke, every click, and readable captions alongside the footage. It is an AGPLv3 fork of [Cap](https://github.com/CapSoftware/Cap), the open source screen recorder.

## What it does

- **Records** your screen, camera overlay, and microphone, with Instant Mode for quick shareable links or Studio Mode for local editing before you export.
- **Visualises input** — keystrokes and clicks are captured alongside the video, so a companion tool can turn them into on-screen overlays after the fact.
- **Exports for editing** through the [`screensese`](export.md) command line tool: captions, a hard-burnt overlay video, or a chroma-keyable layer of keystroke and click graphics you can composite in any editor.
- **Self-hosts** on your own infrastructure with Docker Compose, MySQL, and S3-compatible storage — see the [self-hosting guide](cap/self-hosting.md).

## Get started

1. **[Download](download.md)** Vexy Screensese for macOS or Windows.
2. **[Install it](cap/installation.md)** and grant the recording permissions it asks for.
3. **[Record your first session](cap/quickstart.md)**.
4. Turn it into captions and overlays with **[the `screensese` exporter](export.md)**.

## Documentation

- [Introduction](cap/introduction.md) — what Vexy Screensese is and how it fits together
- [Installation](cap/installation.md) and [Quickstart](cap/quickstart.md)
- [Instant Mode](cap/recording/instant-mode.md) and [Studio Mode](cap/recording/studio-mode.md)
- [Camera & Microphone](cap/recording/camera-and-mic.md) and [Keyboard Shortcuts](cap/recording/keyboard-shortcuts.md)
- [Self-hosting](cap/self-hosting.md) and [S3-compatible storage](cap/s3-config.md)
- [The `screensese` exporter](export.md)

Most of this documentation is adapted from Cap's own docs — see the [attribution page](attribution.md) for details.

## Licence and source

Vexy Screensese is AGPLv3-licensed. Source code lives at [github.com/vexyart/vexy-screensese-cap](https://github.com/vexyart/vexy-screensese-cap), branch `modified`.
