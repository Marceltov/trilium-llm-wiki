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

Say "lint the wiki", roughly weekly. Claude works through the views: pending sources, orphan pages, stubs, the review queue, contradictions between pages, missing colours, work items that belong in an issue tracker, and stale lock claims. It fixes what is mechanical and lists what needs you.

## Adopt

Say that a finding from a work session belongs in the wiki: a debugging result, a migration, a setup. Claude writes or extends concept and entity pages with the symptoms, cause, fix and the decisions behind them. Anything still to do goes into an issue in the repository that owns it, not into the wiki.

## Knowledge, not tasks

The wiki records what is known. To-dos belong in your issue tracker; a page may only reference an issue next to the fact it concerns. "Open questions" on a page are knowledge gaps that a source or a look at the system would answer.
