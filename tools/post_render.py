#!/usr/bin/env python3
"""Post-render pass over the Quarto output directory.

Run by Quarto after every render (project.post-render in _quarto.yml). Only
the output directory is touched; the sources never change. Four jobs:

1. Content-Security-Policy hashes. Quarto writes a few inline scripts into
   every page. Their SHA-256 hashes replace the placeholder
   QUARTO_INLINE_SCRIPT_HASHES in _site/_headers, so script-src can stay
   'self' plus hashes. Non-executable script types (JSON, JSON-LD) are
   skipped because the policy does not apply to them.

2. Directory URLs. The URL scheme uses trailing slashes (/about/, never
   /about/index.html). Quarto links pages as .../index.html and lists them so
   in sitemap.xml; both are rewritten to the directory form.

3. No dark theme. Quarto 1.10 generates a dark variant of the theme whenever
   a _brand.yml exists and links it from every page. The site has no dark
   mode (brief §2), so the dark Bootstrap stylesheet, the dark syntax
   highlighting stylesheet and the duplicate light link are removed. That
   saves about 500 KB per page before compression and clears a duplicate
   id="quarto-text-highlighting-styles" that the two highlighting links
   would otherwise share.

4. listings.json next to listed pages. Quarto's listing script fetches
   listings.json relative to the current page, which 404s on project pages;
   a copy is placed in each folder that a listing links to.

5. Two small fixes to Quarto's output: the navbar toggler's inline onclick, which
   the Content-Security-Policy forbids and which drives a headroom feature
   the site does not use (navbar pinned: false), and the "/./" prefix Quarto
   writes on the 404 page's root-relative links.
"""

import base64
import hashlib
import json
import os
import posixpath
import re
import shutil
import sys

OUTPUT_DIR = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site")
PLACEHOLDER = "QUARTO_INLINE_SCRIPT_HASHES"
SCRIPT_RE = re.compile(r"<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.S)
NON_EXEC_TYPES = ("application/json", "application/ld+json", "text/template")
HREF_RE = re.compile(r'(?P<attr>href|content)="(?P<url>[^"]*?)index\.html(?P<rest>[#?][^"]*)?"')
DARK_LINK_RE = re.compile(
    r'\s*<link[^>]*(?:bootstrap-dark-[^"]*\.css'
    r'|quarto-syntax-highlighting-dark-[^"]*\.css'
    r'|quarto-color-scheme-extra)[^>]*>',
    re.S,
)
DARK_FILE_PREFIXES = ("bootstrap-dark-", "quarto-syntax-highlighting-dark-")
TOGGLER_ONCLICK_RE = re.compile(r'\s*onclick="if \(window\.quartoToggleHeadroom\)[^"]*"')
# Quarto writes the 404 page's root-relative links as href="/./about/" and the
# site root as href="/.". Both are valid but neither is the URL scheme.
DOT_SLASH_RE = re.compile(r'href="/\.(?P<tail>/|")')
LOC_RE = re.compile(r"<loc>([^<]*?)index\.html</loc>")


def html_files():
    for root, _dirs, files in os.walk(OUTPUT_DIR):
        for name in files:
            if name.endswith(".html"):
                yield os.path.join(root, name)


def inline_script_hashes(html):
    for match in SCRIPT_RE.finditer(html):
        attrs, body = match.group("attrs"), match.group("body")
        if "src=" in attrs or not body.strip():
            continue
        if any(t in attrs for t in NON_EXEC_TYPES):
            continue
        digest = hashlib.sha256(body.encode("utf-8")).digest()
        yield "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


def directory_url(page_dir, url):
    """Turn a relative or absolute link to .../index.html into a root-relative
    directory URL. page_dir is the page's directory relative to OUTPUT_DIR."""
    if url.startswith(("http://", "https://")):
        return url  # absolute: only the trailing index.html is dropped
    if url.startswith("/"):
        return url
    joined = posixpath.normpath(posixpath.join("/" + page_dir, url))
    return joined if joined.endswith("/") else joined + "/"


def rewrite_links(path, html):
    page_dir = os.path.relpath(os.path.dirname(path), OUTPUT_DIR).replace(os.sep, "/")
    page_dir = "" if page_dir == "." else page_dir + "/"

    def repl(match):
        url, rest = match.group("url"), match.group("rest") or ""
        if url.startswith(("http://", "https://")) and "daniel-r.com" not in url:
            return match.group(0)
        target = directory_url(page_dir, url)
        if target == "//":
            target = "/"
        return f'{match.group("attr")}="{target}{rest}"'

    return HREF_RE.sub(repl, html)


def main():
    hashes = set()
    listing_targets = set()
    for path in html_files():
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        hashes.update(inline_script_hashes(html))
        new_html = DARK_LINK_RE.sub("", html)
        new_html = TOGGLER_ONCLICK_RE.sub("", new_html)
        new_html = DOT_SLASH_RE.sub(lambda m: 'href="/' + ('' if m.group("tail") == "/" else '"'), new_html)
        new_html = rewrite_links(path, new_html)
        if new_html != html:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_html)

    # 1. CSP hashes
    headers_path = os.path.join(OUTPUT_DIR, "_headers")
    if os.path.exists(headers_path):
        with open(headers_path, encoding="utf-8") as fh:
            text = fh.read()
        if PLACEHOLDER in text:
            text = text.replace(PLACEHOLDER, " ".join(sorted(hashes)))
            with open(headers_path, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"post_render: {len(hashes)} inline script hash(es) written to _headers")

    # 2. sitemap
    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    if os.path.exists(sitemap_path):
        with open(sitemap_path, encoding="utf-8") as fh:
            xml = fh.read()
        xml = LOC_RE.sub(r"<loc>\1</loc>", xml)
        with open(sitemap_path, "w", encoding="utf-8") as fh:
            fh.write(xml)
        print("post_render: sitemap URLs use directory form")

    # 3. dark theme files
    for sub in ("bootstrap", "quarto-html"):
        lib_dir = os.path.join(OUTPUT_DIR, "site_libs", sub)
        if not os.path.isdir(lib_dir):
            continue
        for name in os.listdir(lib_dir):
            if name.endswith(".css") and name.startswith(DARK_FILE_PREFIXES):
                os.remove(os.path.join(lib_dir, name))
                print(f"post_render: removed {name}")

    # 4. listings.json next to listed pages
    listings_path = os.path.join(OUTPUT_DIR, "listings.json")
    if os.path.exists(listings_path):
        with open(listings_path, encoding="utf-8") as fh:
            listings = json.load(fh)
        for listing in listings:
            for item in listing.get("items", []):
                target_dir = os.path.join(OUTPUT_DIR, os.path.dirname(item.lstrip("/")))
                if os.path.isdir(target_dir) and os.path.abspath(target_dir) != os.path.abspath(OUTPUT_DIR):
                    listing_targets.add(target_dir)
        for target_dir in sorted(listing_targets):
            shutil.copy(listings_path, os.path.join(target_dir, "listings.json"))
        print(f"post_render: listings.json copied to {len(listing_targets)} folder(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
