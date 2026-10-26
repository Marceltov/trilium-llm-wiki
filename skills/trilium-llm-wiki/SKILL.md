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

Tool names below are trilium-mcp's. Trilium's built-in MCP server (`/mcp`, also behind
trilium-mcp-proxy) names them `search_notes`, `get_note`, `get_note_content`, `create_note`,
`set_note_content` (or `edit_note_content` / `append_to_note` for partial writes),
`set_attribute`, `delete_attribute`, `clone_note` (= `postBranch`), `move_note` (replaces
`postBranch` + `deleteBranchById`), `rename_note`, `delete_note`, `get_attachment` and
`get_attachment_content`; it has no day-note tool, so find the day note with
`search_notes("#dateNote=<YYYY-MM-DD>")`.

## Look something up

Answering a question, or checking what the wiki knows in the middle of other work, needs **no
schema, no structure lookup and no lock**. Searching is what Karpathy's pattern calls for once a
wiki outgrows its index: links are the human's browsing and the lint pass, not the way to find a
page.

1. **Recall.** In Claude Code a prompt hook may already have added `Wiki recall …` passages to
   the context; use those. Otherwise call `recall("<the question>")` (MCP server `wiki-recall`,
   see `trilium-recall-setup`). Call it on your own before homelab or infrastructure work, on
   unfamiliar errors, hosts or services, and before decisions the wiki may already have made.
2. **Read the pages it points at** (one to three) with `getNoteContent`. A hit is a pointer, not
   the answer: the index can lag behind Trilium by a minute, so rely on the page, not the
   passage. If a page links to the one that holds the answer, follow that one link.
3. **Answer** with links to the pages. No recall tool, or no hit: one keyword search
   (`searchNotes("#wiki <keywords>")`); still nothing: say the wiki has nothing on it. Read a
   topic's hub and walk its links only as a last resort.
4. If the answer took synthesis across several pages, offer to file it as a concept page. That
   is a write: continue with *Write to the wiki*.

## Write to the wiki

Ingest, adopt, lint, filing an answer, and any other change.

1. **Load the schema.** `searchNotes("#llmWikiSchema", fastSearch=true)`. Exactly one hit is
   expected. `getNoteContent` it and follow it. If there is no hit, go to *Bootstrap* below.

2. **Resolve the structure once per session.** `searchNotes("#llmWikiPart")` returns the six
   parts (`schema`, `locks`, `wiki`, `sources`, `templates`, `views`); `searchNotes("#llmWikiTemplate")`
   returns the four templates. Keep the noteIds; only notes that *own* the marker label count
   (instances inherit a template's labels, so filter on `attribute.noteId == note.noteId`).

3. **Take the write lock before the first write**, and release it when done (schema section
   *Write lock*). Other sessions may be writing to the same wiki, and an ETAPI overwrite leaves no
   revision. Reading needs no lock.

4. **Pick the workflow** from what the user asked. Each is specified in the schema; the tool
   mapping is:

   | Schema step | Tools |
   |---|---|
   | Write lock | claim: `createNote` under *Locks* (`<session>: <task>`); check: `searchNotes("note.parents.labels.llmWikiPart = locks note.utcDateModified >= NOW-1800 orderBy note.utcDateCreated")`, yours must be first; keep alive: `putNoteContentById` on the claim; release: `deleteNoteById` |
   | Pending sources | run the view's query: `getNoteById(view)` → `searchString` label → `searchNotes(query)` |
   | File a loose source | a note directly under *Sources* → move it into `Sources/<year>` (`#wikiSourceGroup=<year>`, create if missing): `postBranch` with the year folder as `parentNoteId`, then `deleteBranchById` on the old branch (the note keeps its noteId, links and attributes) |
   | Read a source | `getNoteContent`, `getNoteAttachments` + `getAttachmentContent` |
   | Collect a link-only source | raw fetch (`curl` from a shell; without one, the web-fetch tool and `#fetchedVia=summary`) → `createNote` *Fetched copy* under the link note → `postAttribute` `sourceUrl`, `fetchedOn`, `fetchedVia`, `aiAssisted` |
   | Find existing pages | `recall("<topic or title words>")` first when the `recall` tool is available (a few hundred tokens, finds paraphrases and German/English); then `searchNotes("#wiki #wikiTopic=<slug>")`, `searchNotes("#wiki <title words>")` to be sure nothing is duplicated |
   | Create a page | `createNote` (type `text`, under the hub) then `postAttribute` relation `template` → template id, then the promoted labels (`wikiTopic`, `wikiStatus`, `aiAssisted`) and, for summaries, relation `wikiSource` → the raw note. Same mechanics as `trilium-create-note-from-template`. |
   | Write / extend a page | `getNoteContent` → edit the HTML → `putNoteContentById`. Never replace a page you did not read first. |
   | Link pages | inline `<a class="reference-link" href="#root/<noteId>">Title</a>`; typed edges via `postAttribute` relation `relatesTo` |
   | Clone into a second topic | `postBranch` with the other hub as `parentNoteId` |
   | Log | `getDayNote(today)` → `getNoteContent` → add an `<li>` to the list under `<h2>Wiki</h2>` (create the heading on the first action of the day) → `putNoteContentById`, reading the day note right before writing it (see the schema's *Log format*) |

5. **Respect the boundaries in the schema:** never edit anything under *Sources* (it is
   `#readOnly`; ETAPI would still allow it, so this is on you) beyond adding the *Fetched copy* of a
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
  (`TEMPLATES`, `VIEWS`, the labels on each part) and create the same notes with `createNote`
  and `postAttribute`, then put `schema.html` into the Schema note with `putNoteContentById`.
  Saved searches are `createNote` with type `search` plus a `searchString` label. Note maps are
  `createNote` with type `text`, then `patchNoteById` to type `noteMap`, plus `mapType` and
  `mapRootNoteId` labels.

After bootstrapping, point the user at the schema note and suggest the first ingest: drop a
web clip or article under *Sources* and say "ingest".

## Notes

- `getInboxNote` is Trilium Notes' general inbox (often the day note). Clips the user wants in the
  wiki should be moved under *Sources/<year>* (`postBranch` under the
  year folder, then `deleteBranchById` on the old branch), otherwise they inherit neither `#readOnly` nor `#wikiSource` and never show
  up as pending.
- Search values with hyphens or spaces must be quoted: `#wikiTopic="machine-learning"`.
- A `!=` test on an inherited label (`#wikiType != hub`) only works as the **first** clause of
  a query (Trilium Notes 0.106). Prefer positive filters (`#wikiType=concept`) where you can.
- One ingest is typically 20 to 40 tool calls. Do them; do not summarise a source into a single
  page and stop.
