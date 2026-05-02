"""Generate the PF1 rules-coverage checklist from a local clone of
Foundry PF1e (https://gitlab.com/foundryvtt_pathfinder1e/foundryvtt-pathfinder1).

Usage:
    git clone --depth 1 https://gitlab.com/foundryvtt_pathfinder1e/foundryvtt-pathfinder1 /tmp/foundry-pf1
    python3 -m dnd.tools.generate_checklist \\
        --foundry /tmp/foundry-pf1 \\
        --out dnd/checklist

The script does NOT verify rules fidelity. It produces a per-pack
markdown checklist with rules-text excerpts so a human can read each
entry and tick it off after deciding whether the engine matches PF1
RAW. Update ``dnd/coverage.py`` with the verdicts as you go.

Per-row payload:
    name, type/sub-type, tags, prerequisites, source rulebook + page,
    Foundry doc id, the prose rules text (HTML → markdown), a summary
    of their mechanical encoding (count of `changes`, presence of
    `actions` / `scriptCalls`), our coverage-tracker status if we have
    a matching entry, and a blank `[ ]` checkbox + Notes line.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("This script needs PyYAML.  Install with:  pip install pyyaml",
          file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Paizo product codes → readable names
# ---------------------------------------------------------------------------

# Selected core product codes. Items with unknown codes fall through to
# showing the raw PZO id; add new entries here as you encounter them.
PRODUCT_CODES: dict[str, str] = {
    "PZO1110": "Core Rulebook",
    "PZO1115": "Advanced Player's Guide",
    "PZO1117": "Ultimate Magic",
    "PZO1118": "Bestiary",
    "PZO1119": "Bestiary 2",
    "PZO1121": "Ultimate Combat",
    "PZO1122": "Ultimate Equipment",
    "PZO1123": "Bestiary 3",
    "PZO1124": "NPC Codex",
    "PZO1126": "Mythic Adventures",
    "PZO1129": "Advanced Class Guide",
    "PZO1131": "Advanced Race Guide",
    "PZO1132": "Bestiary 4",
    "PZO1135": "Ultimate Intrigue",
    "PZO1137": "Bestiary 5",
    "PZO1140": "Occult Adventures",
    "PZO1141": "Bestiary 6",
    "PZO1144": "Ultimate Wilderness",
    "PZO1145": "Adventurer's Guide",
    "PZO1149": "Villain Codex",
    "PZO1150": "Bestiary 6",
    "PZO1153": "Ultimate Campaign",
    "PZO1156": "Heroes of the Wild",
    "PZO9280": "Goblins of Golarion",
    "PZO9408": "People of the Stars",
    "PZO9434": "Pathfinder Unchained",
    "PZO9468": "Inner Sea Magic",
    "PZO9470": "Inner Sea Bestiary",
    "PZO9472": "Inner Sea Combat",
    "PZO9473": "Inner Sea Gods",
}


# Categories to render. Each tuple is (foundry-pack-dir, output-shard-name).
# Categories not listed are skipped. ``None`` for the second element means
# "use a per-school sharding scheme defined inline".
INCLUDED_CATEGORIES: list[tuple[str, str | None]] = [
    ("feats",                 "feats"),
    ("classes",               "classes"),
    ("class-abilities",       "class-abilities"),
    ("races",                 "races"),
    ("racial-hd",             "racial-hd"),
    ("companion-features",    "companion-features"),
    ("monster-abilities",     "monster-abilities"),
    ("monster-templates",     "monster-templates"),
    ("template-abilities",    "template-abilities"),
    ("mythic-paths",          "mythic-paths"),
    ("buffs",                 "buffs"),
    ("rules",                 "rules"),
    ("basic-monsters",        "basic-monsters"),
    ("weapons-and-ammo",      "weapons-and-ammo"),
    ("armors-and-shields",    "armors-and-shields"),
    ("ultimate-equipment",    "ultimate-equipment"),
    ("items",                 "items"),
    ("spells",                None),  # special: shard by school
]


SKIPPED_CATEGORIES = {
    "technology",   # sci-fi gear, not core PF1
    "macros",       # JS scripts, not rules
    "roll-tables",  # random encounter tables, not rules
}


# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------


_TAG_REPLACEMENTS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL),
     r"\n\n### \1\n\n"),
    (re.compile(r"<h2[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL),
     r"\n\n#### \1\n\n"),
    (re.compile(r"<h3[^>]*>(.*?)</h3>", re.IGNORECASE | re.DOTALL),
     r"\n\n##### \1\n\n"),
    (re.compile(r"<(strong|b)[^>]*>(.*?)</(strong|b)>", re.IGNORECASE | re.DOTALL),
     r"**\2**"),
    (re.compile(r"<(em|i)[^>]*>(.*?)</(em|i)>", re.IGNORECASE | re.DOTALL),
     r"*\2*"),
    (re.compile(r"<p[^>]*>", re.IGNORECASE), "\n\n"),
    (re.compile(r"</p>", re.IGNORECASE), "\n"),
    (re.compile(r"<br\s*/?>", re.IGNORECASE), "\n"),
    (re.compile(r"<ul[^>]*>", re.IGNORECASE), "\n"),
    (re.compile(r"</ul>", re.IGNORECASE), "\n"),
    (re.compile(r"<ol[^>]*>", re.IGNORECASE), "\n"),
    (re.compile(r"</ol>", re.IGNORECASE), "\n"),
    (re.compile(r"<li[^>]*>", re.IGNORECASE), "\n- "),
    (re.compile(r"</li>", re.IGNORECASE), ""),
    # Tables degrade to whitespace — readable but unstructured.
    (re.compile(r"</?(table|thead|tbody|tr|td|th)[^>]*>", re.IGNORECASE), " "),
]

_REMAINING_TAGS = re.compile(r"<[^>]+>")
_TRIPLE_NEWLINE = re.compile(r"\n{3,}")
_DOUBLE_SPACE = re.compile(r"[ \t]+")
# Foundry's internal link syntax: @UUID[Compendium.pf1.feats.Item.X]{Display Name}
_FOUNDRY_LINK = re.compile(
    r"@(?:UUID|Compendium|Item)\[[^\]]*\]\{([^}]+)\}"
)
# Prose-based prerequisites extraction: "<strong>Prerequisites</strong>: ..."
# After HTML→md it's "**Prerequisites**: ..." up to next "**" or sentence end.
_PROSE_PREREQS = re.compile(
    r"\*\*Prerequisite[s]?\*\*\s*:\s*([^\n]+?)(?=\n|\*\*|$)",
    re.IGNORECASE,
)


def html_to_md(text: str | None) -> str:
    if not text:
        return ""
    out = html.unescape(text)
    out = _FOUNDRY_LINK.sub(r"\1", out)
    for pat, repl in _TAG_REPLACEMENTS:
        out = pat.sub(repl, out)
    out = _REMAINING_TAGS.sub("", out)
    out = _TRIPLE_NEWLINE.sub("\n\n", out)
    out = _DOUBLE_SPACE.sub(" ", out)
    return out.strip()


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------


def _format_sources(item: dict) -> str:
    sources = ((item.get("system") or {}).get("sources")) or []
    parts = []
    for s in sources:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("id", "")).strip()
        pages = s.get("pages")
        book = PRODUCT_CODES.get(sid, sid or "?")
        if pages not in (None, "", []):
            parts.append(f"{book} ({sid}) p. {pages}")
        else:
            parts.append(f"{book} ({sid})")
    return "; ".join(parts) if parts else "—"


def _format_prereqs(item: dict, desc_md: str) -> str:
    """Extract prerequisites: prefer structured field, fall back to prose.

    Most Foundry PF1 items don't have a structured ``system.prerequisites``
    field — the prereqs live only in the prose ``description.value``
    behind a "**Prerequisites**:" lead. We try the structured form
    first, then regex the (already-converted) markdown prose.
    """
    sys_ = item.get("system") or {}
    prereq = sys_.get("prerequisites") or sys_.get("prereq")
    if isinstance(prereq, dict) and prereq:
        bits = [f"{k}: {v}" for k, v in sorted(prereq.items())]
        return "; ".join(bits)
    if isinstance(prereq, list) and prereq:
        return "; ".join(str(x) for x in prereq)
    if isinstance(prereq, str) and prereq.strip():
        return prereq.strip()
    # Prose fallback.
    if desc_md:
        m = _PROSE_PREREQS.search(desc_md)
        if m:
            return m.group(1).strip().rstrip(".")
    return "—"


def _format_tags(item: dict) -> str:
    sys_ = item.get("system") or {}
    tags = sys_.get("tags")
    if not tags:
        return "—"
    if isinstance(tags, dict):
        # Foundry sometimes uses a dict-of-flags instead of a list.
        out = [k for k, v in tags.items() if v]
        return ", ".join(out) if out else "—"
    if isinstance(tags, list):
        flat = []
        for t in tags:
            if isinstance(t, str):
                flat.append(t)
            elif isinstance(t, dict):
                flat.append(t.get("name") or t.get("id") or str(t))
        return ", ".join(flat) if flat else "—"
    return str(tags)


def _summarize_changes(item: dict, max_lines: int = 5) -> tuple[int, list[str]]:
    sys_ = item.get("system") or {}
    changes = sys_.get("changes") or {}
    out_lines: list[str] = []
    if isinstance(changes, dict):
        seq = list(changes.values())
    elif isinstance(changes, list):
        seq = changes
    else:
        return 0, []
    for c in seq[:max_lines]:
        if not isinstance(c, dict):
            continue
        f = c.get("formula", "")
        t = c.get("target", "")
        ty = c.get("type", "")
        out_lines.append(f"  - `{f}` → `{t}`  ({ty})")
    return len(seq), out_lines


def _has_actions(item: dict) -> bool:
    sys_ = item.get("system") or {}
    actions = sys_.get("actions")
    if isinstance(actions, dict):
        return bool(actions)
    if isinstance(actions, list):
        return bool(actions)
    return False


def _has_scripts(item: dict) -> bool:
    sys_ = item.get("system") or {}
    return bool(sys_.get("scriptCalls"))


# ---------------------------------------------------------------------------
# Coverage cross-reference
# ---------------------------------------------------------------------------


_COVERAGE_CATEGORY_MAP: dict[str, str | None] = {
    "feats":              "feats",
    "races":              "player_race_traits",
    "class-abilities":    "class_features_l1",
    "monster-abilities":  "monster_racial_traits",
    # No 1:1 lookup for spells, classes, items, etc.
}


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _lookup_coverage(category: str, name: str) -> str:
    cov_key = _COVERAGE_CATEGORY_MAP.get(category)
    if cov_key is None:
        return "n/a (no per-name lookup for this category)"
    try:
        from dnd.coverage import CATEGORIES as COVERAGE_CATEGORIES
    except ImportError:
        return "could not import dnd.coverage"
    cov_dict = COVERAGE_CATEGORIES.get(cov_key)
    if cov_dict is None:
        return f"category {cov_key!r} missing from coverage.py"
    slug = _slugify(name)
    if slug in cov_dict:
        status, note = cov_dict[slug]
        return f"`{status}` — {note}"
    return f"absent (slug `{slug}` not in `coverage.{cov_key.upper()}`)"


# ---------------------------------------------------------------------------
# Row rendering
# ---------------------------------------------------------------------------


def render_row(item: dict, category: str) -> str:
    name = item.get("name", "<unnamed>")
    item_id = str(item.get("_id", "?"))
    sys_ = item.get("system") or {}
    type_ = item.get("type", "") or ""
    sub_type = sys_.get("subType") or ""

    sources = _format_sources(item)
    tags = _format_tags(item)
    desc_md = html_to_md((sys_.get("description") or {}).get("value", ""))
    prereq = _format_prereqs(item, desc_md)
    change_count, change_summary = _summarize_changes(item)
    has_actions = _has_actions(item)
    has_scripts = _has_scripts(item)
    coverage = _lookup_coverage(category, name)

    header_type = type_
    if sub_type and sub_type != type_:
        header_type = f"{type_} / {sub_type}"

    lines: list[str] = []
    lines.append(f"### {name}")
    if header_type:
        lines.append(f"*({header_type})*")
    lines.append("")
    lines.append(f"**Tags:** {tags}")
    lines.append(f"**Prerequisites:** {prereq}")
    lines.append(f"**Source:** {sources}")
    lines.append(f"**Foundry id:** `{item_id}`")
    lines.append("")

    if desc_md:
        for line in desc_md.split("\n"):
            lines.append(f"> {line}" if line.strip() else ">")
        lines.append("")

    encoding_bits: list[str] = []
    if change_count > 0:
        encoding_bits.append(
            f"`changes`: {change_count}"
            + (" (showing first 5)" if change_count > 5 else "")
        )
    if has_actions:
        encoding_bits.append("has `actions`")
    if has_scripts:
        encoding_bits.append("has `scriptCalls`")

    if encoding_bits:
        lines.append("**Mechanical encoding:** " + ", ".join(encoding_bits))
        lines.extend(change_summary)
        lines.append("")
    else:
        lines.append("*No mechanical encoding — prose only.*")
        lines.append("")

    lines.append(f"**In our coverage tracker:** {coverage}")
    lines.append("**Manual verdict:** `[ ]`")
    lines.append("**Notes:**")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pack iteration
# ---------------------------------------------------------------------------


def _iter_pack_yamls(pack_dir: Path) -> list[Path]:
    """All YAML files in a pack directory (recursive)."""
    return sorted(p for p in pack_dir.rglob("*.yaml") if p.is_file())


def _load_yaml(path: Path) -> dict | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"  [warn] couldn't parse {path}: {e}", file=sys.stderr)
        return None
    return data if isinstance(data, dict) else None


def _shard_path_for_spell(item: dict, out_root: Path) -> Path:
    """Spells get sharded by school."""
    sys_ = item.get("system") or {}
    school = (sys_.get("school") or "unknown").strip().lower()
    return out_root / "spells" / f"{school}.md"


def _category_header(category: str, item_count: int) -> str:
    lines = [
        f"# PF1 Rules Checklist — {category}",
        "",
        f"_Auto-generated from a Foundry PF1e pack snapshot. **Do not edit by hand.**_",
        f"_Items in this shard: {item_count}._",
        "",
        "Status legend (for the `Manual verdict:` field below):",
        "- `[x]` verified — engine matches RAW",
        "- `[~]` partial  — engine has some of it; gap noted",
        "- `[-]` absent   — not in our content / engine",
        "- `[!]` buggy    — implemented but doesn't match RAW",
        "",
        "Update `dnd/coverage.py` with the verdict after marking a row.",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def render_category(
    pack_dir: Path,
    out_path: Path | None,
    category: str,
    out_root: Path,
) -> int:
    """Render one Foundry pack as one (or several) markdown shards.

    Returns the number of items rendered.
    """
    items = _iter_pack_yamls(pack_dir)
    if not items:
        return 0

    # Spells: shard by school.
    if category == "spells":
        buckets: dict[Path, list[str]] = {}
        for path in items:
            data = _load_yaml(path)
            if not data or not data.get("name"):
                continue
            shard = _shard_path_for_spell(data, out_root)
            buckets.setdefault(shard, []).append(render_row(data, category))
        total = 0
        for shard_path, rows in buckets.items():
            shard_path.parent.mkdir(parents=True, exist_ok=True)
            school = shard_path.stem
            with shard_path.open("w", encoding="utf-8") as f:
                f.write(_category_header(f"spells / {school}", len(rows)))
                for row in rows:
                    f.write(row)
                    f.write("\n")
            total += len(rows)
        return total

    # Default: one shard per pack.
    if out_path is None:
        return 0
    rows: list[str] = []
    for path in items:
        data = _load_yaml(path)
        if not data or not data.get("name"):
            continue
        rows.append(render_row(data, category))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(_category_header(category, len(rows)))
        for row in rows:
            f.write(row)
            f.write("\n")
    return len(rows)


def render_index(out_root: Path, summary: list[tuple[str, int, Path]]) -> None:
    lines = [
        "# PF1 Rules Checklist — Index",
        "",
        "_Auto-generated. Each shard below is a manual-verdict checklist for one_",
        "_category of PF1 content from the Foundry PF1e dataset. Tick the_",
        "_`[ ]` boxes as you walk each shard, then update `dnd/coverage.py`._",
        "",
        "| Category | Items | File |",
        "|---|---:|---|",
    ]
    for cat, n, rel in summary:
        lines.append(f"| {cat} | {n} | [{rel}]({rel}) |")
    lines.append("")
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "00_index.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(prog="generate_checklist")
    parser.add_argument(
        "--foundry", required=True,
        help="Path to a checkout of foundryvtt-pathfinder1.",
    )
    parser.add_argument(
        "--out", default="dnd/checklist",
        help="Directory to write the generated markdown into.",
    )
    args = parser.parse_args()

    foundry_root = Path(args.foundry)
    packs_dir = foundry_root / "packs"
    if not packs_dir.is_dir():
        print(f"error: {packs_dir} does not exist or is not a directory",
              file=sys.stderr)
        sys.exit(1)
    out_root = Path(args.out)

    summary: list[tuple[str, int, Path]] = []

    for category, shard_name in INCLUDED_CATEGORIES:
        pack_dir = packs_dir / category
        if not pack_dir.is_dir():
            print(f"  [warn] pack {category} not present at {pack_dir}; skipping",
                  file=sys.stderr)
            continue
        if shard_name is None:
            # Special-case: spells (sharded by school inside render_category)
            count = render_category(pack_dir, None, category, out_root)
            # Add one summary row per generated shard.
            spells_root = out_root / "spells"
            for shard_path in sorted(spells_root.glob("*.md")):
                # Count rows by re-reading "items in this shard:" header.
                with shard_path.open("r") as f:
                    head = f.read(2048)
                m = re.search(r"Items in this shard: (\d+)", head)
                n = int(m.group(1)) if m else 0
                rel = shard_path.relative_to(out_root)
                summary.append((f"spells / {shard_path.stem}", n, rel))
            print(f"  [ok] {category}: {count} items "
                  f"→ sharded by school into {spells_root}")
        else:
            out_path = out_root / f"{shard_name}.md"
            count = render_category(pack_dir, out_path, category, out_root)
            if count > 0:
                summary.append((category, count, out_path.relative_to(out_root)))
            print(f"  [ok] {category}: {count} items → {out_path}")

    render_index(out_root, summary)
    total = sum(n for _, n, _ in summary)
    print(f"\nDone. {len(summary)} shard(s); {total} total items.")
    print(f"Index: {out_root / '00_index.md'}")


if __name__ == "__main__":
    main()
