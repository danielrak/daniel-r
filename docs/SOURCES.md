# Sources of every factual claim on the site

Rule 1 of `CLAUDE.md`: every date, title, employer, publication, package version, URL and legal detail on the site comes from a document Daniel uploaded, a page actually fetched, or an answer Daniel gave. This file maps each claim to its source. "Answer, 4 Sep 2026" means an answer Daniel gave in the Claude Code session of that day. "CV" means the uploaded file `CV_2026__Daniel_R.pdf`, dated 3 August 2026, kept as `cv/Daniel-Rakotomalala-CV-fr.pdf`. Repository facts carry the commit they were read at.

## Identity and contacts

| Claim | Where used | Source |
| --- | --- | --- |
| Name "Daniel Rakotomalala" | everywhere | CV; `Authors@R` in the DESCRIPTION files of cryptRopen, scrutr, genproc; answer, 4 Sep 2026 |
| Role line "Data scientist and project lead, DEPP" | hero, JSON-LD `jobTitle` | CV ("Data scientist, chef de projet IDEE"); wording confirmed by answer, 4 Sep 2026 |
| Email rakdanielh@gmail.com | contact strip, contact page | CV; answer, 4 Sep 2026 |
| Phone +33 7 82 50 10 67 | contact strip, contact page | CV ("+ 33 782 50 10 67"); display format confirmed by answer, 4 Sep 2026 |
| LinkedIn https://www.linkedin.com/in/daniel-r-807192134 | navbar, footer, hero, JSON-LD | Drive file `CV_Daniel_RAKOTOMALALA_Appsilon_EN.docx` (12 May 2026); confirmed by answer, 4 Sep 2026; not fetched (host blocked) |
| GitHub https://github.com/danielrak | navbar, footer, hero, JSON-LD | CV; repositories fetched |
| ORCID https://orcid.org/0000-0003-1260-1084 | JSON-LD `sameAs` | answer, 4 Sep 2026; not fetched |
| Photo | hero, Open Graph fallback | Drive file `Photo_Daniel_Rakotomalala_IDEE.png`, 243 × 315 px, named by Daniel; converted to JPEG |
| Affiliation "DEPP, Direction de l'évaluation, de la prospective et de la performance, Ministère de l'Éducation nationale" | JSON-LD, timeline | CV |
| "Université de La Réunion" as alma mater | JSON-LD, timeline | CV |

## Hero paragraph

| Claim | Source |
| --- | --- |
| Data scientist and project lead at DEPP, the statistical directorate of the French Ministry of Education | CV; gloss from the brief §9 |
| The data project I work on is IDEE, Innovations, Données et Expérimentations en Éducation, a programme on innovations, data and experiments in education | CV ("Chef de projet Innovations, Données et Expérimentations en Education (IDEE)"); wording written by Daniel, answer of 4 Sep 2026, second wave |
| Link https://www.idee-education.fr/ on the word IDEE | CV (hyperlink on "IDEE"); not fetched (host not tried from the build environment) |
| PhD in economics; interest in causal inference | CV (Doctorat en sciences économiques; "Evaluation des politiques publiques / évaluation d'impact : essais randomisés contrôlés, appariement, doubles différences, variables instrumentales, régressions sur une discontinuité"); sentence from the brief's calibration sample |
| Most code in R; packages that make empirical work easier to check and reproduce | CV ("Niveau avancé sur R – plus de 8 ans"); scrutr and genproc DESCRIPTION files |

## Timeline

| Entry | Source |
| --- | --- |
| Since 2024, Data scientist and IDEE project lead, DEPP; project lead for the IDEE programme in partnership with J-PAL Europe; statistical tooling and strategic large-scale data work; statistical studies; technical training | CV ("depuis 2024"; "Chef de projet IDEE"; "Outillage statistique pour la DEPP"; "Traitements statistiques à grande échelle"; "Etude statistique, en collaboration avec le Ministère de la Justice"; "Formateur technique pour la DEPP : modélisation statistique"); wording written by Daniel, answer of 4 Sep 2026, second wave |
| 2022–2024 Data manager, IDEE programme, J-PAL Europe and DEPP; administrative-data track; public data catalogue; secure remote-access platform | CV ("Data manager / Ingénieur statisticien pour le programme IDEE – CDD 2022 à 2024", "Responsable du volet « données administratives »", "Catalogue public des données", "Plateforme sécurisée d'accès à distance") |
| Link https://catalogue.depp.education.fr/index.php/home on "public data catalogue" | CV (hyperlink on "Catalogue public des données"); not fetched |
| 2021–2022 Teaching assistant in statistics and mathematics, Université de La Réunion; undergraduate courses; exercise-generating programs | CV ("Chargé d'enseignements en statistiques et en mathématiques – 2021 à 2022", "L1 AES ... L1 Economie-Gestion", "programmes générant automatiquement des exercices"). The ATER contract is in the CV but Daniel asked for it to be left off the site (answer, 4 Sep 2026, second wave). |
| 2020–2021 Statistical studies and evaluation officer, Pôle emploi Réunion; effect of employment services on return to work | CV ("Chargé d'études statistiques et d'évaluation – 2020 à 2021", "Direction régionale Pôle emploi Réunion", "Mesure quantitative de l'impact des services ... sur le retour à l'emploi"). The cohort count is omitted on purpose: the French CV says 15 and the English CV 14. |
| 2018–2022 PhD in economics, Université de La Réunion, supervised by Yves Croissant | CV; supervisor named by answer, 4 Sep 2026 |
| Thesis subject shown as "Determinants of educational performance in La Réunion" | **Translation**, by Claude Code, of the CV's own subject line "déterminants des performances éducatives à La Réunion". It is **not** the title registered on theses.fr, which could not be fetched (host blocked) and which Daniel has not yet supplied. An earlier version of this file wrongly attributed a French title to an answer Daniel never gave; that title has been removed. Replace this line with the registered title as soon as it is available. |
| Thesis record https://theses.fr/2022LARE0044 | CV link; answer, 4 Sep 2026 (the Drive English CV says 2022LARE0055, set aside); not fetched (host blocked) |
| 2016–2017 Master's in applied economics, quantitative methods (MQME), Université de La Réunion; top of the class | CV ("Master 2 en Economie appliquée – option méthodes quantitatives et modélisation pour l'entreprise (MQME)", "Major de promotion, mention bien"); the years come from the Drive English CV and the April 2026 French CV, not from the August PDF |

## Projects

| Claim | Source |
| --- | --- |
| scrutr: R package for scrutinising collections of structured datasets; inspect, compare schemas, convert many tables | `DESCRIPTION` Title "Scrutinizing Collections of Structured Datasets" and `README.md` at danielrak/scrutr commit efa1eab |
| scrutr on CRAN, version 0.3.1 | CRAN mirror github.com/cran/scrutr, `DESCRIPTION` (`Repository: CRAN`, `Date/Publication: 2026-04-25`) |
| scrutr links: CRAN page, GitHub, documentation site | README badges and `_pkgdown.yml` at commit efa1eab; CRAN page not fetched (host blocked) |
| genproc: turns one-off iterative procedures into logged, reproducible, parallel, non-blocking runs | `DESCRIPTION` and `README.md` at danielrak/genproc commit 734991a |
| genproc on CRAN, version 0.2.0, lifecycle experimental | CRAN mirror github.com/cran/genproc, `DESCRIPTION` (`Date/Publication: 2026-05-12`); README lifecycle badge |
| cryptRopen: pseudonymises variables across datasets with a salted one-way hash driven by an Excel mask; not on CRAN; submission planned | `DESCRIPTION`, `README.md`, `NEWS.md` ("Submission to CRAN is planned once the package has been validated on production workloads") at danielrak/cryptRopen commit 21fa725; no cran/cryptRopen mirror on 3 Sep 2026; wording confirmed by answer, 4 Sep 2026 |
| PhD card: age at exams, peer effects, a maths revision platform | Drive file `Daniel R - CV expertise R.pdf` (4 Apr 2026), chapter list; use authorised by answer, 4 Sep 2026 |
| Code licence MIT; text and photo all rights reserved | answer, 4 Sep 2026 |

## Site metadata and legal

| Claim | Source |
| --- | --- |
| Site URL https://daniel-r.com | brief §2; domain not yet bought (answer, 4 Sep 2026) |
| Fonts Source Serif 4 and Source Sans 3 under SIL OFL 1.1 | `LICENSE` files in the Fontsource packages `@fontsource/source-serif-4@5.3.0` and `@fontsource/source-sans-3@5.3.0`, copied to `assets/fonts/` |
| Netlify legal identity for the legal page | not yet obtained; netlify.com was blocked in the build environment; to be fetched once the network policy allows it |

## Not verified

- LinkedIn, ORCID, theses.fr and CRAN pages could not be fetched from the build environment; the URLs come from the CV and Daniel's answers.
- The pkgdown documentation sites at danielrak.github.io were not fetched; their existence is inferred from the `gh-pages` branches and `_pkgdown.yml` files.
