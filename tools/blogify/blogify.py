#!/usr/bin/env python3
"""blogify — turn a Markdown document into a blog-post HTML fragment.

Renders a Markdown file into a self-contained, semantic ``<article>`` fragment
you can paste straight into an existing template or CMS. Post metadata is
auto-derived: the title comes from the first level-1 heading, the date is
today, and the slug is built from the filename. A reading-time estimate is
computed from the word count.

Usage:
    python blogify.py post.md                 # print fragment to stdout
    python blogify.py post.md -o post.html    # write fragment to a file
    python blogify.py post.md --author "Ada"  # add a byline

Requires the ``markdown`` package:
    pip install markdown
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
import sys
from pathlib import Path

try:
    import markdown as _markdown
except ImportError:  # pragma: no cover - dependency hint
    sys.exit(
        "The 'markdown' package is required. Install it with:\n"
        "    pip install markdown"
    )


WORDS_PER_MINUTE = 200

# Extensions that make the output blog-friendly: tables, fenced code blocks,
# footnotes, definition lists, and heading anchors.
_MD_EXTENSIONS = [
    "extra",
    "sane_lists",
    "smarty",
    "toc",
    "codehilite",
]
_MD_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False},
    "toc": {"anchorlink": True},
}


def slugify(text: str) -> str:
    """Turn arbitrary text into a URL-friendly slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-") or "post"


def extract_title(md_text: str) -> str | None:
    """Return the first level-1 heading (ATX ``# `` or Setext ``===``)."""
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        atx = re.match(r"^\#\s+(.*\S)\s*$", line)
        if atx:
            return atx.group(1).strip()
        # Setext: a line of text underlined by one or more '='.
        if line.strip() and i + 1 < len(lines) and re.match(r"^=+\s*$", lines[i + 1]):
            return line.strip()
    return None


def strip_leading_h1(md_text: str) -> str:
    """Remove the first H1 so it isn't rendered twice inside the body."""
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\#\s+.*\S\s*$", line):
            del lines[i]
            return "\n".join(lines)
        if line.strip() and i + 1 < len(lines) and re.match(r"^=+\s*$", lines[i + 1]):
            del lines[i : i + 2]
            return "\n".join(lines)
    return md_text


def reading_time(md_text: str) -> int:
    """Estimate reading time in minutes (minimum 1)."""
    words = len(re.findall(r"\b\w+\b", md_text))
    return max(1, round(words / WORDS_PER_MINUTE))


def render_fragment(
    md_text: str,
    *,
    title: str,
    slug: str,
    date: _dt.date,
    author: str | None = None,
    minutes: int,
) -> str:
    """Build the ``<article>`` HTML fragment."""
    body_source = strip_leading_h1(md_text)
    md = _markdown.Markdown(
        extensions=_MD_EXTENSIONS, extension_configs=_MD_EXTENSION_CONFIGS
    )
    body_html = md.convert(body_source)

    iso_date = date.isoformat()
    human_date = date.strftime("%B %-d, %Y") if sys.platform != "win32" else date.strftime("%B %#d, %Y")

    meta_bits = [
        f'<time datetime="{iso_date}">{html.escape(human_date)}</time>',
        f"<span class=\"reading-time\">{minutes} min read</span>",
    ]
    if author:
        meta_bits.insert(0, f'<span class="author">{html.escape(author)}</span>')
    meta = '\n      <span class="sep">·</span>\n      '.join(meta_bits)

    return (
        f'<article class="blog-post" data-slug="{html.escape(slug)}">\n'
        f"  <header class=\"post-header\">\n"
        f"    <h1 class=\"post-title\">{html.escape(title)}</h1>\n"
        f'    <p class="post-meta">\n      {meta}\n    </p>\n'
        f"  </header>\n"
        f'  <div class="post-body">\n{body_html}\n  </div>\n'
        f"</article>\n"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a blog-post HTML fragment from a Markdown file."
    )
    parser.add_argument("source", type=Path, help="Path to the Markdown file.")
    parser.add_argument(
        "-o", "--output", type=Path, help="Write to this file instead of stdout."
    )
    parser.add_argument("--title", help="Override the auto-derived title.")
    parser.add_argument("--slug", help="Override the auto-derived slug.")
    parser.add_argument(
        "--date",
        help="Override the date (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument("--author", help="Optional author byline.")
    return parser


def main(argv: list[str] | None = None) -> int:
    # Ensure UTF-8 output regardless of the platform's console codepage.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = build_parser().parse_args(argv)

    if not args.source.is_file():
        sys.exit(f"No such file: {args.source}")

    md_text = args.source.read_text(encoding="utf-8")

    title = args.title or extract_title(md_text) or args.source.stem.replace("-", " ").title()
    slug = args.slug or slugify(args.source.stem)

    if args.date:
        try:
            date = _dt.date.fromisoformat(args.date)
        except ValueError:
            sys.exit(f"Invalid --date '{args.date}'; expected YYYY-MM-DD.")
    else:
        date = _dt.date.today()

    fragment = render_fragment(
        md_text,
        title=title,
        slug=slug,
        date=date,
        author=args.author,
        minutes=reading_time(md_text),
    )

    if args.output:
        args.output.write_text(fragment, encoding="utf-8")
        print(f"Wrote {args.output} ({slug})", file=sys.stderr)
    else:
        sys.stdout.write(fragment)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

