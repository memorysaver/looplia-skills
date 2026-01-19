# Multi-Source Research

Patterns for comparing and cross-referencing information across multiple websites.

Normalize terms and units (dates, currencies, measurements) before comparing values.

## Scenario Recipes

### Cross-site consensus check

Intent: Compare a single data point across three sources.

Steps:
1. Open each source in a separate session and snapshot the target area.
2. Extract the same field from each site and normalize units.
3. Record agreement or conflict and note missing fields.

Output:
```json
{
  "topic": "Example data point",
  "values": {
    "source_a": "Value A",
    "source_b": "Value B",
    "source_c": "Value C"
  },
  "consensus": "agreed | conflicting | partial",
  "accessed": {
    "source_a": "2025-01-19",
    "source_b": "2025-01-19",
    "source_c": "2025-01-19"
  }
}
```

### Price or spec comparison

Intent: Compare structured specs or pricing across vendors.

Steps:
1. Extract the same fields per vendor (price, tier, limits).
2. Normalize currency, units, and ranges.
3. Flag missing data and conflicting values.

Output:
```json
{
  "product": "Example product",
  "fields": ["price", "storage"],
  "vendors": {
    "vendor_a": {"price": "$99", "storage": "100GB"},
    "vendor_b": {"price": "$89", "storage": "1TB"}
  },
  "notes": "Vendor B uses annual pricing",
  "accessed": {
    "vendor_a": "2025-01-19",
    "vendor_b": "2025-01-19"
  }
}
```

### Recency validation

Intent: Resolve conflicts by favoring the most recent primary source.

Steps:
1. Capture last updated dates from each source.
2. Prefer primary sources when timestamps are close.
3. Document the decision rationale.

Output:
```json
{
  "finding": "Example claim",
  "sources": {
    "official": {"value": "X", "updated": "2025-01-18"},
    "secondary": {"value": "Y", "updated": "2024-12-01"}
  },
  "resolution": "Used official source due to newer update",
  "confidence": "high"
}
```

## Parallel Sessions

Use named sessions to maintain separate browser contexts:

```bash
# Open three sources simultaneously
agent-browser --session site1 open "https://source-a.com/topic"
agent-browser --session site2 open "https://source-b.com/topic"
agent-browser --session site3 open "https://source-c.com/topic"

# Work with each independently
agent-browser --session site1 snapshot -i
agent-browser --session site2 snapshot -i
agent-browser --session site3 snapshot -i

# Each session maintains its own:
# - Cookies and authentication
# - Navigation history
# - Page state
```

## Comparison Research Pattern

### Step 1: Identify Sources

```bash
# Start with search to find relevant sources
agent-browser open "https://www.google.com"
agent-browser snapshot -i
agent-browser fill @e1 "topic comparison review"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i
# Note URLs of top 3-5 relevant results
# Prefer primary sources; skip ads and thin aggregators
```

### Step 2: Extract from Each

```bash
# Source A
agent-browser --session a open "https://source-a.com"
agent-browser --session a snapshot -i
agent-browser --session a get text @e15    # Key data point

# Source B
agent-browser --session b open "https://source-b.com"
agent-browser --session b snapshot -i
agent-browser --session b get text @e20    # Same data point
```

### Step 3: Cross-Reference

Structure findings to highlight agreement/disagreement:

```json
{
  "topic": "Research question",
  "findings": {
    "data_point_1": {
      "source_a": "Value from A",
      "source_b": "Value from B",
      "source_c": "Value from C",
      "consensus": "agreed | conflicting | partial"
    }
  }
}
```

## Handling Conflicting Information

When sources disagree:

1. **Note the discrepancy** - Don't silently pick one
2. **Check source authority** - Is one more authoritative?
3. **Check recency** - Is one more recent?
4. **Find additional sources** - Break the tie
5. **Record access date** - Capture timestamps per source

```json
{
  "finding": "Product X price",
  "values": {
    "official_site": "$99",
    "retailer_a": "$89",
    "retailer_b": "$95"
  },
  "accessed": {
    "official_site": "2025-01-19",
    "retailer_a": "2025-01-19",
    "retailer_b": "2025-01-19"
  },
  "resolution": "Official price is $99; retailers offer discounts",
  "confidence": "high"
}
```

## Source Attribution

Always track where information came from:

```json
{
  "claim": "Specific fact or data point",
  "sources": [
    {
      "url": "https://source-a.com/page",
      "title": "Page Title",
      "accessed": "2025-01-19",
      "quote": "Exact text supporting claim"
    }
  ]
}
```

## Session Management

```bash
# List active sessions
agent-browser session list

# Clean up when done
agent-browser --session site1 close
agent-browser --session site2 close
```

## Best Practices

1. **Use consistent data points** - Extract the same fields from each source
2. **Note missing data** - Mark when a source doesn't have information
3. **Prioritize primary sources** - Official sites > aggregators > forums
4. **Check dates** - Note publication/update dates for each source
5. **Save evidence** - Screenshot key findings for reference (when available)
6. **Rank trust** - Add a simple authority score per source
