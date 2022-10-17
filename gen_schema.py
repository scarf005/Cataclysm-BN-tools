#!/bin/env python3

from pathlib import Path

from schema.main import JsonFile
from schema.tileinfo import TileEntry

if __name__ == "__main__":
    Path("data/modinfo.json").write_text(JsonFile.schema_json(indent=2))
    Path('data/tileinfo.json').write_text(TileEntry.schema_json(indent=2))
