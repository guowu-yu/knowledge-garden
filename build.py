#!/usr/bin/env python3
"""Build 凌云知境 static site from Markdown topics."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "topics"
SRC = ROOT / "src"
DIST = ROOT / "dist"

try:
    import markdown as md_lib
except ImportError:
    md_lib = None


def ensure_markdown():
    global md_lib
    if md_lib is not None:
        return
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q"])
    import markdown as md_lib  # noqa: F401


def escape_html(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_front_matter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    yaml = raw[3:end].strip()
    body = raw[end + 4 :].lstrip()
    meta: dict = {}
    for line in yaml.splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            meta[key] = [
                p.strip().strip("\"'")
                for p in inner.split(",")
                if p.strip()
            ]
        else:
            meta[key] = value.strip("\"'")
    return meta, body


def plain_text(md: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", md)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"[#>*_\-|]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


_MATH_DISPLAY = re.compile(r"\\\[((?:.|\n)*?)\\\]")
_MATH_INLINE = re.compile(r"\\\(((?:.|\n)*?)\\\)")
_MATH_DOLLAR = re.compile(r"\$\$((?:.|\n)*?)\$\$")


def _extract_math(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Pull LaTeX out before Markdown so \\(, \\[, \\{ etc. are not escaped."""
    slots: list[tuple[str, str]] = []

    def park(kind: str, tex: str) -> str:
        slots.append((kind, tex))
        return f"@@MATH{len(slots) - 1}@@"

    def park_display(m: re.Match) -> str:
        return park("display", m.group(1))

    def park_inline(m: re.Match) -> str:
        return park("inline", m.group(1))

    body = _MATH_DOLLAR.sub(park_display, body)
    body = _MATH_DISPLAY.sub(park_display, body)
    body = _MATH_INLINE.sub(park_inline, body)
    return body, slots


def _restore_math(html: str, slots: list[tuple[str, str]]) -> str:
    for i, (kind, tex) in enumerate(slots):
        token = f"@@MATH{i}@@"
        if kind == "display":
            repl = f"\\[{tex}\\]"
        else:
            repl = f"\\({tex}\\)"
        html = html.replace(token, repl)
        # Prefer bare display math over a wrapping paragraph
        html = html.replace(f"<p>\\[{tex}\\]</p>", f"\\[{tex}\\]")
        html = html.replace(f"<p>\\[{tex}\\]<br />\n</p>", f"\\[{tex}\\]")
    return html


def render_md(body: str) -> str:
    ensure_markdown()
    body, math_slots = _extract_math(body)
    html = md_lib.markdown(body, extensions=["tables", "fenced_code", "nl2br"])
    html = _restore_math(html, math_slots)
    # Allow MD preview paths from content/topics → src/assets, then rewrite for dist/topics
    html = html.replace("../../src/assets/", "../assets/")
    html = html.replace("../src/assets/", "../assets/")
    return html


def render_tags(tags: list[str]) -> str:
    return "".join(f'<span class="tag">{escape_html(t)}</span>' for t in tags)


def topic_card(topic: dict, href_prefix: str = "topics/") -> str:
    if topic["cover"]:
        cover = (
            f'<div class="card-cover" style="background-image:url(\'{escape_html(topic["cover"])}\')"></div>'
        )
    else:
        cover = '<div class="card-cover card-cover--fallback"></div>'
    slug = sanitize_slug(topic["slug"])
    return f"""
    <a class="topic-card" href="{href_prefix}{escape_html(slug)}.html" data-title="{escape_html(topic['title'])}" data-tags="{escape_html(' '.join(topic['tags']))}" data-summary="{escape_html(topic['summary'])}">
      {cover}
      <div class="card-body">
        <div class="card-meta">
          <time datetime="{escape_html(topic['date'])}">{escape_html(topic['date'])}</time>
          <div class="tags">{render_tags(topic['tags'])}</div>
        </div>
        <h3>{escape_html(topic['title'])}</h3>
        <p>{escape_html(topic['summary'])}</p>
      </div>
    </a>"""


def sanitize_slug(slug: str) -> str:
    slug = slug.strip().replace(" ", "-")
    slug = re.sub(r"[^\w\-.\u4e00-\u9fff]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "topic"


# NTN 学习路线的 20 个专题（按建议学习顺序排列）
NTN_ROADMAP_ORDER = [
    "5g-ntn",
    "ntn-regenerative-payload",
    "ntn-ue-capability",
    "ntn-sib19",
    "ntn-rach",
    "ntn-doppler",
    "ntn-harq",
    "ntn-timers",
    "ntn-mobility",
    "ntn-power",
    "ntn-rlm-bfm",
    "ntn-measurement-csi",
    "ntn-channel-link-budget",
    "ntn-rel18-enhancements",
    "ntn-orbit-architecture",
    "ntn-rf-bands-coexistence",
    "ntn-iot",
    "ntn-rel19-future",
    "ntn-tn-ntn-interworking",
    "ntn-idle-inactive",
]


def roadmap_items(topics: list[dict]) -> str:
    """生成悬窗里的 20 条 NTN 专题导航项（按学习顺序）。"""
    by_slug = {t["slug"]: t for t in topics}
    rows = []
    for i, slug in enumerate(NTN_ROADMAP_ORDER, 1):
        topic = by_slug.get(slug)
        if not topic:
            continue
        title = topic["title"]
        # 去掉副标题，只留主标题，避免悬窗文字过长
        short = re.split(r"[:：]", title, maxsplit=1)[0].strip()
        rows.append(
            f'<a class="roadmap-item" href="topics/{escape_html(slug)}.html" '
            f'data-title="{escape_html(title)}" title="{escape_html(title)}">'
            f'<span class="roadmap-index">{i:02d}</span>'
            f'<span class="roadmap-label">{escape_html(short)}</span>'
            f"</a>"
        )
    return "\n".join(rows)


def roadmap_float(topics: list[dict], href_prefix: str = "topics/") -> str:
    """生成「5G NTN 专题学习路线图」飘动悬窗的 HTML。

    href_prefix：首页用 "topics/"，专题页（位于 dist/topics/）用 "../topics/"。
    """
    items = roadmap_items(topics).replace('href="topics/', f'href="{href_prefix}')
    return f"""
    <div class="roadmap-float" id="roadmap-float">
      <button
        type="button"
        class="roadmap-toggle"
        id="roadmap-toggle"
        aria-expanded="false"
        aria-controls="roadmap-panel"
      >
        <span class="roadmap-toggle-dot" aria-hidden="true"></span>
        <span class="roadmap-toggle-text">5G NTN 专题学习路线图</span>
        <span class="roadmap-toggle-count">20</span>
        <span class="roadmap-chevron" aria-hidden="true"></span>
      </button>
      <div class="roadmap-panel" id="roadmap-panel" role="menu" aria-label="5G NTN 专题学习路线图">
        <p class="roadmap-hint">点击任一项，开始学习该专题</p>
        <div class="roadmap-list">
          {items}
        </div>
      </div>
    </div>"""


def load_topics() -> list[dict]:
    if not CONTENT.exists():
        return []
    topics = []
    for path in CONTENT.glob("*.md"):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(raw)
        slug = sanitize_slug(meta.get("slug") or path.stem)
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        text = plain_text(body)
        summary = meta.get("summary") or text[:120]
        topics.append(
            {
                "slug": slug,
                "title": meta.get("title") or slug,
                "date": meta.get("date") or "",
                "tags": tags,
                "summary": summary,
                "cover": meta.get("cover") or "",
                "body": body,
                "html": render_md(body),
                "text": text,
            }
        )
    topics.sort(key=lambda t: t["date"], reverse=True)
    return topics


def copy_assets():
    src_assets = SRC / "assets"
    dest_assets = DIST / "assets"
    if dest_assets.exists():
        shutil.rmtree(dest_assets)
    shutil.copytree(src_assets, dest_assets)


def build() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "topics").mkdir(parents=True, exist_ok=True)
    copy_assets()

    topics = load_topics()
    index_tpl = (SRC / "index.html").read_text(encoding="utf-8")
    topic_tpl = (SRC / "topic.html").read_text(encoding="utf-8")

    cards = "\n".join(topic_card(t) for t in topics) or (
        '<p class="empty">暂无专题，在 <code>content/topics/</code> 添加 Markdown 即可。</p>'
    )
    index_html = index_tpl.replace("{{TOPIC_COUNT}}", str(len(topics))).replace(
        "{{TOPIC_CARDS}}", cards
    ).replace("{{NTN_ROADMAP_FLOAT}}", roadmap_float(topics, href_prefix="topics/"))
    (DIST / "index.html").write_text(index_html, encoding="utf-8")

    for topic in topics:
        related = [
            t
            for t in topics
            if t["slug"] != topic["slug"]
            and set(t["tags"]).intersection(topic["tags"])
        ][:3]
        related_html = ""
        if related:
            related_html = (
                '<section class="related"><h2>相关专题</h2>'
                f'<div class="related-grid">{"".join(topic_card(t, href_prefix="") for t in related)}</div>'
                "</section>"
            )

        cover_block = (
            f'<div class="topic-hero-media" style="background-image:url(\'{escape_html(topic["cover"])}\')"></div>'
            if topic["cover"]
            else '<div class="topic-hero-media topic-hero-media--fallback"></div>'
        )

        html = topic_tpl
        replacements = {
            "{{TITLE}}": escape_html(topic["title"]),
            "{{DATE}}": escape_html(topic["date"]),
            "{{TAGS}}": render_tags(topic["tags"]),
            "{{SUMMARY}}": escape_html(topic["summary"]),
            "{{COVER}}": escape_html(topic["cover"]),
            "{{COVER_BLOCK}}": cover_block,
            "{{CONTENT}}": topic["html"],
            "{{RELATED}}": related_html,
            "{{NTN_ROADMAP_FLOAT}}": roadmap_float(topics, href_prefix="../topics/"),
        }
        for k, v in replacements.items():
            html = html.replace(k, v)
        (DIST / "topics" / f"{topic['slug']}.html").write_text(html, encoding="utf-8")

    search_index = [
        {
            "slug": t["slug"],
            "title": t["title"],
            "date": t["date"],
            "tags": t["tags"],
            "summary": t["summary"],
            "text": t["text"][:4000],
            "url": f"topics/{t['slug']}.html",
        }
        for t in topics
    ]
    (DIST / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Built {len(topics)} topics → dist/")


if __name__ == "__main__":
    build()
