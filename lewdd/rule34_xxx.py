import re
import os
import bs4
from ._utils import *
from .danbooru import format_tags

domain = "rule34.xxx"
images_per_page = 42


def get_max_page(tags):
    url = "https://{}/index.php?page=post&s=list&tags={}".format(
        domain,
        format_tags(tags)
    )
    page = download_url(url)
    soup = bs4.BeautifulSoup(page, features="html.parser")

    paginator = soup.find("div", attrs={"class": "pagination"})
    last = paginator.find_all("a")[-1]["href"].rsplit("=", 1)[1]
    return int(last)


def _original_image(soup):
    sidebar = soup.find("div", {"class": "sidebar"})
    options = sidebar.findChildren("div")[4]
    original = options.find_all("li")[2]
    if original.a["href"] == "#":  # no "resize image"
        original = options.find_all("li")[1]
    return original.a["href"]


def download_page(tags, folder, page, amount):
    url = "https://{}/index.php?page=post&s=list&tags={}&pid={}".format(
        domain, format_tags(tags), images_per_page * (page - 1)
    )
    page = download_url(url, silent=False)
    soup = bs4.BeautifulSoup(page, features="html.parser")
    images = soup.find_all("span", {"class": "thumb"})
    downloaded_amount = 0
    for image in images:
        if downloaded_amount >= amount:
            break
        url = "https://" + domain + "/" + image.a["href"]
        page = download_url(url)
        soup = bs4.BeautifulSoup(page, features="html.parser")
        image = soup.find("img", {"id": "image"})
        if image is None or "/samples/" in image["src"]:
            image_src = _original_image(soup)
        else:
            image_src = urllib.parse.splitquery(image["src"])[0]
        retrieve_url(
            image_src,
            os.path.join(folder, get_filename(image_src))
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
