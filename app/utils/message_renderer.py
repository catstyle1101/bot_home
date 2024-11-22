from typing import Unpack, TypedDict, NotRequired, TYPE_CHECKING
# from typing_extensions import TypedDict, Unpack # < Python 3.12


from jinja2 import Template

if TYPE_CHECKING:
    from provider.schemas import Torrent
    from torrent_api.data_formatter import TorrentFormatter


class Kw(TypedDict):
    is_admin: NotRequired[bool]
    result: NotRequired[bool]
    torrents: NotRequired[list[TorrentFormatter]]
    is_short: NotRequired[bool]
    name: NotRequired[str]
    torrent_name: NotRequired[str]
    is_deleted: NotRequired[bool]
    torrent: NotRequired[Torrent]


def render_message(template_name: str, **kwargs: Unpack[Kw]) -> str:
    with open(template_name, "r") as f:
        template = Template(f.read())

    message: str = template.render(**kwargs)
    return message
