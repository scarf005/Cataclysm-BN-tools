from schema.modinfo import ModInfo
from schema.tile_entry import TileEntryTypes

from schema.utils import object_or_list

JsonTypes = ModInfo

JsonFile = object_or_list("JsonFile", JsonTypes)
TileEntryFile = object_or_list("TileEntryFile", TileEntryTypes)
