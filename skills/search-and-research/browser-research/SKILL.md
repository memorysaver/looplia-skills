---
name: browser-research
description: |
  Deep web research using agent-browser for interactive pages and JavaScript-rendered content.
  Uses a tiered approach: starts with WebSearch/WebFetch for speed, auto-escalates to
  agent-browser when deeper interaction is needed.

  Trigger phrases:
  - "deep research", "scrape website", "interactive page"
  - "browse and extract", "fill form and get data"
  - "navigate through pages", "click through results"
  - "JavaScript site", "dynamic content"

  Auto-escalates to agent-browser when:
  - WebFetch returns minimal content (JS-rendered pages)
  - Need to interact with forms, filters, or pagination
  - Mission specifies interactive actions

  This is an input-less skill - it executes research missions autonomously.
tools:
  - WebSearch
  - WebFetch
  - Bash
---

# Browser Research

Execute deep web research missions using a tiered approach that balances speed and capability.

## When to Use

- Researching topics that require navigating multiple pages
- Extracting data from JavaScript-rendered websites
- Interacting with forms, filters, or search interfaces
- Scraping content from dynamic web applications
- When WebSearch/WebFetch alone returns incomplete results

## Tiered Research Strategy

### Tier 1: WebSearch (Fastest, ~1-3 seconds)

Use for initial discovery and simple queries:
- General topic searches
- Finding URLs and sources
- News and documentation lookup

```
WebSearch: "topic keywords site:example.com"
```

### Tier 2: WebFetch (Fast, ~2-5 seconds)

Use to extract content from discovered URLs:
- Static page content extraction
- Article and documentation reading
- API documentation parsing

```
WebFetch: url="https://example.com/page" prompt="Extract key information about..."
```

### Tier 3: agent-browser (Slower, ~5-30 seconds)

**Auto-escalate when:**
- WebFetch returns < 100 characters (likely JS-rendered)
- Need to click buttons, fill forms, or navigate
- Content is behind interactive elements
- Mission explicitly requires browser interaction

**Agent-browser workflow:**
```bash
# 1. Open page
agent-browser open "https://example.com"

# 2. Get interactive elements with refs
agent-browser snapshot -i

# 3. Interact using refs
agent-browser click @e2
agent-browser fill @e5 "search query"
agent-browser press Enter

# 4. Wait for content to load
agent-browser wait --load

# 5. Extract data
agent-browser snapshot -i
agent-browser get text @e10
```

## Process

### Step 1: Analyze Mission

Determine research requirements:
- **Target**: What information to find
- **Sources**: Specific sites or general web
- **Depth**: Surface-level or comprehensive
- **Interaction**: Static reading vs form filling

### Step 2: Execute Tiered Search

```
Start with Tier 1 (WebSearch)
  ↓
If URLs found → Tier 2 (WebFetch)
  ↓
If content incomplete/JS-rendered → Tier 3 (agent-browser)
```

### Step 3: Compile Results

Structure findings with:
- Source attribution (URLs)
- Extracted content
- Relevance assessment
- Any limitations encountered

## Agent-Browser Complete Reference

### Core Workflow

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i` to get interactive elements with refs
3. **Interact**: Use refs like `@e1`, `@e2` to click, fill, or manipulate elements
4. **Re-snapshot**: Update after navigation or DOM changes

### Navigation Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `open <url>` | Navigate to URL | `agent-browser open "https://example.com"` |
| `back` | Go back in history | `agent-browser back` |
| `forward` | Go forward | `agent-browser forward` |
| `reload` | Refresh page | `agent-browser reload` |

### Snapshot Options

```bash
agent-browser snapshot                    # Full accessibility tree
agent-browser snapshot -i                 # Interactive elements only (recommended)
agent-browser snapshot -c                 # Compact mode (removes empty elements)
agent-browser snapshot -d 3               # Limit depth to 3 levels
agent-browser snapshot -s "#main"         # Scope to CSS selector
agent-browser snapshot -i -c -d 5         # Combine options
```

| Flag | Description |
|------|-------------|
| `-i, --interactive` | Show only buttons, links, inputs |
| `-c, --compact` | Strip empty structural elements |
| `-d, --depth <n>` | Restrict tree depth |
| `-s, --selector <sel>` | Filter to CSS selector scope |

### Interaction Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `click @ref` | Click element | `agent-browser click @e2` |
| `dblclick @ref` | Double-click | `agent-browser dblclick @e2` |
| `fill @ref <text>` | Clear and fill input | `agent-browser fill @e3 "query"` |
| `type @ref <text>` | Type into element | `agent-browser type @e3 "text"` |
| `press <key>` | Press keyboard key | `agent-browser press Enter` |
| `select @ref <val>` | Select dropdown option | `agent-browser select @e4 "option1"` |
| `check @ref` | Check checkbox | `agent-browser check @e5` |
| `uncheck @ref` | Uncheck checkbox | `agent-browser uncheck @e5` |
| `hover @ref` | Hover over element | `agent-browser hover @e2` |
| `focus @ref` | Focus element | `agent-browser focus @e3` |
| `upload @ref <files>` | Upload files | `agent-browser upload @e6 "file.pdf"` |
| `drag @src @tgt` | Drag and drop | `agent-browser drag @e1 @e2` |
| `scroll <dir> [px]` | Scroll page | `agent-browser scroll down 500` |

### Information Retrieval

| Command | Purpose | Example |
|---------|---------|---------|
| `get text @ref` | Extract text content | `agent-browser get text @e5` |
| `get html @ref` | Get innerHTML | `agent-browser get html @e5` |
| `get value @ref` | Get input field value | `agent-browser get value @e3` |
| `get url` | Current page URL | `agent-browser get url` |
| `get title` | Page title | `agent-browser get title` |
| `screenshot [path]` | Capture viewport | `agent-browser screenshot page.png` |
| `screenshot --full` | Full page capture | `agent-browser screenshot --full page.png` |

### State Checking

| Command | Purpose | Example |
|---------|---------|---------|
| `is visible @ref` | Check visibility | `agent-browser is visible @e2` |
| `is enabled @ref` | Check if enabled | `agent-browser is enabled @e3` |
| `is checked @ref` | Check checkbox state | `agent-browser is checked @e5` |

### Wait Commands

```bash
agent-browser wait <selector>              # Wait for element visibility
agent-browser wait <ms>                    # Wait duration in milliseconds
agent-browser wait --text "Welcome"        # Wait for text to appear
agent-browser wait --url "**/dashboard"    # Wait for URL pattern match
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --load domcontentloaded # Wait for DOM ready
agent-browser wait --fn "window.ready === true"  # Wait for JS condition
```

**Load States:** `load`, `domcontentloaded`, `networkidle`

### Semantic Locators (find command)

Find elements by role, text, or label instead of refs:

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@test.com"
agent-browser find placeholder "Search" fill "query"
agent-browser find alt "Logo" click
agent-browser find title "Help" click
agent-browser find testid "submit-btn" click
agent-browser find first ".item" click
agent-browser find last "a" click
agent-browser find nth 2 "a" text
```

**Supported Actions:** `click`, `fill`, `check`, `hover`, `text`

### Session Management

Sessions provide isolated browser instances with separate cookies, storage, and history:

```bash
# Named sessions for parallel research
agent-browser --session research1 open "https://site-a.com"
agent-browser --session research2 open "https://site-b.com"

# Environment variable
AGENT_BROWSER_SESSION=research1 agent-browser click @e2

# List active sessions
agent-browser session list

# Show current session
agent-browser session
```

### Global Options

| Option | Purpose |
|--------|---------|
| `--session <name>` | Use named isolated session |
| `--json` | Machine-readable JSON output |
| `--headed` | Display visible browser window |
| `--debug` | Enable debug logging |
| `--executable-path <path>` | Custom browser binary |

### Selector Types

- **Refs** (recommended): `@e1`, `@e2` from snapshot output - deterministic selection
- **CSS**: `#id`, `.class`, `button[type=submit]`
- **Text**: Elements containing specific text
- **Semantic**: Via `find` command (role, label, text)

## Output Format

```json
{
  "query": "original research mission",
  "strategy": "tiered",
  "tiers_used": ["WebSearch", "WebFetch", "agent-browser"],
  "results": [
    {
      "source": "https://example.com/page",
      "title": "Page Title",
      "content": "Extracted content...",
      "extraction_method": "WebFetch | agent-browser",
      "timestamp": "2025-01-19T10:30:00Z"
    }
  ],
  "summary": "Brief summary of findings",
  "limitations": "Any access issues or incomplete extractions"
}
```

## Examples

### Example 1: Research with Auto-Escalation

Mission: "Find the pricing tiers for Acme SaaS product"

```
1. WebSearch: "Acme SaaS pricing"
   → Found: https://acme.example.com/pricing

2. WebFetch: Extract pricing from URL
   → Result: Only 50 chars (JS-rendered page)

3. Auto-escalate to agent-browser:
   agent-browser open "https://acme.example.com/pricing"
   agent-browser wait --load
   agent-browser snapshot -i
   agent-browser get text @e15  # Pricing table
   → Full pricing information extracted
```

### Example 2: Form-Based Search

Mission: "Search job listings for 'AI Engineer' in San Francisco"

```
1. WebSearch: "AI Engineer jobs San Francisco site:jobs.example.com"
   → Found job board URL

2. agent-browser (form interaction required):
   agent-browser open "https://jobs.example.com"
   agent-browser snapshot -i
   agent-browser fill @e3 "AI Engineer"
   agent-browser fill @e4 "San Francisco"
   agent-browser click @e5  # Search button
   agent-browser wait --load
   agent-browser snapshot -i
   → Extract job listings from results
```

## Important Rules

1. **Start fast** - Always try WebSearch/WebFetch first
2. **Auto-escalate intelligently** - Only use agent-browser when needed
3. **Attribute sources** - Include URLs for all extracted content
4. **Handle failures gracefully** - Report access issues in output
5. **Respect rate limits** - Don't hammer sites with rapid requests
6. **Session isolation** - Use named sessions for complex multi-tab research
