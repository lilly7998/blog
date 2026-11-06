#!/usr/bin/env python3
"""Generate post audio (zh/en, Edge TTS) and podcast RSS feeds.
Usage: python3 podcast/build.py [slug ...]   (no slug = only missing audio)
Scripts: podcast/scripts/<slug>.zh.txt / .en.txt ; metadata: podcast/episodes.json
"""
import asyncio, json, os, re, subprocess, sys, datetime, email.utils, html
import edge_tts
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE="https://wyz.name"
VOICES={"zh":"zh-CN-YunxiNeural","en":"en-US-AndrewNeural"}
for k in ['HTTPS_PROXY','https_proxy','HTTP_PROXY','http_proxy','ALL_PROXY','all_proxy']: os.environ.pop(k,None)
meta=json.load(open(f"{ROOT}/podcast/episodes.json"))
def post_date(slug):
    fm=open(f"{ROOT}/content/posts/{slug}/index.md").read().split('---')[1]
    d=re.search(r'^date:\s*(\S+)',fm,re.M).group(1)
    return datetime.datetime.fromisoformat(d)
def duration(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode())
async def tts(text,voice,out):
    await edge_tts.Communicate(text,voice).save(out)
force=set(sys.argv[1:])
for slug in meta:
    for lang,voice in VOICES.items():
        out=f"{ROOT}/content/posts/{slug}/audio-{lang}.mp3"
        src=f"{ROOT}/podcast/scripts/{slug}.{lang}.txt"
        if os.path.exists(src) and (slug in force or not os.path.exists(out)):
            print("tts",slug,lang); asyncio.run(tts(open(src).read(),voice,out))
CH={"zh":dict(title="Andy 的博客 · 声音版",desc="Andy 的博客文章朗读版：欧洲政治、能源与地缘。由 AI 语音合成。",lang="zh-cn",cat="News",sub="Politics"),
    "en":dict(title="Andy's Blog (English Audio)",desc="English audio editions of Andy's blog on European politics, energy and geopolitics. Translated and read by AI voices.",lang="en",cat="News",sub="Politics")}
for lang,c in CH.items():
    items=[]
    for slug,m in sorted(meta.items(),key=lambda kv:post_date(kv[0]),reverse=True):
        f=f"{ROOT}/content/posts/{slug}/audio-{lang}.mp3"
        if not os.path.exists(f): continue
        dur=int(duration(f)); url=f"{BASE}/posts/{slug}/audio-{lang}.mp3"
        t=m[f"{lang}_title"]; s=m[f"{lang}_summary"]
        items.append(f"""  <item>
   <title>{html.escape(t)}</title>
   <description>{html.escape(s)} {BASE}/posts/{slug}/</description>
   <link>{BASE}/posts/{slug}/</link>
   <guid isPermaLink="false">wyz-{slug}-{lang}</guid>
   <pubDate>{email.utils.format_datetime(post_date(slug))}</pubDate>
   <enclosure url="{url}" length="{os.path.getsize(f)}" type="audio/mpeg"/>
   <itunes:duration>{dur}</itunes:duration>
   <itunes:explicit>false</itunes:explicit>
   <itunes:episodeType>full</itunes:episodeType>
  </item>""")
    feed=f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:podcast="https://podcastindex.org/namespace/1.0">
 <channel>
  <title>{html.escape(c['title'])}</title>
  <link>{BASE}/</link>
  <atom:link href="{BASE}/podcast/{lang}.xml" rel="self" type="application/rss+xml"/>
  <language>{c['lang']}</language>
  <description>{html.escape(c['desc'])}</description>
  <itunes:summary>{html.escape(c['desc'])}</itunes:summary>
  <itunes:author>Andy</itunes:author>
  <itunes:image href="{BASE}/podcast/cover.jpg"/>
  <image><url>{BASE}/podcast/cover.jpg</url><title>{html.escape(c['title'])}</title><link>{BASE}/</link></image>
  <itunes:category text="{c['cat']}"><itunes:category text="{c['sub']}"/></itunes:category>
  <itunes:explicit>false</itunes:explicit>
  <itunes:type>episodic</itunes:type>
  <copyright>© 2026 Andy</copyright>
{chr(10).join(items)}
 </channel>
</rss>
"""
    os.makedirs(f"{ROOT}/static/podcast",exist_ok=True)
    open(f"{ROOT}/static/podcast/{lang}.xml","w").write(feed); print("feed",lang,len(items))
