# The `screensese` exporter

`screensese` is a companion command-line tool for turning a Vexy Screensese recording bundle into captions, overlays, and burnt-in video. It reads the keystroke and click data that Vexy Screensese records alongside the video and renders it in different forms depending on what you need.

This page describes the tool at a conceptual level; it is being built alongside this documentation site.

## Commands

### `screensese info BUNDLE`

Prints metadata about a recording bundle: duration, resolution, and what event data (keys, moves, clicks) is available.

### `screensese events BUNDLE`

Prints the raw event stream — keystrokes, mouse moves, and clicks — as JSONL, one event per line. Useful for building your own tooling on top of the recorded input data.

### `screensese captions BUNDLE --format vtt|srt [--keys]`

Generates soft caption files (WebVTT or SRT) from the recording. Pass `--keys` to include keystrokes in the caption track alongside spoken captions, so viewers can follow what was typed without an on-screen overlay.

### `screensese overlay BUNDLE`

Renders a hard-captions video: keystroke visualisation and click markers composited on a solid key colour (default black), intended for keying out in a video editor. This lets you drop the overlay onto your own footage with full control over blending and timing in your editor of choice.

### `screensese burn BUNDLE`

Renders the screen recording with keyboard and click overlays burnt directly into the video — a single finished file, no compositing required.

## Keystroke visualisation

Keystrokes appear as white text on a black rounded rectangle that follows the pointer. Text appears and disappears instantly as keys are pressed and released; while a key is held, the label stays on screen. Larger key combinations (for example, a chord like `Cmd+Shift+P`) linger on screen a little longer than a single key press, so viewers have time to read them. Size is configurable.

## Click visualisation

Clicks are drawn as circles at the click location:

- **Blue** — left click
- **Red** — right click
- **Solid filled circle** — single click
- **Small filled dot inside a larger ring** — double click

Size is configurable.
