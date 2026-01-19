# Data Extraction Patterns

Patterns for extracting structured data from web pages using agent-browser.

Prefer scoped snapshots (`-s`) on large pages; use full snapshots (`-i`) when mapping overall structure.

## Scenario Recipes

### Top N items from a feed

Intent: Collect the first N feed items matching keywords.

Steps:
1. Open the feed and snapshot the list container.
2. Verify the list container is visible, then extract title, link, and time for visible items.
3. Continue until N matching items are collected; stop when no new items appear.

Output:
```json
{
  "source_url": "https://example.com/feed",
  "keywords": ["ai", "ml"],
  "items": [
    {
      "title": "Example title",
      "url": "https://example.com/item",
      "time": "2025-01-19"
    }
  ],
  "total_matched": 3
}
```

### Paginated catalog export

Intent: Export all items across a paginated catalog.

Steps:
1. Snapshot the catalog container and extract visible items.
2. Check for the next page button and click it when enabled.
3. Repeat until the next button is missing or disabled.

Output:
```json
{
  "source_url": "https://example.com/catalog",
  "items": [
    {
      "name": "Item A",
      "price": "$99"
    }
  ],
  "pages_scraped": 3,
  "total_items": 120
}
```

### Filtered results via form

Intent: Submit filters and capture the resulting list.

Steps:
1. Fill in the query and select filters.
2. Submit the form and wait for network idle.
3. Snapshot the results container and extract matching fields.

Output:
```json
{
  "source_url": "https://example.com/search",
  "query": "example",
  "filters": {
    "category": "news"
  },
  "results": [
    {
      "title": "Result A",
      "url": "https://example.com/result"
    }
  ]
}
```

## Tables

Tables often contain valuable structured data. Extract systematically:

```bash
# 1. Scope to the table
agent-browser snapshot -s "table" -i

# 2. Identify structure from snapshot
# Look for: thead, tbody, tr, th, td elements with refs

# 3. Verify header row exists
agent-browser is visible @e10

# 4. Extract header row
agent-browser get text @e10                  # First header cell
agent-browser get text @e11                  # Second header cell

# 5. Extract data rows
agent-browser get text @e20                  # Row 1, Cell 1
agent-browser get text @e21                  # Row 1, Cell 2
```

### Large Tables with Pagination

```bash
# Loop pattern for paginated tables
agent-browser snapshot -s "table"
# Extract current page data...

# Check for next page
agent-browser is visible @e99                # "Next" button
agent-browser click @e99
agent-browser wait --load networkidle
agent-browser snapshot -s "table"
# Repeat extraction until next is missing or disabled
```

## Lists

Product listings, search results, article feeds:

```bash
# 1. Scope to list container
agent-browser snapshot -s ".results-list" -i

# 2. Verify list container exists
agent-browser is visible @e10

# 3. Each item typically has consistent structure
# Look for repeating patterns in refs

# 4. Extract key fields per item
agent-browser get text @e30                  # Title
agent-browser get text @e31                  # Description
agent-browser get attr @e32 href             # Link
```

### Infinite Scroll Lists

```bash
# Scroll-and-extract pattern
agent-browser snapshot -i
# Extract visible items...

agent-browser scroll down 1000
agent-browser wait 1500                      # Allow lazy load
agent-browser snapshot -i
# Extract newly loaded items...

# Repeat until no new content appears
```

## Forms with Dynamic Data

Some data appears only after form interaction:

```bash
# 1. Fill form to reveal data
agent-browser fill @e5 "search term"
agent-browser select @e6 "category"
agent-browser click @e7                      # Submit/Apply
agent-browser wait --load networkidle

# 2. Extract revealed data
agent-browser snapshot -i
agent-browser get text @e20
```

## Structured Data Extraction

### JSON in Page

Some pages embed JSON data in page globals or JSON-LD:

```bash
agent-browser eval "JSON.stringify(window.__DATA__)"
agent-browser eval "JSON.stringify(window.__NEXT_DATA__)"
```

### Data Attributes

Extract from HTML attributes:

```bash
agent-browser get attr @e15 data-price
agent-browser get attr @e15 data-id
agent-browser get attr @e15 data-category
```

### JSON Output Flag

For machine-readable extraction, add `--json`:

```bash
agent-browser snapshot -i --json        # Structured element data
agent-browser get text @e15 --json      # Structured text response
```

## Handling Missing Data

Always check before extracting:

```bash
# Check element exists
agent-browser is visible @e50

# Conditional extraction
# If not visible, record "Not found" in your output
```

## Output Structure

Organize extracted data consistently:

```json
{
  "source_url": "https://example.com/products",
  "extraction_date": "2025-01-19",
  "data": [
    {
      "name": "Product A",
      "price": "$99",
      "description": "..."
    }
  ],
  "total_items": 25,
  "pages_scraped": 3
}
```
