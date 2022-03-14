from contextlib import contextmanager
from pathlib import Path
import time

from plover.dictionary.json_dict import JsonDictionary
from plover.oslayer.config import ASSETS_DIR
from plover import system
from plover.registry import registry

from plover_markdown_dictionary import MarkdownDictionary

registry.update()
system.setup("English Stenotype")

MAIN_DICT = Path(ASSETS_DIR) / "main.json"
OUTPUT_JSON = Path("./output.json")
OUTPUT_MD = Path("./output.md")
OUTPUT_MD2 = Path("./output2.md")


def load_json():
    json_dict = JsonDictionary().create(str(MAIN_DICT))
    json_dict._load(str(MAIN_DICT))
    return json_dict


def load_markdown():
    md_dict = MarkdownDictionary().create(str(OUTPUT_MD))
    md_dict._load(str(OUTPUT_MD))
    return md_dict


def load_json_save_json():
    json_dict = load_json()

    json_dict2 = JsonDictionary().create(str(OUTPUT_JSON))
    json_dict2.update(json_dict)
    json_dict2.save()


def load_json_save_md():
    json_dict = load_json()

    md_dict = MarkdownDictionary().create(str(OUTPUT_MD))
    md_dict.update(json_dict)
    md_dict.save()

def load_markdown_save_markdown():
    md_dict = load_markdown()

    md_dict2 = MarkdownDictionary().create(str(OUTPUT_MD2))
    md_dict2.update(md_dict)
    md_dict2.save()

@contextmanager
def timer(label):
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    print(f"{label}: {end_time - start_time:.2f}s")


if __name__ == "__main__":
    with timer("Load JSON"):
        load_json()

    with timer("Load JSON + Save JSON"):
        load_json_save_json()

    with timer("Load JSON + Save Markdown"):
        load_json_save_md()

    with timer("Load Markdown"):
        load_markdown()

    with timer("Load Markdown + Save Markdown"):
        load_markdown_save_markdown()

