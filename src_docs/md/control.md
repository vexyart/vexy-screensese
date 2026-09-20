# Operate it from anywhere

One set of operations, reachable from the command line, from AI agents over MCP, over a local HTTP API and from Python.

## Command line

```bash
screensese ops                                     # every operation and its parameters
screensese record start --screen=1 --duration=60   # record without touching the app's windows
screensese record stop                             # prints the .cap bundle path
screensese app open_editor Demo.cap                # drive the desktop app itself
screensese burn Demo.cap --social=1080x1920
```

Structured results print as JSON. Options go after the command and the bundle.

The app's **Settings > CLI** page installs the bundled recorder command under the name `screensese`. The Python package installs a `screensese` as well, which is the superset: it passes the recorder's own commands (`export`, `project`, `targets`, `recordings`, `screenshot`, `doctor`) to the same bundled binary and adds the exports described on the [exporter page](export.md).

## MCP

```bash
uv tool install "vexy-screensese[mcp]"
claude mcp add screensese -- screensese mcp
```

One tool per operation, with schemas taken from the operations themselves. A typical agent flow: `targets`, `record_start`, `record_stop`, then `burn` on the bundle path that `record_stop` returned.

## HTTP

```bash
screensese serve --port=8765      # prints the bearer token it expects
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8765/v1/ops
curl -H "Authorization: Bearer $TOKEN" -d '{"bundle":"Demo.cap","social":"1080x1920"}' http://127.0.0.1:8765/v1/ops/burn
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8765/v1/jobs/JOB_ID
```

The server listens on `127.0.0.1` only and needs the token on every request. Renders run as jobs: the first call answers with a job id to poll. It can start recordings and read your files, so do not expose it to a network.

## Python

```python
from vexy_screensese import ops

session = ops.record_start(screen="1", duration=30)
ops.burn(session["path"], social="1080x1920", timeflex=True)
```
