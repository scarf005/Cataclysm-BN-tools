from pydantic import BaseModel, ConstrainedSet, conlist
from schema.tileentry.tile_id import TileID
from schema.utils import JPositive, field


class SingleImageArray(BaseModel):
    __root__: tuple[TileID] = field(
        """A single image.
        why not just use a string instead?""",
        deprecated=True,
    )


class LeftRightImage(BaseModel):
    __root__: tuple[TileID, TileID] = field("`left` and `right`")


class FourRotateImage(BaseModel):
    __root__: tuple[TileID, TileID, TileID, TileID] = field(
        "`north`, `east`, `south`, `west`"
    )


class WeightedEntry(BaseModel):
    weight: JPositive = field("The weight of this entry")
    sprite: TileID = field("The sprite to use")

class WeightedArray(BaseModel):
    __root__: list[WeightedEntry] = field("A list of weighted entries")

Image = (
    TileID
    | SingleImageArray
    | LeftRightImage
    | FourRotateImage
    | WeightedArray
)
