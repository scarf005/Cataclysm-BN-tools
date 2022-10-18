from pydantic import BaseModel

from schema.utils import ID, reqfield

from .tileentry.tile_id import TileID


class TileEntry(BaseModel):
    id_: TileID = reqfield(  # type: ignore
        "the `game entity` represented by this sprite", alias="id"
    )
    fg: ID = reqfield("sprite name")
    bg: ID = reqfield("background sprite name, **always** a single value")
    rotates: bool = reqfield("true for things that rotate like vehicle parts")
