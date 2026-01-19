---
name: browser-research
description: |
  This skill should be used when the user needs to perform deep web research
  across multiple websites, extract data from JavaScript-rendered or dynamic pages,
  navigate through search results or paginated content, or build comprehensive
  research reports from multiple sources.

  Use this skill when the user says: "research this topic across sites",
  "scrape this website", "extract data from this page", "compare prices",
  "browse and extract information", "fill forms and get results",
  "navigate through pages", "click through search results",
  "research authenticated content", or "cross-reference multiple sources".

  Prefer this over WebFetch when pages require JavaScript, interaction,
  authentication, or multi-step navigation.
allowed-tools: Bash(agent-browser:*)
---

# Browser Research

Execute deep web research missions using agent-browser for interactive page navigation and data extraction.

## When to Use

- **Multi-page research**: Navigating search results, following links, exploring sites
- **Dynamic content**: JavaScript-rendered pages, SPAs, interactive dashboards
- **Form interaction**: Filling search fields, applying filters, submitting queries
- **Data extraction**: Tables, lists, product information, structured data
- **Authenticated content**: Sites requiring login or session state

For simple static pages, consider `WebFetch` first. Escalate to agent-browser when content is incomplete or interaction is required.

## Core Research Loop

```
┌─────────────────────────────────────────────────────┐
│  1. OPEN     agent-browser open <url>               │
│  2. SNAPSHOT agent-browser snapshot -i              │
│  3. EXTRACT  agent-browser get text @ref            │
│  4. NAVIGATE agent-browser click @ref / fill / etc  │
│  5. REPEAT   Loop steps 2-4 until mission complete  │
└─────────────────────────────────────────────────────┘
```

### The Snapshot-Act Pattern

Always snapshot before interacting. Refs (`@e1`, `@e2`) are stable identifiers for elements:

```bash
agent-browser open "https://example.com/search"
agent-browser snapshot -i                    # See what's available
agent-browser fill @e3 "search query"        # Fill the search box
agent-browser click @e5                      # Click search button
agent-browser wait --load networkidle        # Wait for results
agent-browser snapshot -i                    # See new state
```

## Research Planning

Before starting, define:

| Aspect | Question | Example |
|--------|----------|---------|
| **Mission** | What information do you need? | "Find pricing for top 3 CRM tools" |
| **Sources** | Which sites to visit? | Specific URLs or search-discovered |
| **Extraction** | What data points to capture? | Price, features, limits |
| **Depth** | How many pages/levels? | First 10 results, 2 levels deep |

### Source Discovery

Start broad, then narrow:

```bash
# Option 1: Direct navigation (when you know the site)
agent-browser open "https://known-site.com/pricing"

# Option 2: Search engine discovery
agent-browser open "https://www.google.com"
agent-browser snapshot -i
agent-browser fill @e1 "CRM pricing comparison 2025"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i
# Extract relevant URLs from results
```

## Scenario Recipes

Use recipes when you need a repeatable pattern. Each recipe should include:

1. **Intent** - The question being answered and the expected output shape
2. **Minimal Steps** - 3-6 steps with snapshots, verification, and stop conditions
3. **Output** - JSON fields with sources, access dates, and missing-data notes

### Extraction

- [Data Extraction Patterns](references/data-extraction.md) - Feed top-N, paginated catalog, filtered results

### Comparison

- [Multi-Source Research](references/multi-source.md) - Consensus checks, price/spec comparisons, recency validation

### Exploration

- [Site Exploration](references/site-exploration.md) - Docs crawl, category discovery, auth-gated inventory

## Data Extraction Strategies

### Extract Text Content

```bash
# Single element
agent-browser get text @e15

# Multiple elements - snapshot shows structure
agent-browser snapshot -s ".results"         # Scope to results section
agent-browser get text @e20                  # First result
agent-browser get text @e25                  # Second result
```

### Handle Pagination

```bash
# Pattern: Extract current page, navigate to next, repeat
agent-browser snapshot -i
# ... extract data from current page ...
agent-browser click @e99                     # "Next" button
agent-browser wait --load networkidle
agent-browser snapshot -i                    # New page content
```

### Handle Lazy Loading

```bash
agent-browser scroll down 1000
agent-browser wait 1000                      # Allow content to load
agent-browser snapshot -i                    # See newly loaded content
```

## Output Format

Structure your research results for clarity:

```json
{
  "mission": "Original research question",
  "sources": [
    {
      "url": "https://example.com/page",
      "title": "Page Title",
      "accessed": "2025-01-19",
      "data": {
        "key_finding_1": "value",
        "key_finding_2": "value"
      }
    }
  ],
  "summary": "Key findings in 2-3 sentences",
  "limitations": "Any access issues or incomplete data"
}
```

Always include:
- **Source URLs** for attribution
- **Access timestamps** for currency
- **Limitations** for transparency

## Sessions for Parallel Research

Use named sessions to research multiple sources simultaneously:

```bash
# Research source A
agent-browser --session src-a open "https://site-a.com"
agent-browser --session src-a snapshot -i

# Research source B (parallel)
agent-browser --session src-b open "https://site-b.com"
agent-browser --session src-b snapshot -i

# Continue working in each session
agent-browser --session src-a click @e5
agent-browser --session src-b fill @e3 "query"
```

## Quick Reference

For complete command documentation, see: **agent-browser** skill

| Task | Command |
|------|---------|
| Navigate | `open`, `back`, `forward`, `reload`, `close` |
| Analyze | `snapshot -i`, `get text/html/value/url/title` |
| Interact | `click`, `fill`, `press`, `select`, `find` |
| Wait | `wait --load`, `wait <selector>`, `wait <ms>` |
| State | `is visible`, `is enabled`, `state save/load` |
| Capture | `screenshot`, `pdf`, `--json` |

## See Also

- [Data Extraction Patterns](references/data-extraction.md) - Tables, lists, structured data
- [Multi-Source Research](references/multi-source.md) - Comparing across sites
- [Site Exploration](references/site-exploration.md) - Deep-diving single domains

## Handling Failures

Research automation can fail. Handle common issues:

```bash
# Check if element exists before interacting
agent-browser is visible @e50
# If false, the page structure may have changed - re-snapshot

# Timeout waiting for content
agent-browser wait --load networkidle
# If this times out, content may require scrolling or interaction

# Element not found - try semantic locators
agent-browser find text "Submit" click
# More resilient than refs when DOM structure changes

# Network errors - check page loaded
agent-browser get url
# Verify you're on the expected page before extracting
```

When failures occur:
- **Re-snapshot** - DOM may have changed
- **Try `find` locators** - More stable than refs for dynamic content
- **Check URL** - Redirects or errors may have changed the page
- **Report limitations** - Note access issues in output, don't silently skip

## Best Practices

1. **Snapshot frequently** - DOM changes after interactions
2. **Use `-i` flag** - Interactive elements only, cleaner output
3. **Wait after navigation** - `--load networkidle` ensures content is ready
4. **Scope when needed** - `-s ".container"` focuses on relevant sections
5. **Track sources** - Use `get url` and `get title` for attribution
6. **Handle failures** - Report access issues, don't silently skip
7. **Use `find` for dynamic content** - When refs change, semantic locators are more stable
8. **Close when done** - `agent-browser close` releases resources
