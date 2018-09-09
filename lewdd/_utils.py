import progressbar
import urllib.request
import urllib.parse
import os

_widgets = [
    "PLACEHOLDER",
    " ",
    progressbar.Percentage(),
    " ",
    progressbar.Bar(),
    progressbar.FileTransferSpeed(),
    " ",
    progressbar.AdaptiveETA()
]


def _reporthook(bar, block_count, block_size, total_size):
    if total_size != -1:
        bar.maxval = total_size
        downloaded = min(block_size * block_count, total_size)
        bar.update(downloaded)
    else:
        bar.update()


def get_filename(url):
    """
    Gets a file name from an url
    """
    url = urllib.parse.urlparse(url)
    return url.path.rsplit("/", 1)[1]


def retrieve_url(url, filename, silent=False):
    """
    Downloads to disk
    """
    if silent:
        urllib.request.urlretrieve(url, filename)
        return
    progress = progressbar.ProgressBar(widgets=_widgets)
    _widgets[0] = url + " -> " + filename
    progress.start()
    urllib.request.urlretrieve(
        url, filename, reporthook=lambda *args: _reporthook(progress, *args)
    )
    progress.finish()


def download_url(url, silent=True):
    """
    Download to memory (returns page content in bytes)
    """

    if not silent:
        progress = progressbar.ProgressBar(widgets=_widgets)
        _widgets[0] = url
    response = urllib.request.urlopen(url)

    downloaded = b""
    block_size = 8192
    block_count = 1
    total_size = int(response.getheader("Content-Length", -1))

    if not silent:
        progress.start()

    buffer = response.read(block_size)
    while buffer:
        if not silent:
            _reporthook(progress, block_count, block_size, total_size)
        downloaded += buffer
        buffer = response.read(block_size)
        block_count += 1
    if not silent:
        progress.finish()
    return downloaded
