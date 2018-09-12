import json
import urllib.request
import os
from ._utils import download_url, retrieve_url

domain = "danbooru.donmai.us"
images_per_page = 20


def format_tags(tags):
    return "+".join(tags)


def get_max_page(tags):
    raise NotImplementedError("Can't be implemented")


def download_page(tags, folder, page, amount):
    url = "https://{}/posts.json?tags={}&page={}".format(
        domain, format_tags(tags), page
    )
    print(url)
    page = download_url(url)
    posts = json.loads(page)
    downloaded_amount = 0
    for i, post in enumerate(posts):
        if downloaded_amount > amount:
            break
        if "file_url" not in post:
            print(
                "You need a gold account to see this image.",
                "(https://{}/posts/{})".format(domain, post["id"])
            )
            continue
        retrieve_url(
            post["file_url"],
            os.path.join(folder, post["md5"] + "." + post["file_ext"])
        )
        downloaded_amount += 1
    return downloaded_amount


def download(tags, folder, amount):
    if amount is None:
        amount = float("inf")

    downloaded_amount = 0
    current_page = 1
    while downloaded_amount < amount:
        downloaded_amount += download_page(
            tags,
            folder,
            current_page,
            amount - downloaded_amount
        )
        current_page += 1
