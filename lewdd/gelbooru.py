import os
import xml.etree.ElementTree
import math
from ._utils import *
from .danbooru import format_tags
from .rule34_xxx import images_per_page


domain = "gelbooru.com"
images_per_page = 20

_api_url = "https://" + domain + "/index.php?page=dapi&s=post&q=index"


def get_max_page(tags):
    url = _api_url + "&tags={}&limit=0".format(format_tags(tags))
    page = download_url(url)
    posts = xml.etree.ElementTree.fromstring(page)
    return math.ceil(int(posts.get("count")) / images_per_page)


def download_page(tags, folder, page, amount):
    url = _api_url + "&tags={}&pid={}".format(format_tags(tags), page - 1)
    page = download_url(url, silent=False)
    posts = xml.etree.ElementTree.fromstring(page)
    downloaded_amount = 0
    for post in posts:
        if downloaded_amount >= amount:
            break
        file_url = post.get("file_url")
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
    current_page = 1
    while downloaded_amount < amount:
        downloaded_amount += download_page(
            tags,
            folder,
            current_page,
            amount - downloaded_amount
        )
        current_page += 1
