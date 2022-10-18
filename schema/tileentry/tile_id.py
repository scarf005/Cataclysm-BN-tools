from distutils.sysconfig import PREFIX

from schema.utils import ID, RegexType, id_from
from typing_extensions import LiteralString

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

    "id": "mon_wolf_season_winter"."""

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

TERRAIN = id_from("Terrain", "{id} indicates terrain", ("t",), RegexType.PREFIX)

def overlay(text: str, desc: str):
    names: tuple[LiteralString, ...] = tuple(f"overlay{t}_{text}" for t in ("", "_female", "_male"))  # type: ignore

    return id_from(f"Overlay{text.capitalize()}", desc, names, RegexType.PREFIX)


OVERLAY_MUTATION_DESC = """
    {id} can prefix any trait or bionic in the game to specify an overlay image
    that will be laid over the player and NPC sprites to indicate they have that mutation or bionic."""

OVERLAY_MUTATION = overlay("mutation", OVERLAY_MUTATION_DESC)

OVERLAY_WORN_DESC = """
    {id} can prefix any item in the game to specify an overlay image
    that will be laid over the player and NPC sprites to indicate they are wearing that item."""

OVERLAY_WORN = overlay("worn", OVERLAY_WORN_DESC)

OVERLAY_WIELDED_DESC = """
    {id} can prefix any item in the game to specify an overlay image
    that will be laid over the player and NPC sprites to indicate they are holding that item."""

OVERLAY_WIELDED = overlay("wielded", OVERLAY_WIELDED_DESC)

OverlayID = OVERLAY_MUTATION | OVERLAY_WORN | OVERLAY_WIELDED
SpecialID = NPCS | UNKNOWN | SEASON | OverlayID
TileID = ID | TERRAIN | SpecialID
