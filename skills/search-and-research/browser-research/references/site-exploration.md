# Site Exploration

Patterns for deep-diving into a single domain to understand its structure and find specific content.

## Site Mapping

Understand what's available before extracting:

```bash
# 1. Start at homepage or main section
agent-browser open "https://example.com"
agent-browser snapshot -i

# 2. Identify navigation structure
# Look for: nav, menu, sidebar elements with refs

# 3. Map main sections
agent-browser get text @e5                   # Nav item 1
agent-browser get attr @e5 href              # Link URL
agent-browser get text @e6                   # Nav item 2
agent-browser get attr @e6 href              # Link URL

# 4. Note URL patterns early
# Example: /docs/{category}/{page} or /products/{id}
```

## Following Internal Links

Systematic exploration of site sections:

```bash
# 1. Start at section index
agent-browser open "https://example.com/docs"
agent-browser snapshot -i

# 2. Get list of pages in section
# Extract all links in content area
# Track visited URLs to avoid loops

# 3. Visit each page
agent-browser click @e20                     # First doc page
agent-browser wait --load networkidle
agent-browser snapshot -i
# Extract content...

agent-browser back                           # Return to index
agent-browser snapshot -i
agent-browser click @e21                     # Next doc page
```

## Finding Hidden Content

Content that's not immediately visible:

### Expand/Collapse Sections

```bash
agent-browser snapshot -i
agent-browser click @e30                     # "Show more" / accordion
agent-browser wait 500
agent-browser snapshot -i                    # Newly visible content
```

### Tab Panels

```bash
agent-browser snapshot -i
agent-browser click @e15                     # Tab 2
agent-browser wait 300
agent-browser snapshot -s "[role=tabpanel]"  # Active panel content
```

### Modal/Popup Content

```bash
agent-browser click @e25                     # "Details" button
agent-browser wait 500
agent-browser snapshot -s "[role=dialog]"    # Modal content
agent-browser press Escape                   # Close modal
```

### Iframes

Content inside iframes requires frame switching:

```bash
agent-browser frame "#content-frame"    # Switch to iframe
agent-browser snapshot -i               # Now see iframe content
agent-browser frame main                # Return to main document
```

### Dialogs

Alert/confirm/prompt dialogs block automation. Handle them:

```bash
# If a dialog appears unexpectedly
agent-browser dialog accept             # Accept and continue
agent-browser dialog dismiss            # Or dismiss it
```

## Site Search

Use the site's own search for targeted finding:

```bash
# 1. Find search input
agent-browser snapshot -i
# Look for search box, often in header

# 2. Execute search
agent-browser fill @e3 "specific topic"
agent-browser press Enter
agent-browser wait --load networkidle

# 3. Parse results
agent-browser snapshot -s ".search-results"
```

## Authenticated Areas

For sites requiring login:

```bash
# 1. Login
agent-browser open "https://example.com/login"
agent-browser snapshot -i
agent-browser fill @e5 "username"
agent-browser fill @e6 "password"
agent-browser click @e7                      # Submit
agent-browser wait --url "**/dashboard"
# Avoid logging or storing credentials in notes

# 2. Save state for reuse
agent-browser state save example-auth.json

# 3. Later: restore session
agent-browser state load example-auth.json
agent-browser open "https://example.com/protected-page"
```

## Breadcrumb Navigation

Use breadcrumbs to understand hierarchy:

```bash
agent-browser snapshot -s ".breadcrumb"
# Reveals: Home > Category > Subcategory > Current Page
```

## Sitemap Discovery

Check for sitemap files:

```bash
agent-browser open "https://example.com/sitemap.xml"
agent-browser snapshot
# Or
agent-browser open "https://example.com/sitemap_index.xml"
agent-browser snapshot
# Or
agent-browser open "https://example.com/robots.txt"
agent-browser snapshot
# Look for Sitemap: directives
```

## Exploration Output

Document site structure as you explore:

```json
{
  "domain": "example.com",
  "explored": "2025-01-19",
  "structure": {
    "main_sections": ["Products", "Docs", "Blog", "Support"],
    "key_pages": [
      {
        "title": "Pricing",
        "url": "/pricing",
        "content_type": "pricing table"
      }
    ],
    "navigation": {
      "primary": "Top nav bar",
      "secondary": "Left sidebar in docs"
    }
  },
  "auth_required": ["Dashboard", "Account Settings"],
  "notes": "Blog has infinite scroll, docs are paginated"
}
```

## Best Practices

1. **Start broad** - Understand structure before deep diving
2. **Use site search** - Often faster than manual navigation
3. **Check footer links** - Often contains sitemap, policies, hidden sections
4. **Note URL patterns** - `/products/{id}`, `/docs/{category}/{page}`
5. **Save auth state** - Don't re-login repeatedly
6. **Respect robots.txt** - Be aware of restricted areas
7. **Rate-limit** - Add small delays for large crawls
