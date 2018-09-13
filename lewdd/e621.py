import os
import xml.etree.ElementTree
import math
from ._utils import *
from .danbooru import format_tags

domain = "e621.net"
images_per_page = 75


def get_max_page(tags):
    url = "https://{}/post/index.xml?&tags={}&limit=0".format(
        domain,
        format_tags(tags)
    )
    page = download_url(url)
    posts = xml.etree.ElementTree.fromstring(page)
    return math.ceil(int(posts.get("count")) / images_per_page)


def download_page(tags, folder, page, amount):
    url = "https://{}/post/index.xml?&tags={}&page={}".format(
        domain,
        format_tags(tags),
        page
    )
    page = download_url(url, silent=False)
    posts = xml.etree.ElementTree.fromstring(page)
    downloaded_amount = 0
    for post in posts:
        if downloaded_amount >= amount:
            break
        file_url = post.find("file_url").text
        retrieve_url(
            file_url,
            os.path.join(folder, get_filename(file_url))
        )
        downloaded_amount += 1
    return downloaded_amount


def download(tags, folder, amount):
    if amount is None:
        amount = float("inf")

    downloaded_amount = 0
    max_page = get_max_page(tags)
    current_page = 1
    while downloaded_amount < amount and current_page < max_page:
        downloaded_amount += download_page(
            tags,
            folder,
            current_page,
            amount - downloaded_amount
        )
        current_page += 1
