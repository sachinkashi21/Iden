import json
from typing import List, Dict

def open_file(filepath: str) -> None:
    """Initialize the JSON file with an opening ["""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("[\n")

def append_to_file(filepath: str, items: List[Dict], first: bool = False) -> None:
    """Append items to the JSON array in the file."""
    with open(filepath, "a", encoding="utf-8") as f:
        for i, item in enumerate(items):
            if not first or i > 0:
                f.write(",\n")
            json.dump(item, f, ensure_ascii=False)

def close_file(filepath: str) -> None:
    """Close the JSON file with a closing ]"""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n]\n")
