import bs4

domain = "danbooru.donmai.us"
images_per_page = 20


def format_tags(tags):
    return "+".join(tags)
