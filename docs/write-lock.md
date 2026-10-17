# Write lock

Several Claude sessions can work on the same Trilium Notes instance at once: one ingesting, one adopting a finding, one linting. When two of them replace the same note, the later write wins, and Trilium keeps no revision of an overwrite made through its API. The schema therefore lets only one session write to the wiki at a time.

## How it works

The lock is a queue of **claims** under *Locks*:

1. Before its first write, a session creates its own claim note, titled with the session's name and what it is about to do.
2. It searches for live claims, oldest first. If its own claim is first, it holds the lock.
3. If another claim is ahead, it tells you who holds the lock and either waits or withdraws.
4. While working, it touches its claim at least every 25 minutes. A claim not modified for 30 minutes has expired and no longer counts.
5. When done, or when it stops early, it deletes its claim.

Reading never needs the lock. Writes that need it: anything under *LLM Wiki* and the *Wiki* section of the day note.

## Why a queue and not one lock note

The obvious design, one lock note with a fixed noteId that a session creates to take the lock, does not work: creating a note with an existing noteId does not fail, it silently replaces the note. Two sessions would both think they hold the lock. Separate claim notes never collide, and their creation times decide the order.

## Things to know

- **It is advisory.** Trilium does not block a write without a claim. The lock works because every session follows the schema, which it reads at the start.
- **You can always clear it.** Delete any claim under *Locks* by hand, for example one left behind by a session that crashed.
- **Claims are hidden from graphs** (`#excludeFromNoteMap` on *Locks*) and are not logged.
