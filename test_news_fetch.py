# -*- coding: utf-8 -*-
import os
import sys
import re
import html
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import requests

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def search_news_rss(query, lang='en'):
    try:
        clean_q = re.sub(r'[^\w\s]', '', query).strip()
        encoded = urllib.parse.quote(f'"{clean_q}"')
        url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            items = root.findall('.//item')
            results = []
            for it in items[:5]:
                title = it.find('title').text if it.find('title') is not None else ''
                desc = it.find('description').text if it.find('description') is not None else ''
                source = it.find('source').text if it.find('source') is not None else 'News'
                # Clean html tags from desc
                clean_desc = re.sub(r'<[^>]+>', '', desc)
                clean_desc = html.unescape(clean_desc)
                results.append({
                    'title': html.unescape(title),
                    'snippet': clean_desc,
                    'source': source
                })
            return results
    except Exception as e:
        print(f"RSS error for {query}: {e}")
    return []

if __name__ == '__main__':
    for term in ['keep in the loop', 'lead time', 'red carpet']:
        res = search_news_rss(term)
        print(f"Query: '{term}' -> {len(res)} results")
        for r in res[:2]:
            print(f"  [{r['source']}] {r['title']}")
            print(f"    {r['snippet'][:120]}...")
