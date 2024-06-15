import sys
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse

def add(url: str):
    with open("./data.json", "r") as reader:
        data: list = json.load(reader)
    urls = set()
    for d in data:
        urls.add(d["url"])
    if url in urls:
         if input("url already in dataset, enter y to continue:").strip() != "y":
             exit()

    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    resp = requests.get(url, proxies=proxies, timeout=10)

    content_type = resp.headers.get('Content-Type')
    if 'charset' in content_type:
        charset = content_type.split('charset=')[-1]
    else:
        charset = 'utf-8'
    resp.encoding = charset

    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find('title').text
    title = title.split(" - ")[0].strip()
    title = title.split(" | ")[0].strip()
    icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
    if icon_link and 'href' in icon_link.attrs:
        icon_url = icon_link['href']
        icon_url = urllib.parse.urljoin(url, icon_url)
        if len(icon_url) > 100:
            icon_url = ""
    else:
        icon_url = urllib.parse.urljoin(url, "/favicon.ico")
    
    info = {
        "url": url,
        "title": title,
        "icon": icon_url
    }
    print(info)

    data.append(info)
    with open("./data.json", "w") as writer:
        json.dump(data, writer, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit
    add(sys.argv[1])
