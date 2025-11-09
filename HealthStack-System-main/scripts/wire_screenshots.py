import re
from pathlib import Path


START_MARKER = "<!-- screenshots:auto:start -->"
END_MARKER = "<!-- screenshots:auto:end -->"
ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
IGNORED_PREFIXES = {"screenshot", "img", "image", "screen", "ss"}


def title_from_filename(name: str) -> str:
    stem = Path(name).stem
    # Replace dashes/underscores with spaces and title-case
    cleaned = re.sub(r"[-_]+", " ", stem).strip()
    return cleaned.title()


def parse_date_label(name: str) -> str | None:
    m = re.search(r"(\d{4})[-_](\d{2})[-_](\d{2})", name)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def group_from_stem(stem: str) -> str | None:
    lower = stem.lower().strip()
    # If the stem starts with generic screenshot-like prefixes, skip grouping
    space_tokens = lower.split()
    if space_tokens and space_tokens[0] in IGNORED_PREFIXES:
        return None
    # Try separators to infer a prefix-based group
    for sep in ("__", "_", "-", " "):
        if sep in stem:
            prefix = stem.split(sep)[0].strip()
            lp = prefix.lower()
            if not lp or lp in IGNORED_PREFIXES or lp.isdigit():
                continue
            return re.sub(r"[-_]+", " ", prefix).strip().title()
    # Recognize common section names directly
    recognized = {
        "homepage",
        "home",
        "dashboard",
        "patient",
        "doctor",
        "hospital",
        "pharmacy",
        "admin",
        "chat",
        "payment",
        "api",
        "ai",
    }
    if lower in recognized:
        return lower.title()
    return None


def build_block(screens_dir: Path) -> str:
    files = sorted(
        [p for p in screens_dir.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXTS],
        key=lambda p: p.name.lower(),
    )
    lines = [START_MARKER, ""]
    if not files:
        lines.append(
            "No screenshots found in `static/screenshots/`. Add PNG/JPG files to populate this section automatically."
        )
    else:
        # Build groups using prefix-based categories, then date labels, with a Misc fallback
        groups: dict[str, list[Path]] = {}
        for f in files:
            stem = f.stem
            group = group_from_stem(stem)
            if not group:
                group = parse_date_label(f.name) or "Miscellaneous"
            groups.setdefault(group, []).append(f)

        # Sort groups: named categories first (alphabetical), date groups (desc), then Miscellaneous
        date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        named_groups = sorted([g for g in groups.keys() if not date_re.match(g) and g != "Miscellaneous"], key=str.lower)
        date_groups = sorted([g for g in groups.keys() if date_re.match(g)], reverse=True)
        tail_groups = [g for g in ["Miscellaneous"] if g in groups]
        ordered_groups = named_groups + date_groups + tail_groups

        for grp in ordered_groups:
            lines.append(f"### {grp}")
            lines.append("")
            for f in sorted(groups[grp], key=lambda p: p.name.lower()):
                alt = title_from_filename(f.name)
                rel_path = f"static/screenshots/{f.name}"
                lines.append(f"![{alt}]({rel_path})")
            lines.append("")

    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def insert_or_replace(readme_text: str, block_text: str) -> str:
    if START_MARKER in readme_text and END_MARKER in readme_text:
        pattern = re.compile(
            re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
        )
        return pattern.sub(block_text, readme_text)
    # Insert after "## Screenshots" if present
    m = re.search(r"^##\s*Screenshots\s*$", readme_text, re.MULTILINE)
    if m:
        idx = m.end()
        return readme_text[:idx] + "\n\n" + block_text + "\n" + readme_text[idx:]
    # Otherwise, append a new section at the end
    return readme_text + "\n\n## Screenshots\n\n" + block_text + "\n"


def wire():
    repo_root = Path(__file__).resolve().parent.parent
    readme_path = repo_root / "README.md"
    screens_dir = repo_root / "static" / "screenshots"

    if not readme_path.exists():
        raise FileNotFoundError(f"README not found at: {readme_path}")
    screens_dir.mkdir(parents=True, exist_ok=True)

    readme_text = readme_path.read_text(encoding="utf-8")
    block_text = build_block(screens_dir)
    updated = insert_or_replace(readme_text, block_text)
    readme_path.write_text(updated, encoding="utf-8")
    print("Screenshots section wired successfully.")


if __name__ == "__main__":
    wire()