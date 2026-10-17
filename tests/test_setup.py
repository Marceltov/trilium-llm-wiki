"""Run skills/trilium-llm-wiki/setup.py twice against an in-memory fake of ETAPI.

The first run must create the whole structure, the second must write nothing.
Run with: python3 -I tests/test_setup.py
"""
import importlib.util
import itertools
import sys
import urllib.parse
from pathlib import Path

SETUP = Path(__file__).resolve().parent.parent / "skills" / "trilium-llm-wiki" / "setup.py"

spec = importlib.util.spec_from_file_location("setup", SETUP)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)

notes, attrs, ids, calls = {}, {}, itertools.count(1), []


def fake_call(self, method, path, body=None, raw=None, ctype=None):
    calls.append(method)
    if path == "/app-info":
        return {"appVersion": "fake"}
    if method == "GET" and path.startswith("/notes?"):
        name, _, value = urllib.parse.parse_qs(path.split("?", 1)[1])["search"][0][1:].partition("=")
        hits = []
        for n in notes.values():
            own = [a for a in attrs.values() if a["noteId"] == n["noteId"]]
            if any(a["name"] == name and (not value or a["value"] == value) for a in own):
                hits.append({**n, "attributes": own})
        return {"results": hits}
    if path == "/create-note":
        nid = f"N{next(ids)}"
        notes[nid] = {"noteId": nid, "title": body["title"], "type": body["type"]}
        return {"note": notes[nid]}
    if path == "/attributes":
        aid = f"A{next(ids)}"
        attrs[aid] = {**body, "attributeId": aid}
        return attrs[aid]
    if path.startswith("/attributes/"):
        attrs[path.split("/")[2]].update(body)
    elif path.startswith("/notes/") and method == "PATCH":
        notes[path.split("/")[2]].update(body)
    return None


def own(nid):
    return {a["name"]: a["value"] for a in attrs.values() if a["noteId"] == nid}


def by_marker(name, value=""):
    found = [n for n in notes.values() if own(n["noteId"]).get(name, None) == value]
    assert len(found) == 1, f"expected one note with #{name}={value}, found {len(found)}"
    return found[0]


setup.Etapi._call = fake_call
writes = []
for _ in range(2):
    calls.clear()
    sys.argv = ["setup.py", "--token", "x"]
    setup.main()
    writes.append(sum(1 for m in calls if m != "GET"))

assert writes[0] > 0, "first run wrote nothing"
assert writes[1] == 0, f"second run wrote {writes[1]} times, expected 0"

wiki = by_marker("llmWikiPart", "wiki")
review = by_marker("llmWikiView", "review")
locks = by_marker("llmWikiPart", "locks")
assert "excludeFromNoteMap" in own(locks["noteId"])
for slug, root in (("graph", wiki), ("review", review)):
    m = by_marker("llmWikiMap", slug)
    assert m["type"] == "noteMap", m
    assert own(m["noteId"])["mapRootNoteId"] == root["noteId"]
for t in ("hub", "summary", "concept", "entity"):
    assert own(by_marker("llmWikiTemplate", t)["noteId"]).get("color"), f"{t} template has no #color"

print(f"ok: first run {writes[0]} writes, second run 0")
