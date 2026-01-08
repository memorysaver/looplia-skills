#!/usr/bin/env python3
"""
Fetch and parse RSS/Atom feeds.

Usage:
    python fetch_rss.py <feed_url> [--limit N] [--format json|text]

Examples:
    python fetch_rss.py https://example.com/feed.xml
    python fetch_rss.py https://example.com/rss --limit 5 --format json
"""

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional
from urllib.error import HTTPError, URLError


def parse_date(date_str: Optional[str]) -> Optional[str]:
    """Parse various date formats to ISO 8601."""
    if not date_str:
        return None

    formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # RFC 822
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",        # ISO 8601
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.isoformat()
        except ValueError:
            continue

    return date_str


def get_text(element: Optional[ET.Element], default: str = "") -> str:
    """Safely extract text from an XML element."""
    if element is not None and element.text:
        return element.text.strip()
    return default


def parse_rss(root: ET.Element) -> list[dict]:
    """Parse RSS 2.0 format."""
    entries = []
    channel = root.find("channel")
    if channel is None:
        return entries

    for item in channel.findall("item"):
        entry = {
            "title": get_text(item.find("title")),
            "link": get_text(item.find("link")),
            "published": parse_date(get_text(item.find("pubDate"))),
            "summary": get_text(item.find("description")),
            "author": get_text(item.find("author")) or get_text(item.find("dc:creator")),
        }
        entries.append(entry)

    return entries


def parse_atom(root: ET.Element, ns: dict) -> list[dict]:
    """Parse Atom format."""
    entries = []

    for entry in root.findall("atom:entry", ns):
        link_elem = entry.find("atom:link[@rel='alternate']", ns)
        if link_elem is None:
            link_elem = entry.find("atom:link", ns)

        entry_data = {
            "title": get_text(entry.find("atom:title", ns)),
            "link": link_elem.get("href", "") if link_elem is not None else "",
            "published": parse_date(
                get_text(entry.find("atom:published", ns)) or
                get_text(entry.find("atom:updated", ns))
            ),
            "summary": get_text(entry.find("atom:summary", ns)) or
                       get_text(entry.find("atom:content", ns)),
            "author": get_text(entry.find("atom:author/atom:name", ns)),
        }
        entries.append(entry_data)

    return entries


def fetch_feed(url: str, limit: int = 10) -> list[dict]:
    """Fetch and parse an RSS/Atom feed."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; RSSReader/1.0)"
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode("utf-8")
    except HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code}: {e.reason}")
    except URLError as e:
        raise RuntimeError(f"URL error: {e.reason}")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch feed: {e}")

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        raise RuntimeError(f"Failed to parse XML: {e}")

    # Detect feed type and parse
    if root.tag == "rss":
        entries = parse_rss(root)
    elif root.tag == "{http://www.w3.org/2005/Atom}feed":
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = parse_atom(root, ns)
    elif root.tag == "feed":
        # Atom without namespace
        entries = []
        for entry in root.findall("entry"):
            link_elem = entry.find("link[@rel='alternate']")
            if link_elem is None:
                link_elem = entry.find("link")

            entry_data = {
                "title": get_text(entry.find("title")),
                "link": link_elem.get("href", "") if link_elem is not None else "",
                "published": parse_date(
                    get_text(entry.find("published")) or
                    get_text(entry.find("updated"))
                ),
                "summary": get_text(entry.find("summary")) or get_text(entry.find("content")),
                "author": get_text(entry.find("author/name")),
            }
            entries.append(entry_data)
    else:
        raise RuntimeError(f"Unknown feed format: {root.tag}")

    return entries[:limit]


def format_text(entries: list[dict]) -> str:
    """Format entries as readable text."""
    lines = []
    for i, entry in enumerate(entries, 1):
        lines.append(f"{i}. {entry['title']}")
        if entry['published']:
            lines.append(f"   Published: {entry['published']}")
        if entry['author']:
            lines.append(f"   Author: {entry['author']}")
        lines.append(f"   Link: {entry['link']}")
        if entry['summary']:
            summary = entry['summary'][:200]
            if len(entry['summary']) > 200:
                summary += "..."
            lines.append(f"   {summary}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and parse RSS/Atom feeds"
    )
    parser.add_argument("url", help="Feed URL to fetch")
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Number of entries to return (default: 10)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()

    try:
        entries = fetch_feed(args.url, args.limit)

        if args.format == "json":
            print(json.dumps(entries, indent=2, ensure_ascii=False))
        else:
            print(format_text(entries))

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
