from . import rule34_xxx, danbooru, gelbooru, rule34_paheal, e621, realbooru
from ._utils import *

domains_to_module = {
    rule34_xxx.domain: rule34_xxx,
    danbooru.domain: danbooru,
    gelbooru.domain: gelbooru,
    rule34_paheal.domain: rule34_paheal,
    e621.domain: e621,
    realbooru.domain: realbooru
}
