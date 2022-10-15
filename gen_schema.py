from schema.modinfo import ModInfoFile
from pathlib import Path

if __name__ == "__main__":
    Path("data/modinfo.json").write_text(ModInfoFile.schema_json(indent=2))
