Keyword Spider

A compact, quick, agile web spider that starts from a single URL, discovers links on each page, and recursively prints URLs that contain a user-supplied keyword. It normalizes links to absolute form, uses a browser-like User-Agent, and caps recursion depth for safety.

Status: Minimal reference utility and fast URL filter. Not intended for large-scale crawling.

Features

Keyword-filtered recursion — follows and prints only URLs whose absolute address contains your keyword (case-insensitive).

Absolute URL normalization — resolves relative hrefs with urljoin and strips #fragments to reduce duplicates.

De-duplication — tracks visited pages in an in-memory set.

Resilient fetching — timeouts, redirects followed, browser-like User-Agent.

Depth control — max_depth prevents runaway crawls.

Requirements

Python: 3.8+

Packages:

requests

beautifulsoup4

Install:

pip install -U requests beautifulsoup4


Optional requirements.txt:

requests>=2.0
beautifulsoup4>=4.9


Then:

pip install -r requirements.txt

Usage

Run the script and answer two prompts:

python spider.py


Example session:

Enter the URL you want to scrape.
https://en.wikipedia.org/wiki/Programmer
Enter the keyword to search for in the URL provided.
wiki
https://en.wikipedia.org/wiki/Computer_programmer
https://en.wikipedia.org/wiki/Programming_language
...
[Done] scanned 37 pages; printed 12 matching URLs.


Input notes

You can enter a bare domain like example.com; the script adds https:// if missing.

Keyword match is case-insensitive (e.g., news, wiki, about).

Config tweaks (inline)

Adjust these in the __main__ call:

spider_urls(start, kw, session=s, max_depth=4, verbose=False)


max_depth: recursion limit (default 4).

verbose: set True for progress logs ([Fetch], [Parse], [Skip], errors).

To stay on one site, see Extensions.

Code layout
spider.py
├─ ensure_scheme()  # Adds https:// to bare domains
├─ is_href_ok()     # Skips mailto:, javascript:, tel:, fragments, empties
├─ spider_urls()    # Core DFS: fetch → parse → filter → print → recurse
└─ __main__         # Interactive prompts + Session (User-Agent)

Troubleshooting

Nothing prints

The site might return non-200 (403/429/999). Re-run with verbose=True to see [Skip] ... (HTTP ...).

The keyword doesn’t appear in any absolute URL. Test with a broader keyword like / or try a different start page.

The site blocks programmatic clients. Keep the default User-Agent or rotate it.

It crawls too deep/fast

Lower max_depth, add a tiny delay (time.sleep(0.3)), or add a page counter.

Limitations

No robots.txt checks.

No rate limiting or retry/backoff adapter.

Domain scoping is off by default.

Results are printed to stdout (no file output).

This is intentional to keep the tool compact.

Ethical use

Respect site Terms of Service and robots.txt.

Be gentle: low request rates, no excessive crawling.

Avoid collecting personal data.

Get permission for restricted or large crawls.

Extensions (quick adds)

Domain scope — keep the crawl on the starting host:

from urllib.parse import urlparse
start_host = urlparse(start).netloc

# inside the loop, after computing `absolute`
if urlparse(absolute).netloc != start_host:
    continue


Rate limit — insert time.sleep(0.2) between requests.
Output to file — append matches to CSV/JSON instead of print.
Retries — use HTTPAdapter with backoff on the Session.
