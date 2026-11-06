#!/usr/bin/env python3
"""Verify every reference by identifier before it goes in the report.

refs.tsv columns (tab separated):  key <TAB> claimed title <TAB> id
  id is  arxiv:2602.17753  or  doi:10.xxxx/yyyy
Exit 1 if any id does not resolve or its title does not match the claimed one.
Network required; use --offline to only validate the file format.
"""
from __future__ import annotations
import difflib, json, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "swarm-sprint-refcheck/0.1"}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def title_arxiv(i: str) -> str | None:
    url = "http://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(i)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        root = ET.fromstring(r.read())
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = root.find("a:entry", ns)
    t = e.find("a:title", ns) if e is not None else None
    return " ".join(t.text.split()) if t is not None and t.text else None


def title_doi(d: str) -> str | None:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        t = json.load(r)["message"].get("title") or []
    return t[0] if t else None


def main(path: str, offline: bool) -> int:
    bad = 0
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 3 or not re.match(r"^(arxiv|doi):\S+$", parts[2]):
            print(f"line {ln}: BAD FORMAT"); bad += 1; continue
        key, claimed, ident = parts
        if offline:
            print(f"{key}: format ok"); continue
        kind, val = ident.split(":", 1)
        try:
            actual = title_arxiv(val) if kind == "arxiv" else title_doi(val)
        except Exception as e:  # noqa: BLE001
            print(f"{key}: UNRESOLVED ({type(e).__name__}: {e})"); bad += 1; continue
        if not actual:
            print(f"{key}: NOT FOUND {ident}"); bad += 1; continue
        ratio = difflib.SequenceMatcher(None, norm(claimed), norm(actual)).ratio()
        if ratio < 0.85:
            print(f"{key}: TITLE MISMATCH ({ratio:.2f})\n   claimed: {claimed}\n   actual:  {actual}"); bad += 1
        else:
            print(f"{key}: ok ({ratio:.2f})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "refs.tsv",
                  "--offline" in sys.argv))
