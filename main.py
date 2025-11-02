#https://en.wikipedia.org/wiki/Programmer

#Beginner Examples
"""import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    #print(soup.a) #Returns the first anchor tag
    #print(soup.find_all("a")) #Grab all anchor tags, ".find" grabs the first one
    #print(soup.find(id="mw-searchButton"))# replace with any tag
    #print(soup.title.string)#Title of the Page in string

    tag = soup.find_all("a")

    for t in tag:
        url2 =t.get("href")
        print(url2)

get_page(input("What url would you like to scrape?\n "))"""

#-------------------------------------------------------------------------------------------

# Keyword Spider


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()
matches = 0

def ensure_scheme(u: str) -> str:
    u = u.strip()
    if not u.startswith(("http://", "https://")):
        return "https://" + u
    return u

def is_href_ok(href: str) -> bool:
    if not href:
        return False
    href = href.strip()
    if href.startswith(("#", "javascript:", "mailto:", "tel:")):
        return False
    return True

def spider_urls(url, keyword, *, session=None, depth=0, max_depth=3, verbose=False):
    global matches
    url = ensure_scheme(url)

    if url in visited_urls or depth > max_depth:
        return
    visited_urls.add(url)

    if session is None:
        session = requests.Session()
        session.headers.update({
            # many sites block default Python UA; this looks like a real browser
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })

    if verbose:
        print(f"[Fetch] depth={depth} {url}")

    try:
        resp = session.get(url, timeout=10, allow_redirects=True)
    except requests.RequestException as e:
        print(f"[Error] {url} -> {e}")
        return

    if resp.status_code != 200:
        print(f"[Skip ] {url} (HTTP {resp.status_code})")
        return

    soup = BeautifulSoup(resp.content, "html.parser")
    anchors = soup.find_all("a")
    if verbose:
        print(f"[Parse] {len(anchors)} links on {resp.url}")

    for a in anchors:
        href = a.get("href")
        if not is_href_ok(href):
            continue

        # use resp.url (post-redirect) as the base for urljoin
        absolute = urljoin(resp.url, href)

        # strip fragments so /page#a and /page#b dedupe
        p = urlparse(absolute)
        absolute = p._replace(fragment="").geturl()

        if absolute in visited_urls:
            continue

        if keyword.lower() in absolute.lower():
            print(absolute)  # <-- your matches
            matches += 1
            spider_urls(absolute, keyword, session=session,
                        depth=depth + 1, max_depth=max_depth, verbose=verbose)

if __name__ == "__main__":
    start = input("Enter the URL you want to scrape.\n").strip()
    kw = input("Enter the keyword to search for in the URL provided.\n").strip()
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    })
    spider_urls(start, kw, session=s, max_depth=4, verbose=False)
    print(f"[Done] scanned {len(visited_urls)} pages; printed {matches} matching URLs.")
