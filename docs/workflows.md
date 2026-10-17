# Workflows

Each workflow is written out in full in the schema note; this page is the overview. Every workflow that writes takes the [write lock](write-lock.md) first and records what it did in the day note under a *Wiki* heading.

## Page types

| Type | What it is |
|---|---|
| **Hub** | Entry point of a topic: what it covers, its key pages, what the wiki does not know yet. |
| **Source summary** | One page per ingested source, linked to the raw note with `~wikiSource`. |
| **Concept** | An idea, method or pattern, synthesised across sources, citing the summaries. |
| **Entity** | A person, organisation, product, tool, place or dataset. |

Pages carry `#wikiTopic`, `#wikiStatus` (`stub`, `draft`, `reviewed`) and `#aiAssisted`. Only you set `reviewed`.

## Ingest

Say "ingest" or "process the sources". Claude:

1. Moves a source dropped directly under *Sources* into its year folder.
2. Reads it in full. A source that is only a link gets fetched first and stored as a *Fetched copy* under it.
3. Tells you the key takeaways and the topics it would file them under.
4. Writes a summary page under the topic hub, and updates every concept and entity page the source touches (often 5 to 15 pages), creating stubs for new ones.
5. Links everything from the hub, logs it, and reports what changed.

## Query

Ask the wiki a question ("what does the wiki say about…"). Claude reads the hub first, then the pages it links, and answers with links. If the answer needed synthesis across several pages, it offers to save it as a new concept page.

## Lint

Say "lint the wiki", roughly weekly. Claude works through the views: pending sources, orphan pages, stubs, the review queue, contradictions between pages, missing colours, open to-dos (moving them to a to-do app or issue tracker where one is connected), and stale lock claims. It fixes what is mechanical and lists what needs you.

## Adopt

Say that a finding from a work session belongs in the wiki: a debugging result, a migration, a setup. Claude writes or extends concept and entity pages with the symptoms, cause, fix and the decisions behind them. Work still to do on the code goes into an issue in the repository that owns it; other to-dos go to a connected to-do app or onto the page.

## To-dos, and work on code

| Kind | Goes to | Otherwise |
|---|---|---|
| To-do (look up, try, buy, decide) | a to-do app connected through MCP, for example Todoist | a *To do* checklist on the page |
| Work on code (build, fix, change in a repository) | the repository's issue tracker, when Claude can reach it | a *To do* item on the page, marked with the repository |

The page names the task or links the issue next to the fact it concerns. When it isn't clear where something goes (several apps, no clear repository, personal or not), Claude asks you, and writes a standing answer into the schema.
