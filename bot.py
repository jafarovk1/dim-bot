import os, re, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://dim.gov.az/az/metbuat/xeberler"
KEYWORDS = ["qeydiyyat", "keçir", "dövlət qulluğ"]   # istədiyin sözləri bura əlavə et
SEEN = "seen.txt"

def send(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": text}, timeout=15)

r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

news = {}
for a in soup.find_all("a", href=True):
    link = urljoin(URL, a["href"])
    title = a.get_text(strip=True)
    if "/az/metbuat/xeberler/" in link and title:
        news[link] = title

first_run = not os.path.exists(SEEN)
seen = set(open(SEEN, encoding="utf-8").read().split()) if not first_run else set()

for link, title in news.items():
    if link not in seen:
        if not first_run and (any(k in title.lower() for k in KEYWORDS) or re.search(r"\bbb\b", title.lower())):
            send(f"{title}\n{link}")
        seen.add(link)

open(SEEN, "w", encoding="utf-8").write("\n".join(seen))
