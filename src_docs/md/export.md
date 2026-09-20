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

### `screensese all BUNDLE`

Runs everything above in one go and writes the results into `BUNDLE/exports/`: captions as WebVTT and SRT with keyboard shortcuts included, the event list, the overlay and the burnt-in video.

## Options worth knowing

| Option | Effect |
| --- | --- |
| `overlay --alpha` | A transparent ProRes 4444 `.mov` instead of a key colour |
| `--background=green` | Key colour for `overlay` (default black) |
| `--key_size`, `--click_size`, `--caption_size` | Sizes, as fractions of frame height |
| `--caption_top` | Captions at the top instead of the bottom |
| `--key_corner` | Keystroke badge parked bottom-left instead of following the pointer |
| `--glyphs` | `⌘⇧K` instead of `Shift+Cmd+K` |
| `--shortcuts_only` | Hide plain typing, keep shortcuts and named keys |
| `--raw` | Ignore the editor's cuts and speed changes |
| `--captions_from=FILE` | Use your own `.srt`, `.vtt` or Whisper `.json` transcript |
| `--event_offset=SECONDS` | Shift keys, clicks and pointer if they lead or lag the video |

All options go after the command and the bundle: `screensese burn Demo.cap --raw --glyphs`.

Recordings made on Windows show `Win` where a Mac shows `Cmd`.

## View follows action

Give `burn` a canvas and the picture moves with the work.

```bash
screensese burn Demo.cap --canvas=1920x1080              # follow the pointer
screensese burn Demo.cap --canvas=1920x1080 --leave=pan  # pan between close views instead of zooming out
screensese burn Demo.cap --canvas=1920x1080 --view=keys  # views you chose while recording
```

The **far view** shows the largest canvas-shaped part of the recording, scaled to fit. The nine **close views** map recording pixels to canvas pixels at `--ratio` (default `1:1`) and sit at the corners, the edges and the centre: `left-top`, `xcenter-top`, `right-top`, `left-ymiddle`, `center`, `right-ymiddle`, `left-bottom`, `xcenter-bottom`, `right-bottom`.

With `--view=auto` the view starts in the centre. The moment the pointer leaves the centre rectangle, the view zooms out to far, or with `--leave=pan` pans to the close view that holds the pointer. It returns to the centre only after the pointer has stayed there for `--center_after` seconds (default 1.5).

With `--view=keys` you direct the views while recording: hold `Ctrl+Alt` (change it with `--view_chord`) and press `0` for far or `1` to `9` for the close views in reading order. These presses never show up in the keystroke overlay.

`--transition` sets the seconds per zoom or pan; `0` cuts. Overlays are drawn after the move, so badges and click marks keep their size and stay with the pointer.

## Keystroke visualisation

Keystrokes appear as white text on a black rounded rectangle that follows the pointer. Text appears and disappears instantly as keys are pressed and released; while a key is held, the label stays on screen. Larger key combinations (for example, a chord like `Cmd+Shift+P`) linger on screen a little longer than a single key press, so viewers have time to read them. Size is configurable.

## Click visualisation

Clicks are drawn as circles at the click location:

- **Blue** — left click
- **Red** — right click
- **Solid filled circle** — single click
- **Small filled dot inside a larger ring** — double click

Size is configurable.
