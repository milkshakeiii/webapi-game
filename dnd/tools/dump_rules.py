"""Scrape PF1 core-mechanic rules pages from d20pfsrd.com into
``dnd/checklist/rules/<slug>.md``.

Companion to ``generate_checklist.py``. The Foundry-PF1e checklist
covers content (feats, spells, monsters, items, etc.) but its ``rules``
pack is empty — Foundry doesn't pack the CRB rules chapters. d20pfsrd
*does* host the full RAW prose under the OGL, so we mirror the relevant
chapters here for offline reference when implementing core mechanics.

Output is a one-shot snapshot. The pages don't change often and every
re-run will overwrite the shards, so commit the output and treat the
script as a way to refresh it later if needed.

### Running

``markdownify`` and ``beautifulsoup4`` are not in stdlib. Use a venv
to keep system Python clean::

    python3 -m venv /tmp/rulesenv
    /tmp/rulesenv/bin/pip install markdownify beautifulsoup4
    /tmp/rulesenv/bin/python -m dnd.tools.dump_rules \\
        --out dnd/checklist/rules

The d20pfsrd article body lives in ``<article>``; we strip the
sidebar/ad/related-posts noise around it and run ``markdownify`` on
what's left.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# What to scrape
#
# Each entry: (slug, url, human title). Slugs become file names —
# ``combat`` -> ``dnd/checklist/rules/combat.md``.
#
# The list is hand-curated for what our engine actually needs in core
# mechanics RAW text. Add more if you find gaps.
# ---------------------------------------------------------------------------

PAGES: list[tuple[str, str, str]] = [
    ("combat", "https://www.d20pfsrd.com/gamemastering/combat/",
     "Combat"),
    ("magic", "https://www.d20pfsrd.com/magic/",
     "Magic"),
    ("conditions", "https://www.d20pfsrd.com/gamemastering/conditions/",
     "Conditions"),
    ("special-abilities",
     "https://www.d20pfsrd.com/gamemastering/special-abilities/",
     "Special Abilities"),
    ("skills", "https://www.d20pfsrd.com/skills/",
     "Skills"),
    ("exploration-movement",
     "https://www.d20pfsrd.com/gamemastering/exploration-movement",
     "Exploration and Movement"),
    ("animal-companions",
     "https://www.d20pfsrd.com/classes/core-classes/druid/animal-companions/",
     "Animal Companions"),
    ("familiars",
     "https://www.d20pfsrd.com/classes/core-classes/wizard/familiar",
     "Familiars"),
]

USER_AGENT = "Mozilla/5.0 (compatible; webapi-game/dump_rules)"


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="replace")


def _extract_article(html: str) -> str | None:
    """Return the inner HTML of the first ``<article>`` element."""
    m = re.search(r"<article\b[^>]*>(.*?)</article>",
                  html, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else None


def _strip_noise(html: str) -> str:
    """Drop non-content blocks (scripts, styles, ad/share widgets)
    that d20pfsrd embeds inside the article body."""
    # script / style / iframe — never useful prose.
    for tag in ("script", "style", "iframe", "noscript"):
        html = re.sub(
            rf"<{tag}\b[^<]*(?:(?!</{tag}>)<[^<]*)*</{tag}>",
            "", html, flags=re.DOTALL | re.IGNORECASE,
        )
    # Common WordPress ad / nav widgets by class, identified after
    # eyeballing rendered output. Drop the whole div.
    noise_classes = (
        "ogn-ad-block",
        "share-buttons",
        "post-meta",
        "addtoany",
        "wp-block-buttons",
        "yarpp-related",
        "post-navigation",
        "comments-area",
    )
    for cls in noise_classes:
        html = re.sub(
            rf'<div[^>]*\bclass="[^"]*\b{cls}\b[^"]*"[^>]*>'
            rf'.*?</div>',
            "", html, flags=re.DOTALL | re.IGNORECASE,
        )
    return html


def _convert(html: str) -> str:
    from markdownify import markdownify  # type: ignore[import]
    md = markdownify(html, heading_style="ATX", bullets="-")
    md = _trim_chrome(md)
    # markdownify likes 4+ blank lines from <p><br/></p> chains; collapse.
    md = re.sub(r"\n{3,}", "\n\n", md)
    # Trim trailing whitespace per line.
    md = "\n".join(line.rstrip() for line in md.splitlines())
    return md.strip() + "\n"


# Markers that bound the actual rules content. Everything before the
# first ``# `` heading is breadcrumbs / ads; everything after these
# tail markers is unrelated WordPress chrome (Discord links, product
# carousels). The OGL "Section 15" copyright block stays because OGC
# republication legally requires it.
_TAIL_CUTOFFS = (
    "\n#### Discuss!",
    "\n#### [RSS]",
    "\n#### Latest Pathfinder",
)


def _trim_chrome(md: str) -> str:
    # Drop preamble before the first H1.
    m = re.search(r"^# [^\n]", md, re.MULTILINE)
    if m:
        md = md[m.start():]
    # Drop trailing footer chrome.
    for marker in _TAIL_CUTOFFS:
        i = md.find(marker)
        if i != -1:
            md = md[:i]
    return md


def _banner(title: str, url: str) -> str:
    return (
        f"# PF1 Core Mechanics — {title}\n\n"
        f"_Auto-generated from d20pfsrd by `dnd/tools/dump_rules.py`._\n"
        f"_Do not edit by hand — re-run the script to refresh._\n\n"
        f"**Source:** [{url}]({url})\n\n"
        f"---\n\n"
    )


def _process(slug: str, url: str, title: str, out_dir: Path) -> None:
    print(f"  fetching {url}", file=sys.stderr)
    html = _fetch(url)
    body = _extract_article(html)
    if body is None:
        print(f"  ! no <article> on {url} — skipping", file=sys.stderr)
        return
    body = _strip_noise(body)
    md = _convert(body)
    out = out_dir / f"{slug}.md"
    out.write_text(_banner(title, url) + md, encoding="utf-8")
    print(f"  wrote {out} ({len(md):,} chars)", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path,
                    default=Path("dnd/checklist/rules"),
                    help="output directory (default dnd/checklist/rules)")
    ap.add_argument("--only", nargs="+", default=None,
                    help="restrict to these slugs (default: all)")
    ap.add_argument("--delay", type=float, default=1.5,
                    help="seconds to wait between requests (default 1.5)")
    args = ap.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)

    pages = PAGES
    if args.only:
        wanted = set(args.only)
        pages = [p for p in PAGES if p[0] in wanted]
        missing = wanted - {p[0] for p in pages}
        if missing:
            print(f"unknown slugs: {sorted(missing)}", file=sys.stderr)
            return 2

    for i, (slug, url, title) in enumerate(pages):
        if i:
            time.sleep(args.delay)
        try:
            _process(slug, url, title, args.out)
        except Exception as exc:  # noqa: BLE001 — best-effort tool
            print(f"  ! {slug}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
