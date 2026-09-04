# daniel-r.com

Personal site of Daniel Rakotomalala. A [Quarto](https://quarto.org) website, rendered by GitHub Actions and published to Netlify. The standing rules for anyone editing it are in `CLAUDE.md`; the build brief is in `docs/BRIEF_CLAUDE_CODE.md`; the design plan is in `docs/design.md`; every fact on the site is traced in `docs/SOURCES.md`.

## Run it locally

1. Install Quarto 1.10.18 or later from the Quarto download page. No R, Python or LaTeX is needed: the site has no code chunks.
2. From the repository root:

```sh
quarto preview      # development server with live reload
quarto render       # full build into _site/ (never committed)
```

`quarto render` must finish with zero warnings before a commit. The post-render script `tools/post_render.py` runs automatically at the end of every render and needs Python 3.

## Layout

| Path | Content |
| --- | --- |
| `_quarto.yml` | project, navigation, footer, HTML format options |
| `_brand.yml` | palette and typography (Quarto brand file) |
| `styles/custom.scss` | the only stylesheet: fonts, header, timeline, cards, footer |
| `index.qmd` | Home: hero, timeline, selected projects, contact strip |
| `about/index.qmd`, `contact/index.qmd`, `legal/index.qmd` | About, Contact, Mentions légales |
| `projects/index.qmd` | listing of the project pages |
| `projects/<slug>/index.qmd` | one page per project |
| `404.qmd` | the not-found page, in the site's design |
| `includes/head.html` | preload links, JSON-LD, the contact script tag |
| `includes/contact-links.html` | the contact strip; email and phone are assembled by `assets/contact.js` |
| `assets/` | photo, favicon, Open Graph image (SVG source and PNG), fonts |
| `cv/` | CV PDFs |
| `_redirects`, `_headers`, `robots.txt` | Netlify files, copied into `_site/` through `project.resources` |
| `tools/post_render.py` | runs after each render: CSP hashes, directory URLs, no dark theme, `listings.json` copies (see "After each render") |
| `docs/` | brief, design plan, sources; not rendered |

Pages live in folders named after their URL because the URL scheme uses trailing slashes (`/about/`, `/projects/scrutr/`): Netlify serves `/about/` from `about/index.html`, and Quarto writes `about/index.qmd` to exactly that path.

## The URL scheme is permanent

`/`, `/about/`, `/projects/`, `/projects/<slug>/`, `/contact/`, `/legal/`, `/cv/<file>.pdf`. To move a page, add `aliases: [/old-path/index.html]` to its front matter (Quarto writes a redirect stub) and a `301` line in `_redirects`. Never remove a URL silently. `/blog/*`, `/talks/*` and `/<package>/*` are reserved for redirects to future sub-sites; do not create pages there.

## Add a project

1. Create `projects/<slug>/index.qmd` with a lower-case slug and this front matter:

```yaml
---
title: "Package name"
description: "One sentence of at most 120 characters; it is the card text and the meta description."
categories: [R package, CRAN]
order: 5
canonical-url: https://daniel-r.com/projects/<slug>/
---
```

2. `order` decides the position in the grid on Home and on the Projects page (ascending). Keep the four sections of the other project pages: what it is, why it exists, how it is built, status and links, one thing to change.
3. Add the sources of every fact to `docs/SOURCES.md`.
4. `quarto render`, check the two grids, commit.

## Add a timeline entry

In `index.qmd`, inside `::: {.timeline}`, entries are ordered most recent first. Copy this block:

```markdown
::: {.timeline-entry}
::: {.when}
2026 –
:::
::: {.what}
### Role title {.unnumbered .unlisted}
[Organisation in French, English gloss on first use]{.org}

One line on what it involved, taken from the CV.
:::
:::
```

Dates use an en dash with spaces (`2022 – 2024`; `2024 –` for a current position).

## Add a sub-site behind a redirect

The site links to other content; it does not host it (brief §14). Each new kind of content gets its own repository and deploy.

1. Create the new project (for a blog: `quarto create project blog`), copy `_brand.yml` into it so the look matches, and publish it to its own Netlify site.
2. In Netlify, give the new site the subdomain, for example `blog.daniel-r.com` (Domain management → Add domain alias; if Netlify DNS is used, the record is created for you; otherwise add a CNAME `blog` → the site's `netlify.app` host at the registrar).
3. In this repository, add a redirect line to `_redirects`, before the catch-all comments:

```
/blog/*  https://blog.daniel-r.com/:splat  301
```

4. Add a navbar item in `_quarto.yml` (`website.navbar.left`) pointing at `https://blog.daniel-r.com/`, and, for a blog, an RSS link in the footer.
5. `quarto render`, commit, push to `main`; the redirect is live with the next deploy.

Package documentation follows the same pattern with pkgdown sites: the redirect targets `https://danielrak.github.io/<pkg>/` (or a custom subdomain set through a `CNAME` file in the package repository plus a DNS CNAME). The commented lines in `_redirects` show the exact syntax.

## How deployment works

- Every push to `main`, and every manual run from the Actions tab, runs `.github/workflows/publish.yml`: it installs Quarto 1.10.18, renders the site and runs `quarto publish netlify`, which uploads `_site/` to the Netlify site identified in `_publish.yml`. Netlify does not build anything; it only serves the files.
- Every pull request runs `.github/workflows/check.yml`: a render, failing on any warning.
- `_publish.yml` holds the Netlify site id and its `netlify.app` URL (no secret). It is created once, either by running `quarto publish netlify` locally or by hand from the site id shown in Netlify's site settings.
- The token that lets the action deploy is the repository secret `NETLIFY_AUTH_TOKEN`.
- `_redirects` and `_headers` are read by Netlify from the published directory, so redirects and headers change with a normal push.

### Rotate the Netlify token

1. In Netlify: user settings → Applications → Personal access tokens → New access token. Name it after the repository and the date; copy it.
2. In GitHub: repository Settings → Secrets and variables → Actions → `NETLIFY_AUTH_TOKEN` → Update secret; paste the new token.
3. Run the "Quarto Publish" workflow by hand from the Actions tab and check that it deploys.
4. Back in Netlify, delete the old token.

### After each render

`tools/post_render.py` (declared as `project.post-render` in `_quarto.yml`, Python 3, no dependencies) edits the output directory only:

1. Content-Security-Policy hashes. Quarto writes a few inline scripts into every page, so `script-src` lists their SHA-256 hashes next to `'self'`; the script computes them and writes them into `_site/_headers` in place of the placeholder `QUARTO_INLINE_SCRIPT_HASHES`. Nothing to do by hand after a Quarto upgrade.
2. Directory URLs. Links that Quarto writes as `.../index.html`, and the entries of `sitemap.xml`, are rewritten to the `/about/` form of the URL scheme. `_redirects` also sends the `index.html` forms to the directory form.
3. No dark theme. Quarto 1.10 generates a dark variant of the theme whenever `_brand.yml` exists; the site has none, so the file and its links are removed (about 500 KB per page before compression).
4. `listings.json` is copied next to each listed project page, because Quarto's script requests it relative to the page.

### Security headers

`_headers` sets `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy` and the `Content-Security-Policy`. Scripts are allowed from this origin plus the hashes above; styles keep `'unsafe-inline'` because Quarto sets inline style attributes; images allow `data:` for Quarto's inline SVG icons; everything else is `'self'`.

## Fonts

Source Serif 4 (body) and Source Sans 3 (headings, navigation, dates), SIL Open Font License 1.1, taken from the Fontsource packages `@fontsource/source-serif-4@5.3.0` and `@fontsource/source-sans-3@5.3.0` (`files/*-latin-*.woff2`). The licence files sit next to the fonts in `assets/fonts/`. To add a weight, copy the WOFF2 from the package, list it in `_brand.yml` and add the matching `@font-face` in `styles/custom.scss`.

## Yearly maintenance

The footer year is written in `_quarto.yml` (`page-footer.left`). Update it in January.

## Licences

Code: MIT (see `LICENSE`). Text, photograph and CV: © Daniel Rakotomalala, all rights reserved. Fonts: SIL OFL 1.1.
