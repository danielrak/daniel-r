# CLAUDE.md — daniel-r.com

Personal portfolio site of Daniel (full name as on the CV): data scientist and project lead at DEPP, PhD in economics, author of R packages. Quarto website, published to Netlify by GitHub Actions. Daniel directs the work from Claude Code. This file holds the standing rules for every session. The one-off build task is `BRIEF_CLAUDE_CODE.md` (kept in `docs/` after the build).

## Non-negotiables

1. **No invented facts.** Every date, title, employer, publication, package version, URL, address and legal detail comes from Daniel's uploaded documents, from a page you have actually fetched, or from Daniel's answer to a question. If something is missing, ask; never fill the gap with a plausible value. Record the source of each factual claim in `docs/SOURCES.md`.
2. **Employer discretion.** DEPP, the ministry and the IDEE programme: use only information that is already public (official pages, publications, Daniel's CV). Nothing about internal data, projects, tools or people.
3. **No job-seeking signals.** No "open to work" badge, no availability line, nothing that reads as a job advert. The site is a portfolio.
4. **Personal data.** Phone and email are displayed on purpose (Daniel's decision) but assembled client-side so scrapers do not get them. Never publish a postal address. Strip address and date of birth from any CV placed on the site.
5. **URL scheme is permanent** once live (see `BRIEF_CLAUDE_CODE.md` §6). Renaming a page requires an `aliases:` entry in its front matter or a rule in `_redirects`; never a silent break.
6. **Static only.** No JS frameworks, no CDN-hosted fonts or scripts, no analytics, no third-party embeds unless Daniel asks. Fonts are self-hosted.
7. **`execute: freeze: auto` stays on.** Commit `_freeze/`; never commit `_site/`.
8. **Do not delete or hide evidence of Claude Code use** (this file, the brief, co-author trailers). Write commits in Daniel's style; do not disguise them.

## Language

- Site copy, comments, docs, commit messages: UK English (organise, programme, colour, licence as a noun). Institutional names stay in French with an English gloss on first use.
- The voice rules in `BRIEF_CLAUDE_CODE.md` §9 apply to every text change, not only the initial build.

## Git conventions

- Before the first commit, inspect the `git log` of Daniel's public repos (`scrutr`, `genproc`; ask for the URLs) and mirror their subject length, mood and capitalisation. Defaults if unclear: imperative subject of at most 60 characters, sentence case, no emoji, no scope prefix, body only when the *why* is not obvious.
- `main` is deployable at all times. Work on short-lived branches named `<area>-<what>` (`home-timeline`, `seo-jsonld`, `legal-page`). Merge strategy is Daniel's call; ask once.
- One logical change per commit. `quarto render` must complete with zero warnings before any commit.

## Commands

| Command | Use |
| --- | --- |
| `quarto preview` | local development server |
| `quarto render` | full build into `_site/` |
| `quarto publish netlify` | first publication only; creates `_publish.yml`, which is committed |
| GitHub Actions (`.github/workflows/publish.yml`) | renders and publishes on every push to `main` |

## Where things live

| Path | Content |
| --- | --- |
| `_quarto.yml`, `_brand.yml` | project config; colours and typography |
| `index.qmd`, `about/index.qmd`, `contact/index.qmd`, `legal/index.qmd`, `404.qmd` | top-level pages; each page sits in the folder of its URL so that `/about/` is served from `about/index.html` (decided with Daniel, 4 Sep 2026) |
| `projects/index.qmd`, `projects/<slug>/index.qmd` | listing page plus one folder per project |
| `styles/custom.scss` | the only stylesheet |
| `includes/` | `head.html` (metadata, JSON-LD), `contact-links.html` (obfuscated contacts, filled by `assets/contact.js`) |
| `assets/` | photo, favicon, Open Graph image, self-hosted fonts |
| `cv/` | CV PDFs (FR at launch; EN when one exists) |
| `_redirects`, `_headers`, `robots.txt` | copied into `_site/` via `project.resources` |
| `tools/post_render.py` | post-render script: CSP hashes into `_site/_headers`, directory URLs in links and sitemap, removal of Quarto's dark theme, `listings.json` copies (README, "After each render") |
| `docs/` | `SOURCES.md`, the brief, `design.md`; excluded from rendering |

## Working with Daniel

- Structural changes (config, navigation, URL scheme, deployment, design system): plan mode first, present the plan, wait for approval.
- Content changes: make them, show the diff, list any fact you could not verify.
- Missing fact, file or credential: stop and ask, all questions batched.
- Questions go through the interactive question dialog (AskUserQuestion), one item per question, the proposed answer as the first option plus a free-text field, batches of at most four; never a numbered list of questions in prose (Daniel's request, 4 Sep 2026).
- Report in at most ten lines. Do not summarise what Daniel already knows.
