---
hide:
  - toc
---

<div class="tm-hero" markdown>

# An LLM wiki in Trilium Notes, kept up by Claude

<p class="tm-hero__lead">You collect sources: web clips, articles, PDFs, notes from a work session. Claude turns them into a wiki of linked summary, concept, entity and topic pages, answers questions from it, and keeps it tidy. The rules live in a schema note inside your Trilium Notes instance, so you can change them.</p>

[Install it](install.md){ .md-button .md-button--primary } [Set up the wiki](setup.md){ .md-button }

</div>

```
/plugin marketplace add Marceltov/trilium-llm-wiki
/plugin install trilium-llm-wiki
```

!!! warning "Needs a running Trilium Notes MCP server"

    This plugin is only the client half. You need the [Trilium Notes MCP server](https://trilium-mcp.marceltov.de/) deployed next to your Trilium Notes instance first (see its [quick start](https://trilium-mcp.marceltov.de/getting-started/)).

## The idea

The pattern comes from [Andrej Karpathy's "LLM wiki"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): people are good at picking what to read and bad at the upkeep a wiki needs, such as cross-references, updating ten pages when one new source arrives, and noticing contradictions. That upkeep is the assistant's job here.

Trilium Notes already has the pieces other setups build by hand: labels instead of frontmatter, links and relations as the graph, a note map to look at it, saved searches as views and the journal day note as a log.

## What you get

- **A ready structure.** One command (or one request on claude.ai) creates the schema note, read-only *Sources*, the *Wiki*, four page templates, saved-search views, two graphs and a lock folder. See [Set up the wiki](setup.md).
- **Workflows.** *Ingest* a source, *query* the wiki, *lint* it, *adopt* a finding from a work session. See [Workflows](workflows.md).
- **A graph like Obsidian's.** Pages coloured by type, a review queue and a graph of what is still unreviewed. See [Graph and review](graph-and-review.md).
- **Safe with several sessions.** A write lock stops two Claude sessions from overwriting each other's edits. See [Write lock](write-lock.md).
- **Your rules.** The schema is a note you edit. The plugin never overwrites it unless you ask. See [Customise your schema](customise.md).

## LLM wiki or general note skills?

This plugin is for building an LLM wiki. If you want Claude to work with the notes you already have (search, create, move, tag, journal, export), install the [Trilium Notes plugin](https://trilium-plugin.marceltov.de/) instead, or next to this one. Both share the same MCP connection.
