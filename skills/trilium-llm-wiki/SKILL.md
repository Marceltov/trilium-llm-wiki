---
name: trilium-llm-wiki
description: Maintain an LLM wiki inside Trilium Notes following Karpathy's "LLM wiki" pattern - ingest raw sources into interlinked summary, concept, entity and hub pages, answer questions from the wiki, and lint it - using the schema note (#llmWikiSchema) as the rulebook. Use when the user says "ingest", "process the sources", "lint the wiki", "ask the wiki", "file this in the wiki", or mentions the LLM wiki / graphkasten / knowledge base, and to bootstrap the structure when it does not exist yet.
---

# LLM Wiki in Trilium Notes

The pattern ([Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)):
the user curates **raw sources**, the assistant compiles them into a **wiki** of
interlinked pages, and a **schema note** holds the conventions. The maintenance humans give up
on (cross-references, touching 15 pages per source) is the assistant's job. Trilium Notes supplies the
pieces Obsidian-based setups build by hand: labels instead of frontmatter, internal links plus
relations as the graph, the note map for review, saved searches as views, and the journal day
note as the log.

**The schema note is the source of truth, not this file.** This skill only tells you how to find
it and which tools implement each step. Conventions the user changes in the schema win.

If more than one Trilium Notes instance is connected this session, resolve which one to use first (the wiki lives in one of them) — see [Working with multiple instances](reference/shared-rules.md#working-with-multiple-instances).

The tools are those of Trilium Notes' built-in MCP server (0.106+, at `/mcp`, connected directly
or through [trilium-mcp-proxy](https://github.com/Marceltov/trilium-mcp-proxy)). Text notes go in
and come out as **Markdown**; Trilium stores them as HTML. Internal links are inline HTML
(`<a class="reference-link" href="#root/<noteId>">Title</a>`) inside the Markdown and survive the
round trip. Three things the built-in tools don't do:

- No day-note tool: find today's note with `search_notes('#dateNote="<YYYY-MM-DD>"')` (quoted:
  the value has hyphens).
- `set_attribute` **replaces** an existing attribute of the same type and name. It can't add a
  second `wikiTopic` or `relatesTo`: give a page its main topic and clone it into the other hub,
  and link related pages inline (Trilium turns inline links into `internalLink` relations).
- `create_note` can't make note maps (see *Bootstrap*).

## Look something up

Answering a question, or checking what the wiki knows in the middle of other work, needs **no
schema, no structure lookup and no lock**. Searching is what Karpathy's pattern calls for once a
wiki outgrows its index: links are the human's browsing and the lint pass, not the way to find a
page.

1. **Recall.** In Claude Code a prompt hook may already have added `Wiki recall …` passages to
   the context; use those. Otherwise call `recall("<the question>")` (MCP server `trilium-recall`,
   from the [trilium-recall](https://trilium-recall.marceltov.de/) plugin). Call it on your own before homelab or infrastructure work, on
   unfamiliar errors, hosts or services, and before decisions the wiki may already have made.
2. **Read the pages it points at** (one to three) with `get_note_content`. A hit is a pointer, not
   the answer: the index can lag behind Trilium by a minute, so rely on the page, not the
   passage. If a page links to the one that holds the answer, follow that one link.
3. **Answer** with links to the pages. No recall tool, or no hit: one keyword search
   (`search_notes("#wiki <keywords>")`); still nothing: say the wiki has nothing on it. Read a
   topic's hub and walk its links only as a last resort.
4. If the answer took synthesis across several pages, offer to file it as a concept page. That
   is a write: continue with *Write to the wiki*.

## Write to the wiki

Ingest, adopt, lint, filing an answer, and any other change.

1. **Load the schema.** `search_notes("#llmWikiSchema", fastSearch=true)`. Exactly one hit is
   expected. `get_note_content` it and follow it. If there is no hit, go to *Bootstrap* below.

2. **Resolve the structure once per session.** `search_notes("#llmWikiPart")` returns the six
   parts (`schema`, `locks`, `wiki`, `sources`, `templates`, `views`); `search_notes("#llmWikiTemplate")`
   returns the four templates. Keep the noteIds; only notes that *own* the marker label count
   (instances inherit a template's labels, so filter on `attribute.noteId == note.noteId`).

3. **Take the write lock before the first write**, and release it when done (schema section
   *Write lock*). Other sessions may be writing to the same wiki, and an overwrite through the
   tools leaves no revision. Reading needs no lock.

4. **Pick the workflow** from what the user asked. Each is specified in the schema; the tool
   mapping is:

   | Schema step | Tools |
   |---|---|
   | Write lock | claim: `create_note` under *Locks* (`<session>: <task>`); check: `search_notes("note.parents.labels.llmWikiPart = locks note.utcDateModified >= NOW-1800 orderBy note.utcDateCreated")`, yours must be first; keep alive: `set_note_content` on the claim; release: `delete_note` |
   | Pending sources | run the view's query: `get_note(view)` → `searchString` label → `search_notes(query)` |
   | File a loose source | a note directly under *Sources* → `move_note` into `Sources/<year>` (`#wikiSourceGroup=<year>`, create if missing); the note keeps its noteId, links and attributes |
   | Read a source | `get_note_content`; attachments are listed by `get_note`, read them with `get_attachment_content` |
   | Collect a link-only source | raw fetch (`curl` from a shell; without one, the web-fetch tool and `#fetchedVia=summary`) → `create_note` *Fetched copy* under the link note → `set_attribute` `sourceUrl`, `fetchedOn`, `fetchedVia`, `aiAssisted` |
   | Find existing pages | `recall("<topic or title words>")` first when the `recall` tool is available (a few hundred tokens, finds paraphrases and German/English); then `search_notes("#wiki #wikiTopic=<slug>")`, `search_notes("#wiki <title words>")` to be sure nothing is duplicated |
   | Create a page | `create_note` (type `text`, under the hub) then `set_attribute` relation `template` → template id, then the promoted labels (`wikiTopic`, `wikiStatus`, `aiAssisted`) and, for summaries, relation `wikiSource` → the raw note |
   | Write / extend a page | `get_note_content` → edit the Markdown → `set_note_content` with the whole page (`edit_note_content` doesn't work on text notes). Never replace a page you did not read first. |
   | Link pages | inline `<a class="reference-link" href="#root/<noteId>">Title</a>`; one typed edge via `set_attribute` relation `relatesTo` |
   | Clone into a second topic | `clone_note` with the other hub as `parentNoteId` |
   | Log | find the day note (`search_notes('#dateNote="<today>"')`; if there is none yet, create it under the month note `#monthNote="<YYYY-MM>"`, titled like its siblings, with label `dateNote=<today>`) → `get_note_content` → add a list item under `## Wiki` (create the heading on the first action of the day) → `set_note_content`, reading the day note right before writing it (see the schema's *Log format*) |

5. **Respect the boundaries in the schema:** never edit anything under *Sources* (it is
   `#readOnly`; the MCP tools would still allow it, so this is on you) beyond adding the *Fetched copy* of a
   link-only source, never set `#wikiStatus=reviewed`
   yourself, never create a page without first searching for an existing one, and never leave
   a new page unlinked from its hub.

6. **Report back** in the shape the schema asks for: created pages, updated pages, new stubs,
   issues created, open questions for the user. Link noteIds so the user can jump to them.

## Bootstrap (no schema note found)

Offer the user two ways to create the structure. Both are idempotent and safe to re-run.

- **Through the MCP tools** (the default: works on claude.ai and in Claude Code, and needs no
  credentials beyond the MCP connection): see below.
- **Script** (faster, but only when the user already has an ETAPI token and Trilium's ETAPI is
  reachable from this machine; the MCP connection's OAuth sign-in does not cover it):
  `python3 <this skill's folder>/setup.py --url <trilium-url> --token <etapi-token>` creates the
  `LLM Wiki` root with `Schema`, `Locks`, `Graph` and `Review graph` (note maps), `Wiki`, `Sources` (plus the current year folder), `Templates` (4) and `Views` (7) under
  `root` (`--parent <noteId>` to put it elsewhere, `--dry-run` to preview). The schema text is
  `schema.html` in the same folder; `--update-schema` pushes a changed file into an existing note.
  That **replaces the whole note**, including conventions the user added to their schema: only use
  it when the user asks, and on a customised schema merge the new default sections in by hand
  instead.
- **How the MCP route works:** read `setup.py`'s declarations
  (`TEMPLATES`, `VIEWS`, the labels on each part) and create the same notes with `create_note`
  and `set_attribute`, then put the text of `schema.html` into the Schema note with
  `set_note_content` (as Markdown). Saved searches are `create_note` with type `search` plus a
  `searchString` label. The built-in tools can't create note maps: leave `Graph` and
  `Review graph` out and tell the user to add them in Trilium (*new note → Note Map*, labels
  `mapType` and `mapRootNoteId` as in `setup.py`), or run the script.

After bootstrapping, point the user at the schema note and suggest the first ingest: drop a
web clip or article under *Sources* and say "ingest".

## Notes

- Clips that land elsewhere (Trilium Notes' inbox, often the day note) and belong in the wiki
  must be moved under *Sources/<year>* with `move_note`, otherwise they inherit neither
  `#readOnly` nor `#wikiSource` and never show up as pending.
- Search values with hyphens or spaces must be quoted: `#wikiTopic="machine-learning"`.
- A `!=` test on an inherited label (`#wikiType != hub`) only works as the **first** clause of
  a query (Trilium Notes 0.106). Prefer positive filters (`#wikiType=concept`) where you can.
- One ingest is typically 20 to 40 tool calls. Do them; do not summarise a source into a single
  page and stop.
