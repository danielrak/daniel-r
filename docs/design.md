# Design plan

Written before any SCSS, as the brief (§10) asks. Seven proposals were rendered as static mock-ups with the real CV entries and self-hosted fonts, screenshotted at 1280 px and 360 px, and shown to Daniel. He chose proposal F on 4 September 2026. The other six are listed at the end with the reason they were set aside.

## Palette

| Name | Hex | Role | Contrast on white |
| --- | --- | --- | --- |
| paper | `#FFFFFF` | page background | – |
| ink | `#1F1F1F` | text, headings | 16.5:1 |
| muted | `#5C5C5C` | organisation lines, tags, footer text | 6.7:1 |
| rule | `#D0D3D8` | hairlines, borders | decorative only |
| band | `#F2F4F7` | project panels, footer band | ink on band 15.1:1, muted on band 6.1:1 |
| navy | `#1F3D7A` | the one accent: links, buttons, dates, section rules | 10.5:1; white on navy 10.5:1 |

Why navy: Daniel asked for an institutional register, close to the sites of statistical institutes and ministries. Those sites use a dark blue and a light grey band, and readers already read dark blue as "official". The value is deliberately not the French State's blue, so the site does not borrow the State's identity. Contrast ratios were computed with the WCAG 2.1 formula; every text pair clears AA, and the accent clears AAA.

## Type

Two families, both SIL Open Font License 1.1, self-hosted as WOFF2 from the Fontsource packages (version 5.3.0), `latin` subset, which already covers French accented capitals and œ.

| Role | Family | Files | Size |
| --- | --- | --- | --- |
| body text | Source Serif 4 | 400, 400 italic | 40 KB |
| headings, navigation, dates, labels, buttons | Source Sans 3 | 400, 600, 700 | 47 KB |
| code, package names | system monospace stack | none | 0 |

Scale (base 17 px, ratio about 1.2 with hand-set steps): body 1rem / line-height 1.6; small labels 0.9375rem; h3 1.125rem; h2 1.375rem; h1 2.25rem / 1.15. Measure: content column 44 rem wide, which gives 70 to 78 characters per line at body size. Serif body with sans headings is the pairing of most French institutional reports; the serif carries the reading, the sans does the signposting.

## Layout

One column, left-aligned, 44 rem wide, generous vertical rhythm (sections separated by 3.5 rem). The header is a white bar with a 3 px navy rule on its top edge and a hairline under it; name on the left, four links and two icons on the right. Sections open with a short navy rule above the heading. Project cards sit on the light grey band with a navy top rule; no shadow, no rounding; the whole card is a link. The contact strip is a ruled line holding the email and the phone. The footer is a full-width grey band.

```
+---------------------------------------------------------------+  <- 3px navy rule
| Daniel Rakotomalala        Home  About  Projects  Contact  GH LI |
+---------------------------------------------------------------+  <- hairline
|                                                                 |
|  Daniel Rakotomalala                              [photo 120px] |
|  Data scientist and project lead, DEPP                          |
|  Three sentences of introduction in serif ...                   |
|                                                                 |
|  ----                                                           |
|  Experience and education                                       |
|  ---------------------------------------------------------------|
|  since 2024  | Data scientist and IDEE project lead              |
|              | DEPP, ... (organisation, muted)                   |
|              | One line on what it involved.                    |
|  ---------------------------------------------------------------|
|  2022 - 2024 | Data manager, IDEE programme                     |
|  ...         | ...                                              |
|                                                                 |
|  ----                                                           |
|  Selected projects                                              |
|  +-- navy rule -----------+  +-- navy rule -----------+         |
|  | scrutr                 |  | genproc                |         |
|  | one sentence           |  | one sentence           |         |
|  | R package, CRAN        |  | R package, CRAN        |         |
|  +------------------------+  +------------------------+         |
|  +------------------------+  +------------------------+         |
|  | cryptRopen             |  | PhD thesis             |         |
|  +------------------------+  +------------------------+         |
|                                                                 |
|  ---------------------------------------------------------------|
|  Email  x [at] y   Phone  +33 ...                               |
|  ---------------------------------------------------------------|
+=================================================================+
|  (c) 2026 Daniel Rakotomalala    Mentions legales        GH LI  |  <- grey band
+=================================================================+
```

## The identity element

The timeline. It is drawn as a ruled table: a left column of navy dates in the sans, a vertical hairline, then the role, the organisation in muted grey and one line of fact. Rows are separated by hairlines. Nothing else on the site uses this construction, so it is what a visitor remembers. Below 48 rem the columns stack: date above the role, hairlines kept, vertical rule dropped.

## Motion and states

No decorative motion. Links thicken their underline on hover; a project card darkens slightly and its title underlines; focus rings are 3 px navy with a 3 px offset, drawn around the whole card where the card is the link. Transitions of 150 ms on colour only, and none at all under `prefers-reduced-motion: reduce`.

## Checked against the list of defaults in the brief

- No all-caps eyebrow labels: section titles are sentence case with a rule above.
- No numbered markers outside the timeline; the timeline itself uses dates, not numbers.
- No identical rounded cards with grey shadows: the project panels have square corners, a flat band colour and a top rule.
- No gradients, no arrows appended to links, no middle-dot meta strings (tags are comma-separated).
- Photo displayed at 120 CSS px from a 243 × 315 px file until a larger one exists; `width` and `height` set; no lazy loading.
- Responsive to 360 px; verified on the mock-up.

## Proposals rendered and set aside

| Proposal | Type and accent | Timeline | Why set aside |
| --- | --- | --- | --- |
| A | Source Sans 3 only, blue `#1D5FAE` | spine with dots | Reads as a generic Bootstrap site once the accent is removed. |
| B | Source Serif 4 headings, green `#14664B` | ruled rows, large years | Editorial rather than institutional. |
| C | IBM Plex Sans, Plex Mono labels, teal `#0B5F5F` | ledger rows, square markers | Technical register, not institutional. |
| D | Newsreader headings, Public Sans body, dark red `#8F3527` | hairline spine, serif years | Editorial; red reads as warning on an official-looking page. |
| E | Hanken Grotesk, violet `#553C9A` | tick markers, dark contact strip | Start-up register. |
| G | Source Sans 3, navy `#1F3D7A`, full navy header band | grey date cells | Same family as F, heavier; Daniel preferred the white header of F. |

The mock-ups live outside the repository; the screenshots were sent to Daniel in the session of 4 September 2026.

## Changed after the first review, 4 September 2026

Daniel's own list, applied the same day. The wireframe and the notes above already reflect these.

- The hero row of buttons (GitHub, LinkedIn, About, Projects) is gone: the navbar and the footer carried the same four destinations.
- The contact strip keeps the email and the phone only, for the same reason.
- The timeline's open-ended date reads "since 2024" rather than "2024 –".
- A project card is clickable over its whole surface, through a stretched link on the title, so the title stays the link's accessible name.
- The Projects page carries a visually hidden second-level heading, so that the card headings do not skip a level.
