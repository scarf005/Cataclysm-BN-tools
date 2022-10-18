from pydantic import BaseModel
from schema.tileentry.tile_id import TileID

from schema.utils import JPositive

class Foo(BaseModel):
    weight: JPositive
    sprite: TileID
