
#  Lewd-Downloader

## Installation
It's as easy as:
```bash
pip install git+https://github.com/StellaSmith/lewd_downloader/
```

##  Usage

```bash
python -m lewdd [-h] [-n amount] [-o path] domain tags [tags ...]
```

Please see `python -m lewdd -h` for more information

#### Examples:
```bash
python -m lewdd rule34.xxx vocaloid big_breats
```
This will download *every* image tagged with `vocaloid big_breats`, under the `rule34.xxx vocaloid big_breasts` folder

```bash
python -m lewdd -n 5 -o fountains realbooru.com squirting
```
This will download *at most* five images tagged with `squirting`, under the `fountains` folder
