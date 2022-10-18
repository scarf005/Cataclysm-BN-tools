#!/bin/env python3

from pathlib import Path

from schema.main import JsonFile, TileEntryFile

if __name__ == "__main__":
    Path("data/modinfo.json").write_text(JsonFile.schema_json(indent=2))
    Path('data/tileentry.json').write_text(TileEntryFile.schema_json(indent=2))
