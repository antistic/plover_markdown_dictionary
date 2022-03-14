from pathlib import Path

from plover.dictionary.json_dict import JsonDictionary
from plover import system
from plover.registry import registry

from plover_markdown_dictionary import MarkdownDictionary

registry.update()
system.setup("English Stenotype")

README_MD = Path("./README.md")
OUTPUT_JSON = Path("./example.json")


if __name__ == "__main__":
    md_dict = MarkdownDictionary().create(str(README_MD))
    md_dict._load(str(README_MD))

    json_dict2 = JsonDictionary().create(str(OUTPUT_JSON))
    json_dict2.update(md_dict)
    json_dict2.save()
