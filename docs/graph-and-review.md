# Graph and review

## The graph

*Graph* is a Trilium note map (type *Note Map*, `#mapType=link`) rooted at *Wiki*. It works like Obsidian's graph view: every page is a node, every link or relation between pages is an edge. Links are made from the pages' text, so the graph grows as Claude writes.

![The wiki's graph in Trilium Notes: hub pages (violet) such as Homelab, Trilium and Hetzner, each surrounded by its concept (green), entity (orange) and summary (blue) pages, linked to each other and to the Wiki root](assets/graph.png){ width="560" }

Nodes are coloured by page type through a `#color` label on each template:

| Type | Colour |
|---|---|
| Hub | violet `#8b5cf6` |
| Source summary | blue `#3b82f6` |
| Concept | green `#22c55e` |
| Entity | orange `#f97316` |

Pages created from a template inherit the colour. A page you adopted into the wiki without a template needs its own `#color` label; lint adds missing ones.

Parent and child placement in the tree is not drawn, so a node floating alone is an orphan: nothing links to it.

## Narrowing the graph

Trilium has no filter panel on the map, but a note map can be rooted at any note:

- **One topic:** a note map with `#mapRootNoteId` set to that topic's hub.
- **Any query:** a note map rooted at a saved search shows only the matching pages and the links between them, for example one `#wikiTopic`, only `#wikiType=entity`, or only stubs.
- **One page's neighbourhood:** the *Note map* button in a page's ribbon, like Obsidian's local graph.
- **Hide a note:** `#excludeFromNoteMap` keeps it out of every map.

## Review

The view *To review* is the review queue: every page that is a draft or has no status at all, newest change first. *Review graph* shows the same pages as a map.

1. After an ingest, open the topic hub's note map or *Review graph*. Wrong links, misfiled pages and bad topic names are cheapest to fix right then.
2. Read a page. If you accept it, set `#wikiStatus=reviewed`; it drops out of the queue and the review graph.
3. If not, tell Claude what to change. It stays a draft.

Claude never sets `reviewed` itself.
