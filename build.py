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


def render_md(body: str) -> str:
    ensure_markdown()
    return md_lib.markdown(body, extensions=["tables", "fenced_code", "nl2br"])


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
    )
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
