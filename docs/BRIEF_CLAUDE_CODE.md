# BRIEF_CLAUDE_CODE.md — Build the daniel-r.com portfolio site

Read `CLAUDE.md` first; its rules override anything here. Then read every file in the uploads. Start in plan mode: ask the questions in §3 in one batch, propose a plan, and wait for approval before writing files.

## 1. Context and goal

Daniel is a data scientist and project lead at DEPP (Direction de l'évaluation, de la prospective et de la performance), the statistical directorate of the French Ministry of Education. He holds a PhD in economics, has eight-plus years of R, and publishes R packages. He wants a **static portfolio site**: who he is, what he has built, how to reach him. No blog at launch; the architecture must let a blog and other content be added later as separate sites behind redirects.

Audience: French employers and international R consultancies; also peers in the R and applied-economics communities. The site must be readable in under two minutes and every claim must be verifiable through a link.

Reference for structure only (do not copy): https://mustapha-zouari.com/ (hero, timeline, short bio, contact). Quarto references for quality: andrewheiss.com and comparable academic Quarto sites.

## 2. Decisions already taken

| Topic | Decision |
| --- | --- |
| Generator | Quarto, project type `website`, version ≥ 1.6 (needed for `_brand.yml`). Check `quarto --version` and use the latest stable. |
| Hosting | Netlify free tier. Rendering happens in GitHub Actions, not on Netlify (Netlify's build image has neither Quarto nor R). |
| Domain | `daniel-r.com`, canonical host = apex (`https://daniel-r.com`); `www` redirects to apex. Daniel buys the domain and connects it; see §13. |
| Language | English only (UK spelling). French CV as a downloadable PDF. Legal page in French. |
| Repo | Public GitHub repository. Claude Code use is visible and stays visible. |
| Scope at launch | Home, About, Projects (PhD, cryptRopen, scrutr, genproc — all four get pages), Contact, Mentions légales. Nothing else. |
| Future content | Blog, package documentation, talks: separate deployables on subdomains, linked from this site via `301` redirects. This site never hosts churning content. |
| Contacts | Email and phone displayed (assembled client-side), LinkedIn and GitHub highlighted. No postal address. No "open to work". |
| Analytics | None at launch. No cookies, no third-party scripts. |
| Dark mode | Skipped. |
| Timeline | No deadline. Daniel drives the work from Claude Code. |

## 3. Questions to ask Daniel before coding (one batch)

1. Full name and exact current role title, as they should appear on the site. (Confirmed from the cryptRopen repo: name is **Daniel Rakotomalala**, GitHub handle **danielrak** at https://github.com/danielrak. Confirm the role title wording.)
2. LinkedIn URL, ORCID (if any), the email and the phone number to display. (GitHub is https://github.com/danielrak.)
3. Is the domain bought, at which registrar, and does a Netlify account exist?
4. Which CV file is the source of truth for dates and titles (EN or FR)? Any publication or talk to list on About?
5. `cryptRopen`: confirmed public at https://github.com/danielrak/cryptRopen, pkgdown site at https://danielrak.github.io/cryptRopen/, MIT, R-CMD-check and Codecov passing, `cran-comments.md` present (CRAN submission planned, not yet on CRAN as of 3 September 2026). Confirm: is a CRAN submission in progress, and should the page say "planned" or stay silent on CRAN?
6. PhD: title, institution, year of defence, links (theses.fr, HAL, PDF), abstract text to draft from. Daniel may rework this page later; keep it factual and short for now.
7. About page: include a line about growing up in western France and living near Paris, yes or no?
8. Content licence: all rights reserved, or CC BY 4.0 for text? Code in the repo: MIT?
9. Any preference on the two type/colour proposals you will present (§10)?

## 4. Deliverables

1. A Quarto repository that renders with `quarto preview` immediately and `quarto render` with zero warnings.
2. GitHub Actions workflow publishing to Netlify on push to `main`, plus an optional `check.yml` that renders on pull requests.
3. `README.md`: how to run, add a project, add a timeline entry, add a subsite behind a redirect (blog, package docs), how deployment works, how to rotate the Netlify token.
4. `docs/SOURCES.md`: every factual claim on the site mapped to its source (CV section, URL, or "Daniel, answer to Q5").
5. A short handover note: what was not verified, what Daniel still has to do (DNS, Search Console).

## 5. Repository layout

```
/
├── CLAUDE.md
├── README.md
├── LICENSE                      # code licence (Daniel decides, Q8)
├── _quarto.yml
├── _brand.yml
├── _publish.yml                 # created by the first `quarto publish netlify`; committed
├── _redirects                   # Netlify redirects (see §6 and §14)
├── _headers                     # security headers
├── robots.txt
├── index.qmd
├── about.qmd
├── contact.qmd
├── legal.qmd
├── projects/
│   ├── index.qmd                # grid listing
│   ├── phd.qmd
│   ├── cryptropen.qmd           # only if a public link exists
│   ├── scrutr.qmd
│   └── genproc.qmd
├── cv/
│   ├── <Full-Name>-CV-en.pdf
│   └── <Full-Name>-CV-fr.pdf
├── styles/custom.scss
├── includes/
│   ├── head.html                # JSON-LD, extra meta
│   └── contact-links.html       # client-side assembled email/phone
├── assets/
│   ├── profile.jpg
│   ├── favicon.svg
│   ├── og-image.png             # 1200×630
│   └── fonts/                   # self-hosted WOFF2 + licence file
├── docs/
│   ├── SOURCES.md
│   ├── BRIEF_CLAUDE_CODE.md     # this file, moved here after the build
│   └── design.md                # the design plan and what was rejected (§10)
├── .github/workflows/
│   ├── publish.yml
│   └── check.yml
├── .gitignore                   # _site/, .quarto/, .DS_Store
└── _freeze/                     # committed; empty until code chunks exist
```

## 6. URL scheme — permanent

| Path | Page |
| --- | --- |
| `/` | Home |
| `/about/` | About |
| `/projects/` | Projects listing |
| `/projects/<slug>/` | One project; slugs: `phd`, `cryptropen`, `scrutr`, `genproc` |
| `/contact/` | Contact |
| `/legal/` | Mentions légales |
| `/cv/<file>.pdf` | CV downloads |

Reserved for future redirects (never create local pages at these paths):

| Path | Target when it exists |
| --- | --- |
| `/blog/*` | `https://blog.daniel-r.com/:splat` |
| `/<package>/*` | that package's documentation site |
| `/talks/*` | talks site, if ever separate |

Rules: trailing-slash URLs; lower-case slugs; no dates in URLs. A moved page gets `aliases:` in its front matter (Quarto writes a redirect stub) *and* a `301` in `_redirects`.

## 7. Quarto configuration

`_quarto.yml` essentials (adapt syntax to the installed Quarto version; check the docs rather than guess):

- `project.type: website`, `output-dir: _site`, `resources: [_redirects, _headers, robots.txt, cv/*.pdf]`.
- `website`: `title` (full name), `site-url: https://daniel-r.com`, `description` (default meta description), `favicon`, `image` (default Open Graph image), `open-graph: true`, `twitter-card: true`, `search: false`.
- Navbar left: Home, About, Projects, Contact. Navbar right: GitHub and LinkedIn icons with `aria-label`s.
- Footer: `© <year> <Full name>` · link to `/legal/` · GitHub and LinkedIn icons.
- `format.html`: `theme: [<bootstrap base>, styles/custom.scss]` combined with `_brand.yml` (see the Quarto brand docs for the exact way to layer brand and a custom SCSS); `lang: en-GB`; `toc: false`; `anchor-sections: false`; `link-external-newwindow: true`; `include-in-header: includes/head.html`.
- `execute.freeze: auto`.
- The legal page sets `lang: fr` in its own front matter.

`_brand.yml`: the palette and the two type roles (base, headings) from the approved design plan; fonts declared with `source: file` pointing at `assets/fonts/`.

Projects listing (`projects/index.qmd`): Quarto `listing`, `type: grid`, two columns, `fields: [image, title, description, categories]`, sorted by a custom `order` field in each project's front matter.

## 8. Page specifications

All text follows §9. Word counts are ceilings.

**Home (`index.qmd`)**
- Hero: full name; one-line role; a 2–3 sentence introduction (calibration sample in §9); the photo; two primary buttons: GitHub, LinkedIn; two secondary links: About, Projects.
- Timeline: experience and education from the CV, most recent first. Each entry: dates, role, organisation (French name, English gloss), one line on what it involved — only what the CV says. This is a genuine sequence, so dated markers are justified.
- Selected projects: the four project cards, linking to `/projects/<slug>/`.
- Contact strip: email, phone, LinkedIn, GitHub (uses `includes/contact-links.html`).

**About (`about.qmd`)** — 250 words. What he does now and for whom (public facts only); the PhD and how it shaped his interests (causal inference, reproducibility); the R work; optionally the western-France / near-Paris line (Q7); publications and talks if any (Q4); CV download links (EN, FR).

**Projects listing (`projects/index.qmd`)** — one intro sentence, then the grid.

**Project pages** — 150–250 words each, same skeleton: what it is (one paragraph); why it exists (the problem); how it is built (approach, key design choices, stack); status and links (CRAN, GitHub, documentation, DOI); one thing he would change. Sources: for `scrutr`, `genproc` and `cryptRopen`, fetch the GitHub README (and the CRAN page where the package is on CRAN) and rewrite in Daniel's voice — never paste the CRAN or README text verbatim.

**Accuracy note for `cryptRopen`.** The package name and its GitHub tagline say "encryption", but the README is explicit that the operation is a **salted one-way hash for pseudonymisation, not reversible encryption**. On the site, describe it as pseudonymisation / hashing (GDPR-style), following the README's own distinction; do not call it encryption in the prose even though the package keeps that name. Key facts from the README to work from: a single Excel "mask" drives which columns are hashed or dropped per file; `crypt_data()` for an in-session data frame, `crypt_r()` for batch file-driven jobs; parallel via `mirai`, streaming of large CSV/parquet via `arrow`; correspondence tables kept private; MIT licence; author "Daniel Rakotomalala". Front matter: `title`, `description` (the tagline, ≤ 120 characters), `image`, `categories` (for example `R package`, `CRAN`, `PhD`), `order`.

**PhD (`projects/phd.qmd`)** — thesis title, institution, year, supervisor(s) only if Daniel asks for them, a plain-language summary of the question and method, links. Short until Daniel reworks it.

**Contact (`contact.qmd`)** — one sentence; then LinkedIn and GitHub as primary; email and phone assembled client-side with a `<noscript>` fallback written as `name [at] domain [dot] com`; no form.

**Mentions légales (`legal.qmd`)** — French; content in §12.

## 9. Voice and style

Author: a French man in his thirties, from western France, living near Paris, writing English for an international audience. He is neutral by temperament; enthusiasm is real but rationed.

- First person singular. Short sentences. Concrete nouns and verbs. One idea per sentence.
- Enthusiasm shows in specifics, never in adjectives. Budget: at most one sentence per page that says what he likes about the work, and it must name a concrete thing. No exclamation marks.
- Banned words: passionate, thrilled, excited, leverage, cutting-edge, journey, empower, seamless, robust (as praise), innovative, world-class, and any sentence that starts with "I'm a firm believer".
- Every claim points at an artefact: a package, a repository, a publication, a role on a CV. No self-praise without a link.
- UK spelling, but no British idioms or slang: the English should read as clean and international. No Americanisms either (no "awesome", "super").
- Institutional names in French with an English gloss on first use: "DEPP, the statistical directorate of the French Ministry of Education".
- Humour: dry, rare, never at the expense of an employer or a colleague.
- No false modesty and no boasting; state what was done and what it is for.

Calibration sample for the hero (every fact to be checked against the CV before use):

> I'm Daniel, a data scientist and project lead at DEPP, the statistical directorate of the French Ministry of Education, where I lead the IDEE programme, a secure remote data-access platform built with J-PAL Europe. I did a PhD in economics, which is where my interest in causal inference comes from. Most of my code is R, and I write packages that make empirical work easier to check and to reproduce.

Enthusiasm calibration:

- Too much: "I'm passionate about building cutting-edge tools that empower researchers."
- Too flat: "I write R packages."
- Right: "The part I like most is when a check I wrote catches a mistake before it reaches a table."

Third-person text (meta descriptions, JSON-LD) uses "he/his" and the same rules.

## 10. Design

Process: write a design plan in `docs/design.md` before any SCSS — a palette of 4–6 named hex values, the type roles, a one-paragraph layout concept with an ASCII wireframe of the home page, and the one element that carries the identity. Then check the plan against the list below and change what reads as a default. Present two proposals as screenshots; Daniel picks one.

Constraints:
- White background, near-black text, one accent colour with a reason for the choice. Not the cream-plus-terracotta combination, not near-black with an acid accent.
- One or two type families, self-hosted, open licence (SIL OFL or similar), WOFF2, `font-display: swap`. A deliberate type scale; body line length under 80 characters.
- Single column, left-aligned, generous vertical rhythm. Text column about 40–45 rem wide.
- The timeline is the memorable element. Everything else stays quiet.
- No decorative motion. Hover and focus states only; respect `prefers-reduced-motion`.
- Avoid the generic tells: all-caps eyebrow labels, numbered markers outside the timeline, identical rounded cards with the same grey shadow, gradients as decoration, a "→" appended to links, middle-dot meta strings.
- Responsive to 360 px wide; the timeline becomes a stacked list on mobile.
- Accessibility: WCAG 2.1 AA contrast; visible focus rings; skip link; correct heading order; alt text on every image; keyboard-navigable navbar.
- Photo: the current file is 243 × 315 px, too small for a hero at high-density screens. Display it at 150 CSS px or less until Daniel supplies a version of at least 800 px on the short side. Set `width` and `height` attributes; no lazy loading on the hero image.
- Favicon: SVG monogram from the initials. Open Graph image: 1200 × 630, name and role, same palette, generated from an SVG in the repo.
- Page weight under 500 KB, no render-blocking external requests.

## 11. SEO and metadata

- `site-url` set; sitemap is generated by Quarto; `robots.txt` allows everything and points at the sitemap.
- Every page has a `title` and a `description` (≤ 160 characters) in its front matter.
- Canonical link on every page: Quarto's `canonical-url` option if the installed version supports it, otherwise a `<link rel="canonical">` in `includes/head.html`.
- Open Graph and Twitter card defaults from `_quarto.yml`; per-page `image` where it helps.
- JSON-LD `Person` in `includes/head.html`: `name`, `jobTitle`, `affiliation` (DEPP), `url`, `sameAs` (LinkedIn, GitHub, ORCID). Nothing not stated on the site.
- Daniel's tasks after launch: verify the domain in Google Search Console (DNS TXT) and submit the sitemap; put the site URL on his GitHub and LinkedIn profiles.

## 12. Legal — required content

French law (LCEN, article 6-III) requires a personal, non-professional site to publish at least the host's identity: name, address and telephone number. Daniel displays his own identity anyway, so the page states:

1. Éditeur du site: full name, email (assembled client-side as elsewhere).
2. Directeur de la publication: full name.
3. Hébergeur: Netlify's current legal name, postal address and telephone — fetch them from Netlify's own legal pages at build time and record the URL in `SOURCES.md`; never write them from memory.
4. Données personnelles: the site sets no cookies, loads no third-party scripts and collects no personal data; contact details sent by email are used only to reply; a sentence on the visitor's rights under the RGPD with the contact email.
5. Propriété intellectuelle: the text licence chosen in Q8; the code licence; a note that third-party logos are not used.

Footer link text: "Mentions légales". Page `lang: fr`.

## 13. Deployment

1. Local: `quarto render` clean. Commit.
2. GitHub: create the public repository, push `main`.
3. Netlify: run `quarto publish netlify` once from the local machine (creates the site and `_publish.yml`; commit the file). Do not link the Netlify site to the repository for builds; GitHub Actions does the publishing.
4. Secrets: `NETLIFY_AUTH_TOKEN` (personal access token from Netlify) as a repository secret. Follow the current Quarto documentation page "Publishing → Netlify → Publish Action" for the workflow; use `quarto-dev/quarto-actions` (`setup`, then `publish` with `target: netlify`). Fetch that page and copy the inputs it specifies rather than reconstructing them.
5. `check.yml` (optional): on pull requests, `quarto render` only.
6. Redirects and headers: `_redirects` and `_headers` live at the project root and are copied into `_site/` through `project.resources`. Netlify reads them from the publish directory whatever the deploy method; do not rely on `netlify.toml` for redirects with API-based publishing. `_headers` sets `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY`, and a `Content-Security-Policy` compatible with the inline contact script (use a nonce or a hash, or move the script to a file).
7. Domain: Daniel adds `daniel-r.com` as a custom domain in Netlify and either delegates DNS to Netlify DNS or sets the records Netlify displays. HTTPS is automatic. Set the apex as primary so `www` redirects to it.
8. Verification after first deploy: `curl -I https://daniel-r.com/`, `https://www.daniel-r.com/` (301), `/about` (redirects to `/about/`), a deliberately wrong URL (404 page renders), and the response headers.

## 14. Future subsites — the pattern

The showcase links; it does not host. Each new kind of content is its own repository and deploy:

| Content | Where it lives | Wiring in this repo |
| --- | --- | --- |
| Blog | New Quarto blog project, its own Netlify site, `https://blog.daniel-r.com`, same `_brand.yml` (copied) | `_redirects`: `/blog/* https://blog.daniel-r.com/:splat 301`; navbar item "Blog"; RSS link in footer |
| Package docs | pkgdown in each package repo, GitHub Pages, optional custom subdomain `<pkg>.daniel-r.com` via a `CNAME` file and a DNS CNAME | `_redirects`: `/<pkg>/* <docs URL>/:splat 301`; project card links to the docs |
| Talks, slides | Quarto revealjs decks in a `talks` repo, or a static list on this site if rare | decide when the first one exists |

Redirect type: `301`, not a `200` proxy. The SEO gain of a subdirectory is negligible for a personal site and proxying breaks asset paths and canonicals. Consistency across sites comes from `_brand.yml` and a shared footer, not from shared hosting. Document this pattern in `README.md` with the exact commands.

## 15. Execution order

1. Read `CLAUDE.md`, this brief, the uploads. Plan mode. Ask §3 in one message.
2. Design plan in `docs/design.md`; two screenshot proposals; wait for Daniel's pick.
3. Scaffold: `_quarto.yml`, `_brand.yml`, SCSS, fonts, includes, `_redirects`, `_headers`, `robots.txt`, `.gitignore`, workflows. First deploy to the Netlify preview URL.
4. Content: Home, About, Contact, Legal, with `docs/SOURCES.md` filled as you go.
5. Projects: listing plus the four pages (or three plus a mention, per Q5).
6. Metadata: descriptions, Open Graph image, JSON-LD, canonical links.
7. Quality pass: Lighthouse on mobile (performance, accessibility, best practices, SEO all ≥ 95), keyboard walk-through, screenshots at 360 / 768 / 1280 px.
8. Domain and DNS with Daniel; verification list in §13.8.
9. Handover: `README.md`, `docs/SOURCES.md`, move this brief to `docs/`, list of unverified items and of Daniel's remaining tasks.

## 16. Definition of done

- `quarto render` completes with zero warnings; `_site/` is not committed; `_freeze/` is.
- Every date, title, link and legal detail on the site appears in `docs/SOURCES.md` with a source.
- No "open to work", no postal address, no third-party logo, no external script or font.
- Lighthouse mobile scores ≥ 95 on all four categories on Home and one project page.
- `https://daniel-r.com/` serves over HTTPS; `www` and `/about` (no slash) redirect correctly; the 404 page renders in the site's design.
- `README.md` lets Daniel add a project, a timeline entry and a subsite without asking anyone.
- Commit history reads like Daniel's other repositories; Claude-related files and trailers are intact.
