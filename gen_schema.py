from schema.main import JsonFile
from pathlib import Path

if __name__ == "__main__":
    Path("data/modinfo.json").write_text(JsonFile.schema_json(indent=2))
