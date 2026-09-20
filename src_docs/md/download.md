# Download

Vexy Screensese builds are attached to [GitHub Releases](https://github.com/vexyart/vexy-screensese/releases) for macOS and Windows.

1. Open the [latest release](https://github.com/vexyart/vexy-screensese/releases/latest).
2. Download the installer for your platform:
   - **macOS** — the `.dmg` for Apple Silicon or Intel.
   - **Windows** — the 64-bit `.exe` installer.
3. Install it and follow the [installation guide](cap/installation.md) for permissions and setup.

There is no hosted download page or auto-update channel outside of GitHub Releases — check the releases page directly for the current version and changelog.

## Building from source

Vexy Screensese is an AGPLv3 fork of Cap. To build it yourself, clone the fork and follow its own build instructions:

```bash
git clone -b modified https://github.com/vexyart/vexy-screensese-cap.git
cd vexy-screensese-cap
```

See the repository's `README.md` and `CONTRIBUTING.md` for the desktop build toolchain (Rust, Tauri, Bun).
