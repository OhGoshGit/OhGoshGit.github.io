"""Post new RSS items to Bluesky.

Environment variables:
    BSKY_HANDLE              Bluesky handle (e.g. ohgoshgit.bsky.social)
    BSKY_APP_PASSWORD        App Password from https://bsky.app/settings/app-passwords
    RSS_URL                  Feed URL (default: https://ohgoshgit.github.io/index.xml)
    UPDATE_WITHIN_MINUTES    Only consider items published this recently (default: 1500)
    POST_TEMPLATE            Format string with {title} and {url} (default: 'New Post: "{title}" {url}')
    DRY_RUN                  If "1", print what would be posted without actually posting
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone

import feedparser
import requests
from atproto import Client, client_utils, models
from bs4 import BeautifulSoup

RSS_URL = os.environ.get("RSS_URL", "https://ohgoshgit.github.io/index.xml")
UPDATE_WITHIN_MINUTES = int(os.environ.get("UPDATE_WITHIN_MINUTES", "1500"))
POST_TEMPLATE = os.environ.get("POST_TEMPLATE", 'New Post: "{title}" {url}')
DRY_RUN = os.environ.get("DRY_RUN") == "1"
RECENT_POSTS_TO_CHECK = 100


def fetch_recent_items() -> list[dict]:
    feed = feedparser.parse(RSS_URL)
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=UPDATE_WITHIN_MINUTES)
    items = []
    for entry in feed.entries:
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        if not published:
            continue
        published_dt = datetime(*published[:6], tzinfo=timezone.utc)
        if published_dt < cutoff:
            continue
        items.append(
            {"title": entry.title, "url": entry.link, "published": published_dt}
        )
    items.sort(key=lambda x: x["published"])
    return items


def already_posted_urls(client: Client, handle: str, limit: int) -> set[str]:
    posted: set[str] = set()
    cursor: str | None = None
    fetched = 0
    while fetched < limit:
        params = {"actor": handle, "limit": min(50, limit - fetched)}
        if cursor:
            params["cursor"] = cursor
        resp = client.app.bsky.feed.get_author_feed(params)
        for item in resp.feed:
            record = item.post.record
            for facet in getattr(record, "facets", None) or []:
                for feat in facet.features:
                    uri = getattr(feat, "uri", None)
                    if uri:
                        posted.add(uri)
            embed = getattr(item.post, "embed", None)
            external = getattr(embed, "external", None) if embed else None
            if external is not None:
                posted.add(external.uri)
        fetched += len(resp.feed)
        cursor = resp.cursor
        if not cursor or not resp.feed:
            break
    return posted


def fetch_link_card(client: Client, url: str):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception as e:
        print(f"  warn: could not fetch URL for card: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    def og(prop: str) -> str:
        tag = soup.find("meta", property=prop)
        return (tag.get("content") if tag else "") or ""

    title = og("og:title") or (soup.title.string.strip() if soup.title and soup.title.string else url)
    desc = og("og:description")
    image_url = og("og:image")

    thumb_blob = None
    if image_url:
        try:
            img_resp = requests.get(image_url, timeout=10)
            img_resp.raise_for_status()
            thumb_blob = client.upload_blob(img_resp.content).blob
        except Exception as e:
            print(f"  warn: could not upload thumbnail: {e}", file=sys.stderr)

    external = models.AppBskyEmbedExternal.External(
        uri=url, title=title, description=desc, thumb=thumb_blob
    )
    return models.AppBskyEmbedExternal.Main(external=external)


def build_post_text(title: str, url: str):
    text = POST_TEMPLATE.format(title=title, url=url)
    if url not in text:
        return client_utils.TextBuilder().text(text)
    before, _, after = text.partition(url)
    return client_utils.TextBuilder().text(before).link(url, url).text(after)


def main() -> int:
    handle = os.environ["BSKY_HANDLE"]
    password = os.environ["BSKY_APP_PASSWORD"]

    client = Client()
    client.login(handle, password)

    items = fetch_recent_items()
    print(f"feed: {RSS_URL}")
    print(f"window: last {UPDATE_WITHIN_MINUTES} minute(s)")
    print(f"candidate items: {len(items)}")
    if not items:
        return 0

    posted = already_posted_urls(client, handle, RECENT_POSTS_TO_CHECK)
    new_count = 0
    for item in items:
        if item["url"] in posted:
            print(f"  skip (already posted): {item['title']}")
            continue
        if DRY_RUN:
            print(f"  DRY_RUN would post: {item['title']} -> {item['url']}")
            new_count += 1
            continue
        text = build_post_text(item["title"], item["url"])
        embed = fetch_link_card(client, item["url"])
        client.send_post(text=text, embed=embed)
        print(f"  posted: {item['title']}")
        new_count += 1

    print(f"done. new posts: {new_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
