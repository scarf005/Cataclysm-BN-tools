import re
from pprint import pprint
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal, Type, Union

from pydantic import BaseModel, Field, conlist, constr, create_model

if TYPE_CHECKING:
    ID = str
    String = str
    List = list
else:
    ID = constr(regex=r"^[a-zA-Z0-9_]+$")
    String = constr(min_length=1)
    List = conlist(min_items=1, item_type=String)


def to_classname(text: str) -> str:
    return "".join(t.capitalize() for t in text.split("_"))


def fold_text(text: str) -> str:
    "replace all whitespaces into single space"
    return re.sub(r"\s+", " ", text)  # type: ignore


def field(*args: str, fold: bool = True, **kwargs: Any):
    """one args: description, two args: default, description"""

    match len(args):
        case 1:
            default, description = ..., args[0]
        case 2:
            default, description = args  # type: ignore

        case _:
            raise ValueError(
                f"field() takes 1 or 2 positional arguments, but got {args}"
            )

    desc = (fold_text if fold else dedent)(description)  # type: ignore
    return Field(
        default,
        description=desc,
        markdownDescription=desc,
        **kwargs,
    )


def enum_model(
    name: str, *args: str, fold: bool = True, **kwargs: Any
) -> Type[BaseModel]:
    """one args: description, two args: default, description"""

    return create_model(
        to_classname(name),
        __root__=(Literal[name], field(*args, fold=fold, **kwargs)),  # type: ignore
        __base__=BaseModel,
    )


def enums_from(data: dict[str, str]) -> Any:
    categories_classes = (enum_model(k, v) for k, v in data.items())
    return Union[*categories_classes]  # type: ignore


Category = enums_from(
    {
        "content": """A mod that adds a lot of stuff.
                  Typically reserved for very large mods or
                  complete game overhauls
                  (eg: Core game files, Aftershock)""",
        "items": """A mod that adds new items and recipes to the game
                (eg: More survival tools)""",
        "creatures": """A mod that adds new creatures or NPCs to the game
                    (eg: Modular turrets)""",
        "misc_additions": """Miscellaneous content additions to the game
                         (eg: Alternative map key, Crazy cataclysm)""",
        "buildings": """New overmap locations and structures
                    (eg: Fuji's more buildings).
                    If you're blacklisting buildings from spawning,
                    this is also a usable category
                    (eg: No rail stations).""",
        "vehicles": """New cars or vehicle parts
                   (eg: Tanks and  vehicles)""",
        "rebalance": """A mod designed to rebalance the game in some way
                    (eg: Safe autodocs).""",
        "magical": """A mod that adds something magic-related to the game
                    (eg: Necromancy)""",
        "item_exclude": """A mod that stops items from spawning in the world
                    (eg: No survivor armor, No drugs)""",
        "monster_exclude": """A mod that stops certain monster varieties from spawning in the world
                    (eg: No fungal monsters, No ants)""",
        "graphical": """A mod that adjusts game graphics in some way
                    (eg: Graphical overmap)""",
    }
)


class ModInfo(BaseModel):
    type_: String = field(
        "MOD_INFO", "Identifier for ModInfo object.", alias="type", const=True
    )
    id_: ID = field(
        """Mod's unique identifier, prefer to use only ASCII letters,
        numbers and underscore for clarity.""",
        alias="id",
    )
    name: String = field("Mod's display name, in `English`.")
    authors: List[String] = field("Original author(s) of the mod.")
    description: String = field("Mod's description, in `English`.")
    category: Category = field(  # type: ignore
        """The `category` attribute denotes
        where the mod will appear in the mod selection menu.
        These are the available categories to choose from,
        with some examples chosen from mods that existed
        when this document was written.
        Pick whichever one applies best to your mod
        when writing your modinfo file.""",
    )
    dependencies: List[String] = field(
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

    from pathlib import Path

    Path("data/modinfo.json").write_text(ModInfoFile.schema_json(indent=2))
