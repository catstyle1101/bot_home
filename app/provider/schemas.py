from typing import Final

from pydantic import BaseModel

BYTES_IN_ONE_KB: Final[int] = 1024
BYTES_IN_ONE_MB: Final[int] = 1024 * BYTES_IN_ONE_KB
BYTES_IN_ONE_GB: Final[int] = 1024 * BYTES_IN_ONE_MB
BYTES_IN_ONE_TB: Final[int] = 1024 * BYTES_IN_ONE_GB

ROUND_SIGNS: Final[int] = 2

BYTES_WITH_NAMES = (
    ("TB", BYTES_IN_ONE_TB),
    ("GB", BYTES_IN_ONE_GB),
    ("MB", BYTES_IN_ONE_MB),
    ("KB", BYTES_IN_ONE_KB),
    ("B", 0),
)


class Torrent(BaseModel):
    id: str | int | None = None
    name: str
    size: int = 0
    category: str = ""
    comment: str = ""
    magnet_uri: str = ""

    @property
    def str_size(self):
        for name, value in BYTES_WITH_NAMES:
            if self.size > value:
                return f"{round(self.size / value, ROUND_SIGNS)} {name}"
