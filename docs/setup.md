# Set up the wiki

The first time you use the wiki skill, Claude searches for the schema note (`#llmWikiSchema`). If there is none, it offers to create the structure. Both ways are safe to run again: they find what exists by its labels and only add what is missing.

## What gets created

```
LLM Wiki                  #llmWiki
├── Schema                #llmWikiSchema       the rulebook (from schema.html)
├── Locks                 #llmWikiPart=locks   write-lock claims, hidden from graphs
├── Graph                 note map of Wiki
├── Review graph          note map of the "To review" view
├── Wiki                  #llmWikiPart=wiki    one child per topic hub
├── Sources               #llmWikiPart=sources read-only, raw material
│   └── 2026              #wikiSourceGroup     one folder per year
├── Templates             hub, source summary, concept, entity
└── Views                 saved searches: to review, pending sources,
                          stubs, drafts, orphans, recent changes, hubs
```

## The default: ask Claude

Ask Claude to "set up the LLM wiki". It reads the declarations in `setup.py` and creates the notes through the MCP tools, so it works in Claude Code and on claude.ai alike and needs nothing beyond the MCP connection you already signed in to. Trilium's MCP tools can't create note maps, so this route leaves out `Graph` and `Review graph` and tells you how to add them in Trilium by hand; the script below creates them.

## Faster: the script (needs an ETAPI token)

```
python3 <skill folder>/setup.py --url https://trilium.example.com --token "$TRILIUM_ETAPI_TOKEN"
```

The skill folder is `skills/trilium-llm-wiki/` in a clone of this repository, or the installed plugin's copy; Claude knows where it is. The script talks to Trilium Notes' ETAPI directly, so it needs an ETAPI token (*Options → ETAPI*; the MCP connection's OAuth sign-in does not cover it) and a machine that can reach Trilium itself, not only the MCP server. It gives the same result in fewer round trips. Useful options:

| Option | What it does |
|---|---|
| `--dry-run` | prints what would be created, writes nothing |
| `--parent <noteId>` | creates *LLM Wiki* under that note instead of the root |
| `--update-schema` | replaces the schema note's content with `schema.html`; see [Customise your schema](customise.md) before using it |

## First ingest

Drop a web clip, a pasted article or a PDF under *Sources* and say "ingest". See [Workflows](workflows.md).
