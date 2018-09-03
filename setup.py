from distutils.core import setup

with open("README.md") as readme:
    long_description = readme.read()

url = "https://github.com/StellaSmith/lewd_downloader"

setup(
    name="Lewd Downloader",
    author="Stella Smith",
    url=url,
    download_url=url + "/archive/master.zip",
    license="The Unlicense",
    packages=["lewdd"]
)
