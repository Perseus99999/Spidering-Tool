# 🕷️ Keyword Spider

<div align="center">

**A compact, quick, agile URL spider** — start from one page, discover links, and recursively print only the URLs that contain your keyword.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python\&logoColor=white)](#requirements)
[![Requests](https://img.shields.io/badge/Powered%20by-requests-000000.svg)](https://docs.python-requests.org/)
[![BeautifulSoup](https://img.shields.io/badge/HTML%20Parsing-BeautifulSoup4-4B8BBE.svg)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

</div>

> Minimal reference utility and fast URL filter. Not intended for large-scale crawling.

---

## ✨ Features

* **Keyword-filtered recursion** — follows and prints only URLs whose absolute address contains your keyword (case-insensitive).
* **Absolute URL normalization** — resolves relative `href`s with `urljoin` and strips `#fragments` to reduce duplicates.
* **De-duplication** — tracks visited pages in an in-memory `set`.
* **Resilient fetching** — timeouts, redirects followed, browser-like User-Agent.
* **Depth control** — `max_depth` prevents runaway crawls.

---

## 📚 Table of Contents

* [Requirements](#-requirements)
* [Quickstart](#-quickstart)
* [Usage](#-usage)
* [Configuration](#-configuration)
* [Full Script](#-full-script)
* [Troubleshooting](#-troubleshooting)
* [Limitations](#-limitations)
* [Extensions](#-extensions)
* [Contributing](#-contributing)
* [License](#-license)

---

## 🔧 Requirements

* **Python**: 3.8+
* **Packages**:

  * `requests`
  * `beautifulsoup4`

Install:

```bash
pip install -U requests beautifulsoup4
```

Optional `requirements.txt`:

```txt
requests>=2.0
beautifulsoup4>=4.9
```

Then:

```bash
pip install -r requirements.txt
```

---

## 🚀 Quickstart

```bash
python spider.py
```

```text
Enter the URL you want to scrape.
https://en.wikipedia.org/wiki/Programmer
Enter the keyword to search for in the URL provided.
wiki
https://en.wikipedia.org/wiki/Computer_programmer
https://en.wikipedia.org/wiki/Programming_language
...
[Done] scanned 37 pages; printed 12 matching URLs.
```

> **Input tips**
>
> * You can enter a bare domain like `example.com`; the script adds `https://` if missing.
> * Keyword matching is case-insensitive.

---

## 🛠️ Usage

The script is interactive. It asks for:

* **Start URL** (string; `https://` will be added if missing)
* **Keyword** (case-insensitive substring; e.g., `news`, `wiki`, `about`)

---

## ⚙️ Configuration

Adjust these values in the call at the bottom of the script:

```python
spider_urls(start, kw, session=s, max_depth=4, verbose=False)
```

| Option       | Type   | Default | Description                                                           |
| ------------ | ------ | ------- | --------------------------------------------------------------------- |
| `max_depth`  | int    | `4`     | Maximum recursion depth.                                              |
| `verbose`    | bool   | `False` | `True` prints progress lines (`[Fetch]`, `[Parse]`, `[Skip]`).        |
| `User-Agent` | string | Chrome  | Browser-like header set on the `requests.Session()` for fewer blocks. |

---

## 🧪 Troubleshooting

> [!TIP]
> **No output?**
>
> * Enable `verbose=True` to see `[Skip] ... (HTTP 403/429/999)` or other hints.
> * Try a broader keyword like `/`.
> * Some sites block bots; the default UA mimics a browser to help.

> [!WARNING]
> **Be polite.** Avoid high request rates and respect terms of service.

---

## 📌 Limitations

* No `robots.txt` checks.
* No rate limiting or retry/backoff adapter.
* Domain scoping is off by default.
* Results are printed to stdout (no file output).

---

## 🔭 Extensions

* **Domain scope (stay on host)**

  ```python
  from urllib.parse import urlparse
  start_host = urlparse(start).netloc

  # inside the loop, after computing `absolute`
  if urlparse(absolute).netloc != start_host:
      continue
  ```

* **Rate limit**: insert `time.sleep(0.2)` between requests.

* **Output to file**: write matches to CSV/JSON instead of `print`.

* **Retries**: attach an `HTTPAdapter` with backoff to the `Session`.

---

## 🤝 Contributing

Improvements to reliability (timeouts, retries), safety (robots.txt, rate limiting), and ergonomics (CLI flags for depth, domain, keyword) are welcome. Please keep examples minimal and add tests where practical.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

## 📄 License
Released under the **MIT License**. See `LICENSE` for details.

