"""Refreshes the live parts of README.md in place, between their HTML comment markers.

- facts: headline numbers from the site's own content (ShinyQ/ShinyQ-HQ main, content/site-content.json),
  the same source https://shinyq.my.id renders, so the README never drifts from the site
- writing: the latest posts from the site's Atom feed (https://shinyq.my.id/en/feed.xml)

Writes README.md only when a section changed and says so; the workflow commits only then.
Run: python3 scripts/refresh.py   (HQ_CONTENT and HQ_FEED read local files instead of the network)
"""
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from html import escape

from hq import ROOT, SITE

CONTENT = "https://raw.githubusercontent.com/ShinyQ/ShinyQ-HQ/main/content/site-content.json"
FEED = f"{SITE}/en/feed.xml"
FACTS = ["prs-merged-2026", "enterprise-clients", "competition-placings"]
POSTS = 2
ATOM = {"a": "http://www.w3.org/2005/Atom"}
README = ROOT / "README.md"


def fetch(url: str, env: str) -> bytes:
    if os.environ.get(env):
        with open(os.environ[env], "rb") as f:
            return f.read()
    req = urllib.request.Request(url, headers={"User-Agent": "ShinyQ-profile-refresh"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()


def facts() -> str:
    stats = {s["id"]: s for s in json.loads(fetch(CONTENT, "HQ_CONTENT"))["stats"]}
    parts = []
    for sid in FACTS:
        if sid not in stats:
            print(f"warning: stat {sid} is no longer in site-content.json; skipped")
            continue
        stat = stats[sid]
        label = stat.get("short", {}).get("en") or re.split(r"[,:(]", stat["label"]["en"])[0].strip()
        if label[1:2].islower():
            label = label[0].lower() + label[1:]
        parts.append(f"`{stat['value']}` {label}")
    if not parts:
        raise SystemExit("no headline stats found; check FACTS against site-content.json")
    return "&nbsp;· ".join(parts)


def writing() -> str:
    feed = ET.fromstring(fetch(FEED, "HQ_FEED"))
    entries = sorted(feed.findall("a:entry", ATOM), key=lambda e: e.findtext("a:published", "", ATOM), reverse=True)
    links = []
    for entry in entries[:POSTS]:
        href = entry.find("a:link[@rel='alternate']", ATOM).get("href")
        title = entry.findtext("a:title", "", ATOM).strip()
        links.append(f'<a href="{escape(href)}?view=classic">{escape(title, quote=False)}</a>')
    if not links:
        raise SystemExit("the feed has no entries")
    more = f'<a href="{SITE}/en/library?view=classic">All writing →</a>'
    return f'<p align="center"><sub><b>Latest writing</b> &nbsp;·&nbsp; {" &nbsp;·&nbsp; ".join(links)} &nbsp;·&nbsp; {more}</sub></p>'


def replace(doc: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {name}:start -->\n).*?(\n<!-- {name}:end -->)", re.S)
    if not pattern.search(doc):
        raise SystemExit(f"README.md has no {name} markers")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), doc)


if __name__ == "__main__":
    before = README.read_text()
    after = replace(replace(before, "facts", facts()), "writing", writing())
    if after == before:
        print("README.md unchanged")
    else:
        README.write_text(after)
        print("README.md refreshed")
