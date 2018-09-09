from distutils.core import setup

with open("README.md") as fp:
    long_description = fp.read()

with open("requirements.txt") as fp:
    requirements = [x.strip() for x in fp]

url = "https://github.com/StellaSmith/lewd_downloader"

setup(
    name="Lewd Downloader",
    author="Stella Smith",
    url=url,
    download_url=url + "/archive/master.zip",
    license="The Unlicense",
    packages=["lewdd"],
    install_requires=requirements
)
