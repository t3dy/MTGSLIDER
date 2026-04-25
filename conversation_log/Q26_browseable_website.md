# Q26 — Browseable website for documentation, code, slideshows, content

## Verbatim user input

> create a website I can use to browse our documentation and code and slide show or other created content

## How I interpreted it

A static HTML site that indexes everything in the repo: docs (writing/, root-level .md), code (source tree), slideshows (98 .pptx files), historical-trip cards, conversation log. No framework — pure Python generator producing flat HTML/CSS readable from `file://` and ready for GitHub Pages.

Per the user's `Claudiens/AFSTYLING.md` aesthetic (warm parchment, dark brown serif body, burnt-sienna accents — the "scholarly site" register), I'm using a similar palette so it feels like part of their family of sites rather than a generic Bootstrap theme.

This pairs naturally with the in-flight Q22 work — the historical-trip cards land in the database AND get rendered by the site. Shipping both together as one commit.

## What I built

- [tools/build_site.py](../tools/build_site.py) — deterministic site generator. Walks the repo and writes `site/` with index page, docs index, decks index (linking to .pptx), historical-trips browser, conversation-log archive, code-tree view.
- [site/](../site/) — generated output (gitignored except for committed artifacts; preview-only locally; can be GitHub-Pages-deployed by a follow-up commit if user wants)
- Site styling drawn from `Claudiens/AFSTYLING.md` (warm parchment + serif body + burnt sienna)

## What I deferred

- Wiring up GitHub Pages deployment (one more commit when user requests)
- Search functionality (deferred to a sprint when content corpus warrants it)
- Card-image embedding in historical-trip pages (the data is in MTGSLIDER's DB; rendering can be a follow-up)
