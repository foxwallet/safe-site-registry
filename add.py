import sys
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse

def add(url: str):
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    resp = requests.get(url, proxies=proxies)

    content_type = resp.headers.get('Content-Type')
    if 'charset' in content_type:
        charset = content_type.split('charset=')[-1]
    else:
        charset = 'utf-8'

    resp.encoding = charset
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find('title').text
    icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
    if icon_link and 'href' in icon_link.attrs:
        icon_url = icon_link['href']
        icon_url = urllib.parse.urljoin(url, icon_url)
    else:
        icon_url = ""
    
    info = {
        "url": url,
        "title": title,
        "icon": icon_url
    }
    print(info)

    with open("./data.json", "r") as reader:
        data: list = json.load(reader)
    data.append(info)
    with open("./data.json", "w") as writer:
        json.dump(data, writer, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit
    add(sys.argv[1])
