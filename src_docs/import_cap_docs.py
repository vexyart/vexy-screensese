#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire"]
# ///
# this_file: src_docs/import_cap_docs.py
"""Import Cap's MDX documentation into plain Markdown for Vexy Screensese docs.

Converts MDX -> Markdown, rebrands "Cap" -> "Vexy Screensese" (whole word,
protecting code spans, upstream URLs, and the .cap bundle extension), skips
pages that only concern the commercial cap.so offering, and rewrites internal
links so they point at pages that were actually imported.

Repeatable: re-run any time the upstream vexy-screensese-cap docs change.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import fire

# Pages that only concern the commercial cap.so cloud offering, billing, or
# migration tooling. Their content does not apply to a self-hosted AGPL fork.
SKIP = {
    "commercial-license.mdx",
    "teams.mdx",
    "teams/google-drive.mdx",
    "migrating-to-cap.mdx",
    "api/rest-api.mdx",
    "api/webhooks.mdx",
    "sharing/analytics.mdx",
    "sharing/comments.mdx",
    "sharing/embeds.mdx",
    "sharing/share-a-cap.mdx",
    # "Cap for Agents" drives the cap.so cloud dashboard (sharing, comments,
    # analytics, spaces, browser login to cap.so) end to end. Every one of
    # those surfaces is itself skipped above, so nothing here stands on its
    # own for a self-hosted install. Judgement call, flagged in the report.
    "agents.mdx",
    "agents/setup.mdx",
    "agents/workflows.mdx",
    "agents/safety.mdx",
}

# Extra link targets that are not /docs/... pages but do have a local
# equivalent among the pages we author ourselves.
EXTRA_LINK_MAP = {
    "https://cap.so/download": "download.md",
    "https://cap.so/download/versions": "download.md",
}

# Protected literal spans: never touched by the rebrand, even outside code.
PROTECTED_LITERALS = [
    "Cap Software, Inc.",
    "github.com/CapSoftware/Cap",
    "hello@cap.so",
    "so.cap.desktop",
    "cap.so",
    "Cap.so",
    "CAP.SO",
]

# Per-destination-path manual fixups applied after the generic pipeline, for
# edits that need real judgement rather than a mechanical rule. Each is a
# literal (old, new) string pair applied with str.replace; a fixup whose
# `old` text is no longer found is reported so drift gets noticed.
POST_FIXUPS: dict[str, list[tuple[str, str]]] = {
    "self-hosting.md": [
        (
            "https://github.com/CapSoftware/Cap/issues/new",
            "https://github.com/vexyart/vexy-screensese/issues/new",
        ),
        (
            "git clone https://github.com/CapSoftware/Cap.git\ncd Cap",
            "git clone -b modified https://github.com/vexyart/vexy-screensese-cap.git\n"
            "cd vexy-screensese-cap",
        ),
        (
            "Vexy Screensese Web is our web application for uploading and "
            "sharing recordings - it's what runs right here on Cap.so.\n"
            "You can upload videos to it from the dashboard or from Vexy Screensese.",
            "Vexy Screensese Web is the web application for uploading and "
            "sharing recordings — the same codebase, as an AGPL fork, that "
            "powers Cap.so.\nYou can upload videos to it from the dashboard "
            "or from Vexy Screensese Desktop.",
        ),
        # The Railway one-click template deploys upstream Cap, not this AGPL
        # fork, so it would silently hand a self-hoster the wrong app.
        (
            "### Option 2: Railway (One-Click)\n\n"
            "[![Deploy on Railway](https://railway.com/button.svg)]"
            "(https://railway.com/new/template/PwpGcf)\n\n"
            "Railway provides a fully managed deployment with automatic SSL and scaling.\n"
            "Login credentials appear in Railway's Deploy Logs after deployment.\n\n"
            "### Option 3: Coolify",
            "### Option 2: Coolify",
        ),
    ],
    "introduction.md": [
        (
            "2. **[Record your first Vexy Screensese](quickstart.md)** in under a minute",
            "2. **[Record your first recording](quickstart.md)** in under a minute",
        ),
        (
            "Vexy Screensese is built for AI agents too. Codex, Claude Code, "
            "Cursor, OpenCode, or any shell-capable agent can record, share, "
            "search, and manage Vexy Screensese for you — one prompt sets it up.\n\n",
            "",
        ),
        (
            "- **Vexy Screensese for Agents** - Let your AI agent drive Vexy "
            "Screensese through the CLI, skill, and local MCP. It can record "
            "your screen, share links, read transcripts and summaries, and "
            "organize your library, asking for confirmation before anything "
            "changes.\n\n",
            "",
        ),
        (
            "Working with an AI agent instead? Vexy Screensese for Agents "
            "sets up the whole integration with a single copy-paste prompt.\n\n",
            "",
        ),
        (
            "## Vexy Screensese for Agents\n\n"
            "Your AI agent can use Vexy Screensese end to end: check capture "
            "readiness, record your screen, upload and return a share link, "
            "read transcripts and AI summaries, search your library, draft "
            "comments, and manage folders, spaces, and team settings. Reads "
            "are free-form; every mutation requires your explicit "
            "confirmation, and secrets never pass through chat.\n\n"
            "Start at Vexy Screensese for Agents — the one-prompt setup "
            "installs the CLI, the Vexy Screensese skill, and the local MCP "
            "server into Codex, Claude Code, Cursor, or OpenCode.\n\n",
            "",
        ),
        (
            "Recordings can be shared instantly through the Vexy Screensese "
            "cloud or your self-hosted instance.",
            "Recordings can be shared instantly through Cap.so's managed "
            "cloud or your self-hosted instance.",
        ),
        (
            "The Vexy Screensese web app at Cap.so is your dashboard",
            "The web app — self-hosted, or Cap.so's managed instance — is "
            "your dashboard",
        ),
        (
            "Vexy Screensese is open source and community-driven. You can "
            "find the source code, report issues, and contribute on "
            "[GitHub](https://github.com/CapSoftware/Cap). Join the "
            "[Vexy Screensese Discord](https://discord.gg/y8gdQ3WRN3) to "
            "connect with other users and the development team.",
            "Vexy Screensese is an AGPLv3 fork of "
            "[Cap](https://github.com/CapSoftware/Cap). Find its source, "
            "report issues, and contribute at "
            "[github.com/vexyart/vexy-screensese-cap]"
            "(https://github.com/vexyart/vexy-screensese-cap). "
            "The upstream project also has a "
            "[Discord community](https://discord.gg/y8gdQ3WRN3).",
        ),
    ],
    "quickstart.md": [
        ("you can rename a Vexy Screensese,", "you can rename a recording,"),
        ("## Manage the Vexy Screensese", "## Manage a Recording"),
        ("- Share a Vexy Screensese\n", "- Share a recording\n"),
        (
            "- Use Vexy Screensese With an Agent\n",
            "",
        ),
    ],
    "recording/camera-and-mic.md": [
        (
            "**Check that the camera feed is visible** in the Vexy Screensese preview",
            "**Check that the camera feed is visible** in the recording preview",
        ),
    ],
    "recording/studio-mode.md": [
        (
            "| Primary result | Shareable Vexy Screensese | Local editable project |",
            "| Primary result | Shareable recording | Local editable project |",
        ),
    ],
    "s3-config.md": [
        (
            "For Google Drive rather than S3, read Google Drive.",
            "See the Google Drive storage option instead of S3-compatible "
            "storage.",
        ),
    ],
    "s3-config/aws-s3.md": [
        (
            "Upload one non-sensitive sample Vexy Screensese.",
            "Upload one non-sensitive sample recording.",
        ),
        (
            "Open the Vexy Screensese link as an allowed viewer.",
            "Open the recording link as an allowed viewer.",
        ),
        (
            "Delete the sample in Vexy Screensese and confirm",
            "Delete the sample recording and confirm",
        ),
    ],
    "recording/instant-mode.md": [
        (
            "*Record and create a shareable Vexy Screensese with the shortest workflow*",
            "*Record and create a shareable recording with the shortest workflow*",
        ),
        (
            "The Vexy Screensese appears in the desktop library and web dashboard",
            "The recording appears in the desktop library and web dashboard",
        ),
        (
            "where a shareable Vexy Screensese matters more than editing first",
            "where a shareable recording matters more than editing first",
        ),
    ],
}


def _protect(text: str) -> tuple[str, dict[str, str]]:
    """Replace code spans/blocks and protected literals with placeholders."""
    placeholders: dict[str, str] = {}
    counter = 0

    def stash(match: re.Match) -> str:
        nonlocal counter
        key = f"\x00PH{counter}\x00"
        placeholders[key] = match.group(0)
        counter += 1
        return key

    # Fenced code blocks first, then inline code spans.
    text = re.sub(r"```.*?```", stash, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", stash, text)

    for literal in PROTECTED_LITERALS:
        text = re.sub(re.escape(literal), stash, text)

    return text, placeholders


def _unprotect(text: str, placeholders: dict[str, str]) -> str:
    for key, original in placeholders.items():
        text = text.replace(key, original)
    return text


def _rebrand(text: str) -> str:
    """Rebrand Cap -> Vexy Screensese as a whole word, noun-usage aware."""
    text, placeholders = _protect(text)

    # Plural noun usage ("existing Caps", "shared Caps") is unambiguous.
    # Singular "a/the Cap" is not: it is sometimes the noun for a recording
    # ("rename a Cap") and sometimes the brand name used attributively
    # ("the Cap cloud", "the Cap repository"). A regex can't reliably tell
    # these apart, so singular usage falls through to the plain brand
    # substitution below; genuine noun-usage sentences get a targeted
    # POST_FIXUPS entry instead of a guess that is wrong as often as right.
    text = re.sub(r"\bCaps\b", "recordings", text)

    # Compound brand terms.
    text = text.replace("Cap Desktop", "Vexy Screensese")
    text = text.replace("Cap Web", "Vexy Screensese Web")
    text = text.replace("Cap Pro", "Vexy Screensese")

    # Remaining bare brand-name usage, whole word only.
    text = re.sub(r"\bCap\b", "Vexy Screensese", text)

    return _unprotect(text, placeholders)


def _strip_jsx(text: str) -> str:
    """Drop import lines and convert/remove JSX components."""
    lines = [ln for ln in text.split("\n") if not re.match(r"^\s*import\s", ln)]
    text = "\n".join(lines)

    # <Warning title="...">...</Warning> (or similar) -> a blockquote.
    def warning_to_blockquote(match: re.Match) -> str:
        title = match.group("title")
        body = match.group("body").strip()
        out = [f"> **{title}**", ">"]
        out += [f"> {ln}" if ln else ">" for ln in body.split("\n")]
        return "\n".join(out)

    text = re.sub(
        r'<Warning title="(?P<title>[^"]*)">(?P<body>.*?)</Warning>',
        warning_to_blockquote,
        text,
        flags=re.DOTALL,
    )

    # Any other self-closing component, e.g. <CapEmbed src="..." />.
    text = re.sub(r"<[A-Z]\w*(\s[^>]*)?/>\s*\n?", "", text)

    # Any other paired component: drop the tags, keep inner text.
    text = re.sub(r"</?[A-Z]\w*(\s[^>]*)?>", "", text)

    return text


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        return {}, text
    raw_fm, body = match.group(1), match.group(2)
    meta: dict[str, str] = {}
    for line in raw_fm.split("\n"):
        m = re.match(r'^(\w+):\s*"?([^"]*)"?\s*$', line)
        if m:
            meta[m.group(1)] = m.group(2)
    return meta, body


def _rewrite_links(
    text: str, dest_file: Path, dest_root: Path, path_map: dict[str, str]
) -> str:
    """Rewrite /docs/... and cap.so links to point at imported pages, or
    strip the link (keeping the text) when no imported page exists.

    `dest_file` and `dest_root` are absolute paths; link targets in
    `path_map`/`EXTRA_LINK_MAP` are stored relative to `dest_root`.
    """

    def replace(match: re.Match) -> str:
        label, href = match.group("label"), match.group("href")
        anchor = ""
        lookup_href = href
        if "#" in href:
            lookup_href, anchor = href.split("#", 1)
            anchor = "#" + anchor

        target = None
        if lookup_href.startswith("/docs/"):
            key = lookup_href[len("/docs/") :].rstrip("/")
            target = path_map.get(key)
        elif lookup_href.rstrip("/") in EXTRA_LINK_MAP:
            target = EXTRA_LINK_MAP[lookup_href.rstrip("/")]
        elif lookup_href in EXTRA_LINK_MAP:
            target = EXTRA_LINK_MAP[lookup_href]
        elif "cap.so" in lookup_href.lower():
            target = None  # no local equivalent -> strip link, keep text
        else:
            return match.group(0)  # unrelated link (e.g. GitHub, Discord) untouched

        if target is None:
            return label

        # A label like "cap.so/download" would be misleading once the link
        # points at our own download page instead of cap.so.
        if "cap.so" in label.lower():
            label = "our download page"

        target_abs = dest_root / target
        rel = os.path.relpath(target_abs, start=dest_file.parent)
        return f"[{label}]({Path(rel).as_posix()}{anchor})"

    return re.sub(
        r"\[(?P<label>[^\]]*)\]\((?P<href>/docs/[^\s)]+|https?://[^\s)]+)\)",
        replace,
        text,
    )


def _build_path_map(source_root: Path) -> dict[str, str]:
    """Map original 'agents/setup' style keys -> destination path relative to
    dest_root (i.e. including the 'cap/' prefix), for every imported page."""
    mapping: dict[str, str] = {}
    for path in sorted(source_root.rglob("*.mdx")):
        rel = path.relative_to(source_root)
        rel_str = rel.as_posix()
        if rel_str in SKIP:
            continue
        key = rel_str[: -len(".mdx")]
        mapping[key] = str(Path("cap") / rel.with_suffix(".md"))
    return mapping


def _convert_file(
    src: Path, dest: Path, dest_root: Path, path_map: dict[str, str]
) -> None:
    raw = src.read_text(encoding="utf-8")
    meta, body = _frontmatter(raw)

    body = _strip_jsx(body)
    body = _rewrite_links(body, dest, dest_root, path_map)
    body = _rebrand(body)

    # Collapse 3+ blank lines, trim trailing whitespace per line.
    body = "\n".join(line.rstrip() for line in body.split("\n"))
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    title = meta.get("title", src.stem.replace("-", " ").title())
    title = _rebrand(title)
    summary = meta.get("summary", "")
    summary = _rebrand(summary) if summary else ""

    parts = [f"# {title}", ""]
    if summary:
        parts += [f"*{summary}*", ""]
    parts.append(body)

    out_text = "\n".join(parts)

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out_text, encoding="utf-8")


def main(
    source: str = (
        "/Users/adam/Developer/vcs3/github.vexyart/vexy-screensese-priv/"
        "vexy-screensese-cap/apps/web/content/docs"
    ),
    dest: str = "md",
) -> None:
    """Import Cap docs from SOURCE (MDX) into DEST (Markdown), relative to
    this script's directory unless DEST is absolute."""
    source_root = Path(source).resolve()
    script_dir = Path(__file__).parent.resolve()
    dest_root = Path(dest)
    if not dest_root.is_absolute():
        dest_root = script_dir / dest_root

    if not source_root.is_dir():
        raise SystemExit(f"Source directory not found: {source_root}")

    path_map = _build_path_map(source_root)

    imported: list[str] = []
    skipped: list[str] = []

    for src in sorted(source_root.rglob("*.mdx")):
        rel = src.relative_to(source_root)
        rel_str = rel.as_posix()
        if rel_str in SKIP:
            skipped.append(rel_str)
            continue

        dest_path = dest_root / "cap" / rel.with_suffix(".md")
        _convert_file(src, dest_path, dest_root, path_map)

        # Apply post-fixups keyed by the path under dest_root/cap/.
        fixup_key = str(rel.with_suffix(".md"))
        fixups = POST_FIXUPS.get(fixup_key, [])
        if fixups:
            text = dest_path.read_text(encoding="utf-8")
            for old, new in fixups:
                if old not in text:
                    print(f"WARNING: fixup for {fixup_key!r} did not match: {old!r}")
                    continue
                text = text.replace(old, new)
            dest_path.write_text(text, encoding="utf-8")

        imported.append(rel_str)

    unused = set(POST_FIXUPS) - {str(Path(p).with_suffix(".md")) for p in imported}
    if unused:
        print(f"WARNING: fixups defined for pages never imported: {sorted(unused)}")

    print(f"Imported {len(imported)} pages:")
    for p in imported:
        print(f"  {p}")
    print(f"\nSkipped {len(skipped)} pages:")
    for p in skipped:
        print(f"  {p}")


if __name__ == "__main__":
    fire.Fire(main)
