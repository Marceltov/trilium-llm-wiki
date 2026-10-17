# Customise your schema

The schema note is the source of truth. The skill only tells Claude how to find it and which tools implement each step; when the schema says something different, the schema wins. Change it whenever you and Claude agree on a new convention, in the note rather than in a chat, so every later session follows it.

Typical changes:

- Different sections on a page type.
- A rule about your sources, for example how to treat a bookmarking tool's imports.
- Where to-dos go: by default a connected to-do app, else the page, and work on code to the repository's issue tracker; yours might name one app or one tracker for everything.
- Stricter or looser linking.

## Updating to a newer default

A new plugin version may bring a newer `schema.html`. Re-running `setup.py` without options adds new parts, views, templates and labels, and never touches the schema text.

`setup.py --update-schema` replaces the **whole** schema note with the default. Anything you added is gone, and because the write goes through the API, Trilium keeps no revision of your version. On a schema you have changed, do this instead:

1. Ask Claude to compare your schema with the new `schema.html`.
2. Let it merge the new default sections into your note, keeping yours.
3. Read the result before it is written.

## Templates and views

Templates and views are ordinary notes, so you can change them too. Keep their marker labels (`#llmWikiTemplate`, `#llmWikiView`, `#llmWikiPart`, `#llmWikiMap`): `setup.py` and the skill find the structure by them.
