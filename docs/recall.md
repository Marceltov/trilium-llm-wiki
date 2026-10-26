# Recall

Recall lets Claude find what your wiki, and the rest of your Trilium Notes, already knows on its
own: a small container next to Trilium Notes, a Claude Code prompt hook and an MCP `recall` tool.

It has moved to its own project: **[trilium-recall](https://trilium-recall.marceltov.de/)**. Up to
0.4.x it lived here as `recall-engine/`, with the image `ghcr.io/marceltov/trilium-llm-wiki-recall`.

The wiki uses recall when it is connected. Without it, lookups fall back to Trilium's search.
