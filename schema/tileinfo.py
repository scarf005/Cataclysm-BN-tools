import re
from typing import Type

from pydantic import BaseModel, ConstrainedStr, constr, create_model

from schema.utils import ID, enums_from, field, id_with, reqfield

NPC_ID_DESC = """ The special ids
`"player_female"`, `"player_male"`, `"npc_female"`, `"npc_male"`
are used to identify the sprites for the player avatar and NPCs."""

SEASON_ID_DESC = """The special suffixes
    `_season_spring`, `_season_summer`, `_season_autumn`, and `_season_winter`
    can be applied to any entity id to create a seasonal variant for that entity
    that will be displayed in the appropriate season like
    this `"id": "mon_wolf_season_winter".`"""


NPCS = {
    k: NPC_ID_DESC
    for k in ("player_female", "player_male", "npc_female", "npc_male")
}

UNKNOWN = {
    "unknown": """The special id `"unknown"` provides a sprite
                      that is displayed when an entity has no other sprite."""
}


# def id_with(suffix: str) -> Type[str]:
#     return constr(regex=rf"^[a-zA-Z0-9_]+_{suffix}$")


# SEASON = {
#     id_with(k): SEASON_ID_DESC
#     for k in (
#         "season_spring",
#         "season_summer",
#         "season_autumn",
#         "season_winter",
#     )
# }

SpecialId = enums_from(NPCS | UNKNOWN)
# SpecialIdSuffix = enums_from(SEASON)

# SEASON_SPRING =
# class IDWith1(ConstrainedStr):
#     regex=re.compile( r"^[a-zA-Z0-9_]+_season_spring$")

# class IDWith2(ConstrainedStr):
#     regex=re.compile( r"^[a-zA-Z0-9_]+_season_winter$")

IDWith1 = id_with("IDWith1", re.compile(r"^[a-zA-Z0-9_]+_season_spring$"))
IDWith2 = id_with("IDWith2", re.compile(r"^[a-zA-Z0-9_]+_season_winter$"))


class MySeasonSpring(BaseModel):
    __root__: IDWith1 | IDWith2 = field(SEASON_ID_DESC)


# SeasonSpring = create_model(
#         "MyClassNameIsSeasonSpring",
#         regex=re.compile(r"^[a-zA-Z0-9_]+_season_spring$"),
#         __base__=ConstrainedStr,
#     )


class TileEntry(BaseModel):
    id_: ID | SpecialId | MySeasonSpring = reqfield(  # type: ignore
        "the `game entity` represented by this sprite", alias="id"
    )
    fg: ID = reqfield("sprite name")
    bg: ID = reqfield("background sprite name, **always** a single value")
    rotates = field(False, "true for things that rotate like vehicle parts")
