# Installation

*Install Vexy Screensese and grant recording permissions*

Vexy Screensese release builds are available for Apple Silicon and Intel Macs, 64-bit Windows, and 64-bit Linux through a Debian package.

Download the current build from [our download page](../download.md). The download page detects common platforms, and the [versions page](../download.md) lists the available installers directly.

## macOS

1. Download the correct `.dmg` for Apple Silicon or Intel.
2. Open it and drag **Vexy Screensese** into **Applications**.
3. Open Vexy Screensese from Applications or Spotlight.
4. Approve the standard downloaded-application prompt if macOS shows it.

Vexy Screensese requests system permissions when a feature first needs them:

- **Screen & System Audio Recording** for display, window, and area capture
- **Microphone** for microphone audio
- **Camera** for camera capture or an overlay

If a permission was denied, open **System Settings > Privacy & Security**, enable Vexy Screensese in the corresponding section, then restart Vexy Screensese if the operating system asks you to.

System-audio support can depend on the macOS version and selected capture path. Keep Vexy Screensese and macOS current if an audio source is unavailable.

## Windows

1. Download the 64-bit `.exe` installer.
2. Run it and follow the installer prompts.
3. Open Vexy Screensese from the Start menu.

Windows manages camera and microphone access under **Settings > Privacy** on Windows 10 or **Settings > Privacy & security** on Windows 11. Make sure desktop applications can access the selected device. Screen capture uses the native Windows capture path and does not present the same separate Screen Recording permission used by macOS.

## Linux

Vexy Screensese's release workflow currently publishes an x86_64 `.deb` package for Debian-compatible distributions. Install the package with your system's package manager, then launch Vexy Screensese from the application menu.

The package declares the GTK, WebKit, app-indicator, VA, PipeWire, and ALSA runtime dependencies it needs. Linux environments vary, so capture source and audio availability can depend on the desktop session and installed system services.

## Updates

Vexy Screensese checks its signed update channel in production builds. macOS and Windows can install supported application updates from Vexy Screensese. Linux `.deb` updates require the package-manager installation flow rather than an automatic privileged install.

## Verify the installation

1. Sign in to Vexy Screensese.
2. Choose a non-sensitive display, window, or area.
3. Record a short test.
4. Stop and confirm the result plays.
5. If using Instant Mode, wait for the share link to finish processing and open it in a browser.

## Uninstall

On macOS, move Vexy Screensese from Applications to the Trash. Production settings and the default recordings directory are under `~/Library/Application Support/so.cap.desktop`. A custom recordings folder stays wherever you selected it.

On Windows or Linux, remove Vexy Screensese through the operating system's installed-app or package-management interface. Back up any local Studio projects you want to keep before removing application data.
