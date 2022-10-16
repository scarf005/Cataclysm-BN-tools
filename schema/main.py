
from pydantic import BaseModel

from schema.modinfo import ModInfo


JsonTypes = ModInfo

class JsonFile(BaseModel):
    __root__: JsonTypes | list[JsonTypes] # type: ignore
