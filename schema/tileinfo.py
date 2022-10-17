from pydantic import BaseModel

from schema.utils import ID, RegexType, field, id_from, reqfield

NPCS_DESC = """
    {id} are used to identify
    the sprites for the **player avatar** and **NPC**s."""
NPCS = id_from(
    "NPCS",
    NPCS_DESC,
    ("player_female", "player_male", "npc_female", "npc_male"),
)

SEASON_DESC = """
    {id} can be applied to any entity id to create a **seasonal variant** for that entity that will be displayed in the appropriate season like this:

    "id": "mon_wolf_season_winter".
    """
SEASON = id_from(
    "Season",
    SEASON_DESC,
    ("spring", "summer", "winter", "fall"),
    RegexType.SUFFIX,
    fold=False,
)

UNKNOWN_DESC = """
    {id} provides a sprite
    that is displayed when an entity has no other sprite."""
UNKNOWN = id_from("UNKNOWN", UNKNOWN_DESC, ("unknown",))


SpecialID = NPCS | UNKNOWN | SEASON


class TileEntry(BaseModel):
    id_: ID | SpecialID = reqfield(  # type: ignore
        "the `game entity` represented by this sprite", alias="id"
    )
    fg: ID = reqfield("sprite name")
    bg: ID = reqfield("background sprite name, **always** a single value")
    rotates = field(False, "true for things that rotate like vehicle parts")
