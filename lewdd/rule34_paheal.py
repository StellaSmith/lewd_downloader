import re
import os
import bs4
from ._utils import *

domain = "rule34.paheal.net"
images_per_page = 70


def format_tags(tags):
    return " ".join(tags)


def get_max_page(tags):
    url = "https://{}/post/list/{}".format(
        domain,
        format_tags(tags)
    )
    page = download_url(url)
    soup = bs4.BeautifulSoup(page, features="html.parser")

    paginator = soup.find("section", attrs={"id": "paginator"})
    last = paginator.find_all("a")[2]["href"].rsplit("/", 1)[1]
    return int(last)


def download_page(tags, folder, page, amount):
    url = "https://{}//post/list/{}/{}".format(
        domain, format_tags(tags), page
    )
    page = download_url(url, silent=False)
    soup = bs4.BeautifulSoup(page, features="html.parser")
    images = soup.find_all("div", {"class": "thumb"})
    downloaded_amount = 0
    for image in images:
        if downloaded_amount >= amount:
            break
        image_src = image.find_all("a")[1]["href"]
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
