from pathlib import Path

from pydantic import BaseModel

from schema.utils import ID, JList, JStr, enums_from, field, reqfield

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
                   (eg: Tanks and vehicles)""",
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
    """data format for modinfo.json

    see https://github.com/cataclysmbnteam/Cataclysm-BN/blob/upload/doc/JSON_INFO.md#mod_info
    """

    type_: JStr = field(
        "MOD_INFO",
        "This field marks this object as modinfo.",
        alias="type",
        const=True,
    )

    id_: ID = reqfield(
        """Mod's unique identifier, prefer to use only ASCII letters,
        numbers and underscore for clarity.""",
        alias="id",
    )
    category: Category = reqfield(  # type: ignore
        """The `category` attribute denotes
        where the mod will appear in the mod selection menu.
        These are the available categories to choose from,
        with some examples chosen from mods that existed
        when this document was written.
        Pick whichever one applies best to your mod
        when writing your modinfo file.""",
    )
    name: JStr = reqfield("Mod's display name, in `English`.")
    description: JStr = reqfield("Mod's description, in `English`.")
    authors: JList[JStr] = reqfield("Original author(s) of the mod.")
    maintainers: JList[JStr] | None = field(
        """If the author(s) abandoned the mod for some reason,
        this entry lists current maintainers."""
    )
    version: JStr | None = field(
        """Mod version string.
        This is for users' and maintainers' convenience,
        so you can use whatever is most convenient here
        (e.g. `2021-12-02`)."""
    )
    dependencies: JList[JStr] = reqfield(
        """The `dependencies` attribute is used to tell Cataclysm
        that your mod is dependent on something present in another mod.
        If you have no dependencies outside of the core game,
        then just including `dda` in the list is good enough.
        If your mod depends on another one to work properly,
        adding that mod's `id` attribute to the array causes
        Cataclysm to force that mod to load before yours.""",
    )
    conflicts: JList[JStr] | None = field(
        "List of mods that are incompatible with this mod."
    )
    core: bool | None = field(
        """Special flag for core game data,
        can only be used by total overhaul mods.
        Only 1 core mod can be loaded at a time.""",
    )
    obsolete: bool | None = field(
        """Marks mod as obsolete.
        Obsolete mods don't show up in mod selection list by default,
        and have a warning on them.""",
    )
    path: Path | None = field(
        """Path of mod's files relative to the modinfo.json file.
        The game automatically loads all files from the folder with modinfo.json,
        and all the subfolders, so this field is only useful
        when you for whatever reason want to stick your modinfo.json
        in a subfolder of your mod.""",
    )


class ModInfoFile(BaseModel):
    __root__: ModInfo | list[ModInfo]
