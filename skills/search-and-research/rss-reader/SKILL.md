---
name: rss-reader
description: Read and parse RSS/Atom feeds to monitor news, blogs, and content updates. Use when you need to fetch RSS feeds, parse entries, or monitor content sources for updates.
---

# RSS Reader

Fetch, parse, and process RSS/Atom feeds to monitor content sources and extract updates.

## When to Use

- Monitoring news feeds for specific topics
- Tracking blog updates from multiple sources
- Aggregating content from various RSS sources
- Extracting structured data from feed entries

## Feed Fetching

### Using the Script

```bash
python scripts/fetch_rss.py <feed_url> [--limit N] [--format json|text]
```

**Arguments:**
- `feed_url`: The RSS/Atom feed URL to fetch
- `--limit N`: Number of entries to return (default: 10)
- `--format`: Output format - `json` or `text` (default: text)

**Examples:**
```bash
# Fetch latest 5 entries as text
python scripts/fetch_rss.py https://example.com/feed.xml --limit 5

# Fetch as JSON for processing
python scripts/fetch_rss.py https://example.com/rss --format json
```

## Feed Entry Structure

Each feed entry typically contains:
- **title**: Entry headline
- **link**: URL to full content
- **published**: Publication date
- **summary**: Brief description or excerpt
- **author**: Content author (if available)

## Common RSS Sources

| Type | Example Feed Pattern |
|------|---------------------|
| Blogs | `/feed`, `/rss`, `/atom.xml` |
| News | `/rss/headlines`, `/feeds/all` |
| GitHub | `/releases.atom`, `/commits.atom` |
| Reddit | `/.rss`, `/top/.rss` |

## Processing Guidelines

1. **Check feed validity**: Ensure URL returns valid XML
2. **Handle encoding**: Most feeds use UTF-8
3. **Parse dates**: Use ISO 8601 format when available
4. **Respect rate limits**: Cache results when possible
5. **Handle errors gracefully**: Some feeds may be temporarily unavailable
