"""test converting to/from this dictionary

plover source code for dictionary copy:
  https://github.com/openstenoproject/plover/blob/4ad9c3077a2821aaf37f52afee6f2fdf800a2d42/plover/gui_qt/dictionaries_widget.py#L396
"""
from pathlib import Path
import json
import pytest

from plover.dictionary.json_dict import JsonDictionary
from plover.oslayer.config import ASSETS_DIR
from plover.registry import registry
from plover import system

from plover_markdown_dictionary import MarkdownDictionary

TEST_DATA = Path("./test/data")

registry.update()
system.setup("English Stenotype")


def test_md_to_json(tmp_path):
    json_path = tmp_path / "dict.json"
    md_path = tmp_path / "dict.md"

    md_path.write_text(
        """
## Added by Plover

```yaml
HEU: hi
HEL/HRO: hello
TEFT: test
```
"""
    )
    md_dict = MarkdownDictionary()
    md_dict._load(str(md_path))

    json_dict = JsonDictionary().create(str(json_path))
    json_dict.update(md_dict)
    json_dict.save()

    result = json.loads(json_path.read_text())
    assert result == {
        "HEU": "hi",
        "HEL/HRO": "hello",
        "TEFT": "test",
    }


def test_json_to_md(tmp_path):
    json_path = tmp_path / "dict.json"
    md_path = tmp_path / "dict.md"

    json_path.write_text(
        """
{
"HEU": "hi",
"HEL/HRO": "hello",
"TEFT": "test"
}
"""
    )
    json_dict = JsonDictionary()
    json_dict._load(str(json_path))

    md_dict = MarkdownDictionary().create(str(md_path))
    md_dict.update(json_dict)
    md_dict.save()

    assert (
        md_path.read_text()
        == """
## Added by Plover

```yaml
HEU: hi
HEL/HRO: hello
TEFT: test
```
"""
    )


def test_json_to_md_to_json(tmp_path):
    json1_path = TEST_DATA / "example.json"
    json2_path = tmp_path / "dict2.json"
    md_path = tmp_path / "dict.md"

    json1_dict = JsonDictionary()
    json1_dict._load(str(json1_path))

    md1_dict = MarkdownDictionary().create(str(md_path))
    md1_dict.update(json1_dict)
    md1_dict.save()

    md2_dict = MarkdownDictionary().create(str(md_path))
    md2_dict._load(str(md_path))

    json2_dict = JsonDictionary().create(str(json2_path))
    json2_dict.update(md2_dict)
    json2_dict.save()

    assert json.loads(json2_path.read_text()) == json.loads(json1_path.read_text())


@pytest.mark.slow
def test_load_main_dict(tmp_path):
    MAIN_DICT = Path(ASSETS_DIR) / "main.json"
    md_path = tmp_path / "output.md"

    json1_dict = JsonDictionary().create(str(MAIN_DICT))
    json1_dict._load(str(MAIN_DICT))

    md_dict = MarkdownDictionary().create(str(md_path))
    md_dict.update(json1_dict)
    md_dict.save()

    # has loaded without error
    assert True
