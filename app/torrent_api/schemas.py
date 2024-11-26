from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict


@dataclass
class TorrentApi(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    magnet_key: str
    size: str
    rank: int
    tracker: str
    downloads: int
    seeders: int
    leechers: int
    magnet_link: str = ""
