# Q28 — Deploy the website to GitHub Pages

## Verbatim user input

> let's deploy the website

(With Q27 = the truncated `;et` precursor.)

## How I interpreted it

Deploy `site/` to GitHub Pages. Two design choices:

1. **Branch + folder source** — would require the site to live at `/` or `/docs`. We'd have to rename `site/` → `docs/` (and update `tools/build_site.py` to write there). Cheap but conflates "the deployable site folder" with the "documentation source folder" naming convention.
2. **GitHub Actions source** — uploads `site/` as an artifact on every push to `main`. More flexible (can keep the folder named whatever we like, can run preprocessing steps, can deploy on demand). Adds one workflow file.

Picked **#2**. Reasons: (a) keeps `site/` as the natural name; (b) the workflow re-runs automatically when `site/` changes, so the user never has to remember to re-deploy after `python tools/build_site.py`; (c) standard GitHub-recommended pattern for Pages in 2026.

## What I built

- [.github/workflows/pages.yml](../.github/workflows/pages.yml) — workflow that uploads `site/` as the Pages artifact and deploys
- Enabled Pages on the repo with `source: workflow` via `gh api`
- Pushed the workflow; the first deployment runs automatically

## What I deferred

- Custom domain (none requested)
- Branch protection on `main` (out of scope)
- Pre-deploy validation (broken-link check, HTML lint) — could be added to the workflow later if pages start breaking
