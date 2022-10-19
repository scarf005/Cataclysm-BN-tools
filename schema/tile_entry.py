from typing import Literal

from pydantic import BaseModel

from schema.tileentry.image import Image
from schema.tileentry.tile_id import TileID
from schema.utils import field, reqfield

MULTITILE_DESC = """
`"multitle"` is an *optional* field.
If it is present and `true`,
there must be an `additional_tiles`
list with 1 or more dictionaries for
entities and sprites associated with
this tile, such as broken versions
of an item or wall connections
"""


class TileEntry(BaseModel):
    id_: TileID = reqfield(  # type: ignore
        "the `game entity` represented by this sprite", alias="id"
    )
    fg: Image = reqfield("sprite name")
    bg: Image = reqfield("background sprite name, **always** a single value")
    rotates: bool = reqfield("true for things that rotate like vehicle parts")
    multitile: Literal[False] | None = field(False, MULTITILE_DESC)


class AdditionalTileEntry(BaseModel):
    id_: TileID = reqfield(
        "Each dictionary in the list has an `id` field", alias="id"
    )
    fg: Image
    bg: Image | None


class MultiTileEntry(BaseModel):
    id_: TileID = reqfield(  # type: ignore
        "the `game entity` represented by this sprite", alias="id"
    )
    fg: Image = reqfield("sprite name")
    bg: Image = reqfield("background sprite name, **always** a single value")
    rotates: bool = reqfield("true for things that rotate like vehicle parts")
    multitile: bool = field(True, MULTITILE_DESC, require=True, const=True)
    additional_tiles: list[AdditionalTileEntry] = reqfield("additional tiles")


class TileEntryTypes(BaseModel):
    __root__: MultiTileEntry | TileEntry
