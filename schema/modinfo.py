import re
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, Extra, Field, conlist, constr, create_model

if TYPE_CHECKING:
    ID = str
    String = str
    List = list
else:
    ID = constr(regex=r"^[a-zA-Z0-9_]+$")
    String = constr(min_length=1)
    List = conlist(min_items=1, item_type=String)


def fold_text(text: str) -> str:
    "replace all whitespaces into single space"
    return re.sub(r"\s+", " ", text)


def field(default: Any = Undefined, desc: str = None, fold=True, **kwargs):  # type: ignore
    print(f'{default = }')
    if not desc:
        return Field(default, **kwargs)
    else:
        description = (fold_text if fold else dedent)(desc)
        return Field(
            default,
            description=description,
            markdownDescription=description,
            **kwargs,
        )


class Content(BaseModel):
    __root__: Literal["content"] = field(
        ...,
        """A mod that adds a lot of stuff.
        Typically reserved for very large mods or
        complete game overhauls
        (eg: Core game files, Aftershock)""",
    )


class Items(BaseModel):
    __root__: Literal["items"] = field(
        ...,
        """A mod that adds new items and recipes to the game
        (eg: More survival tools)""",
    )


class Creatures(BaseModel):
    __root__: Literal["creatures"] = field(
        ...,
        """A mod that adds new creatures or NPCs to the game
        (eg: Modular turrets)""",
    )


class MiscAdditions(BaseModel):
    __root__: Literal["misc_additions"] = field(
        ...,
        """Miscellaneous content additions to the game
        (eg: Alternative map key, Crazy cataclysm)""",
    )


class Buildings(BaseModel):
    __root__: Literal["buildings"] = field(
        ...,
        """New overmap locations and structures
        (eg: Fuji's more buildings).
        If you're blacklisting buildings from spawning,
        this is also a usable category
        (eg: No rail stations).""",
    )


class Vehicles(BaseModel):
    __root__: Literal["vehicles"] = field(
        ...,
        """New cars or vehicle parts
        (eg: Tanks and othem vehicles)""",
    )


class Rebalance(BaseModel):
    __root__: Literal["rebalance"] = field(
        ...,
        """A mod designed to rebalance the game in some way
         (eg: Safe autodocs).""",
    )


class Magical(BaseModel):
    __root__: Literal["magical"] = field(
        ...,
        """A mod that adds something magic-related to the game
        (eg: Necromancy)""",
    )


class ItemExclude(BaseModel):
    __root__: Literal["item_exclude"] = field(
        ...,
        """A mod that stops items from spawning in the world
         (eg: No survivor armor, No drugs)""",
    )


class MonsterExclude(BaseModel):
    __root__: Literal["monster_exclude"] = field(
        ...,
        """A mod that stops certain monster varieties from spawning in the world
        (eg: No fungal monsters, No ants)""",
    )


class Graphical(BaseModel):
    __root__: Literal["graphical"] = field(
        ...,
        """A mod that adjusts game graphics in some way
         (eg: Graphical overmap)""",
    )


Category = (
    Content
    | Items
    | Creatures
    | MiscAdditions
    | Buildings
    | Vehicles
    | Rebalance
    | Magical
    | ItemExclude
    | MonsterExclude
    | Graphical
)


class ModInfo(BaseModel):
    type_: String = field("MOD_INFO", alias="type", const=True)
    id_: ID = field(
        ...,
        alias="id",
        desc="""Mod's unique identifier, prefer to use only ASCII letters, numbers and underscore for clarity.""",
    )
    name: String = field(..., "Mod's display name, in `English`.")
    authors: List[String] = field(..., "Original author(s) of the mod.")
    description: String = field(..., "Mod's description, in `English`.")
    category: Category = field(
        ...,
        """The `category` attribute denotes
        where the mod will appear in the mod selection menu.
        These are the available categories to choose from,
        with some examples chosen from mods that existed
        when this document was written.
        Pick whichever one applies best to your mod
        when writing your modinfo file.""",
    )
    dependencies: List[String] = field(
        ...,
        """The `dependencies` attribute is used to tell Cataclysm
        that your mod is dependent on something present in another mod.
        If you have no dependencies outside of the core game,
        then just including `dda` in the list is good enough.
        If your mod depends on another one to work properly,
        adding that mod's `id` attribute to the array causes
        Cataclysm to force that mod to load before yours.""",
    )


class ModInfoFile(BaseModel):
    __root__: ModInfo | list[ModInfo]


if __name__ == "__main__":
    schema = ModInfoFile.schema()
    # sea

    # from pathlib import Path

    # Path("data/modinfo.json").write_text(ModInfoFile.schema_json(indent=2))
