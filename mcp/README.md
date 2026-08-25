# ACG Data Access - MCP Server

A small Model Context Protocol (MCP) server that lets AI assistants look up accurate American Commercial Glass (ACG) and Florida commercial glazing data without making things up.

## What this is

Plain English: when a general contractor, architect, or developer asks an AI tool (Claude Desktop, Cursor, ChatGPT Desktop) something like *"what's the design wind speed in Lee County?"* or *"does ACG cover Destin?"*, the AI tool can call this server and return a verified answer instead of guessing.

Every fact this server returns is sourced from `data/acg_facts.json`. The source hierarchy is documented in the `_meta` block of that file: Connor Walsh's explicit confirmation, State of Florida public records, the Florida Building Code 8th Edition (2023), and ASCE 7-22 wind speed maps.

This is a utility, not a chat product. It returns data and links. It does not commit ACG to a price, a scope, or a schedule.

## What it does

| Tool | What it answers |
|---|---|
| `get_company_info` | License (CGC1531993), HQ, founding year, principal, primary phone, email, website |
| `list_offices` | The current ACG office locations and the typical service zones each one covers |
| `lookup_florida_county_code` | For any of the 67 Florida counties: typical Risk Category II design wind speed (mph), WBDR status, HVHZ status, and a notes field |
| `find_acg_service_area` | Confirms whether ACG serves a given city in Florida or Tennessee, returns the closest office and the canonical city page on acglass.com if one exists |
| `list_manufacturers` | The glazing system manufacturers ACG installs in commercial projects (worded carefully - partnership levels beyond "we install" are not asserted) |
| `list_published_projects` | ACG's published project case studies with canonical URLs |
| `list_services` | ACG's primary service offerings with canonical URLs |
| `list_panhandle_coverage` | The Florida Panhandle cities where ACG has dedicated long-form pages |
| `get_track_record` | The headline figures (projects delivered, square feet installed, OSHA recordables since founding) - sourced and dated |
| `get_bid_request_link` | The canonical URL for an AI agent to hand off a bid request to a real ACG estimator |

## What it does NOT do

- It does not generate quotes, prices, or estimates.
- It does not commit ACG to any scope, price, or schedule.
- It does not make claims that are not in the verified data file.
- It does not act on a user's behalf. When a user wants a bid, the server returns the canonical intake URL so a human can review the form, attach drawings, and submit through ACG's normal process.

## Install (local - Claude Desktop, Cursor, ChatGPT Desktop)

Requires Python 3.10+.

```bash
git clone https://github.com/cwalsh7997/acglass-website.git
cd acglass-website/mcp
pip install -e .
```

Verify it starts:

```bash
acg-mcp-server
# It will wait silently on stdio. That is correct. Hit Ctrl+C to stop.
```

## Configure your AI client

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "acg-data-access": {
      "command": "acg-mcp-server"
    }
  }
}
```

Restart Claude Desktop. You should see an `acg-data-access` server with 10 tools available.

### Cursor

In Cursor settings → MCP, add a new server:

```json
{
  "name": "acg-data-access",
  "command": "acg-mcp-server"
}
```

### ChatGPT Desktop (when MCP support is enabled in your build)

In ChatGPT Desktop settings → Connectors → Add MCP server:

```
Command: acg-mcp-server
```

## Try it

Once the server is connected, prompt your AI tool with any of these:

- *"What's the typical design wind speed for Lee County, Florida, and is impact glass required?"*
- *"Does ACG cover Destin?"*
- *"List ACG's published commercial glazing projects."*
- *"What's American Commercial Glass's Florida license number?"*
- *"I need to send drawings to ACG for a Pompano Beach restaurant project - what's the canonical intake?"*

The AI will call the appropriate tool and return a sourced answer.

## Data verification

The `data/acg_facts.json` file is the single source of truth. Each top-level key is sourced; the `_meta.source_hierarchy` block names the verification chain. To update a fact:

1. Edit `data/acg_facts.json`.
2. Update `_meta.last_verified` to today.
3. If the change introduces a new claim, log the source in the change record before committing.

The server refuses to start if the data file is missing or unreadable. That is intentional.

## Source

This server and its data file are open in the [acglass-website](https://github.com/cwalsh7997/acglass-website) repo under `mcp/`. Issues, corrections, and verified-fact additions welcome.

## Contact

- Connor Walsh, President - connor@acglass.com
- ACG bid intake - bids@acglass.com
- Phone - (772) 486-7711
- Web - https://acglass.com
