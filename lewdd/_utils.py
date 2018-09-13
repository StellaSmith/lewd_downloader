import progressbar
import urllib.request
import urllib.parse
import os
import colorama

_widgets = [
    colorama.Fore.CYAN,
    "PLACEHOLDER",
    colorama.Fore.RESET,
    " ",
    progressbar.Percentage(),
    " ",
    progressbar.Bar(left="[", right="]"),
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

_headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) "
        "Gecko/20100101 Firefox/62.0"
    )
}


class _FancyURLOpener(urllib.request.FancyURLopener):
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        if errcode == 403:
            print(dir(self))
            raise ValueError(errcode, errmsg)
        return super(FixFancyURLOpener, self).http_error_default(
            url, fp, errcode, errmsg, headers
        )
_opener = _FancyURLOpener()
for v, k in _headers.items():
    _opener.addheader(v, k)
del v, k


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
    request = urllib.request.Request(url, headers=_headers)
    if silent:
        _opener.retrieve(url, filename)
        return
    progress = progressbar.ProgressBar(widgets=_widgets)
    _widgets[1] = url  # + " -> " + filename
    progress.start()
    _opener.retrieve(
        url, filename, reporthook=lambda *args: _reporthook(progress, *args)
    )
    progress.finish()


def download_url(url, silent=True):
    """
    Download to memory (returns page content in bytes)
    """

    if not silent:
        progress = progressbar.ProgressBar(widgets=_widgets)
        _widgets[1] = url
    request = urllib.request.Request(url, headers=_headers)
    response = urllib.request.urlopen(request)

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
