from pathlib import Path
import pytest

from plover_markdown_dictionary import MarkdownDictionary

TEST_DATA = Path("./test/data")


@pytest.mark.parametrize(
    "test_path",
    ["empty.md", "small.md", "weird_entries.md", "code_blocks.md", "changes.md"],
)
def test_load_save(test_path, tmp_path):
    input_path = TEST_DATA / test_path
    output_path = tmp_path / "file.md"

    dictionary = MarkdownDictionary()
    dictionary._load(str(input_path))
    dictionary._save(str(output_path))

    assert input_path.read_text() == output_path.read_text()


class TestAdd:
    def test_add_to_empty(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text("")
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test"
        dictionary[("HEL", "HRO")] = "hello"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """
## Added by Plover

```yaml
TEFT: test
HEL/HRO: hello
```
"""
        )

    def test_special_characters(self, tmp_path):

        # Prefer to not quote, unless there are special characters/untrimmed spaces.
        # If there are special characters, prefer quoting with double quotes, then
        # quoting with single quotes, then escaping.

        filepath = tmp_path / "file.md"
        filepath.write_text("")
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test "
        dictionary[("T-FT",)] = " test"
        dictionary[("T-T",)] = ' "test" '
        dictionary[("T-",)] = " 'test' "
        dictionary[("R-R",)] = "\n"
        dictionary[("#S-",)] = "1"
        dictionary[("KW-T",)] = '"'
        dictionary[("AE",)] = "'"
        dictionary[("S",)] = "double \" and single '"
        dictionary[("H-RB",)] = "#"
        dictionary[("HARB",)] = '#"'
        dictionary[("HAERB",)] = "#'"
        dictionary[("PW-RB",)] = "\\"
        dictionary[("AUL",)] = " \\ # \" '"

        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """
## Added by Plover

```yaml
TEFT: "test "
T-FT: " test"
T-T: ' "test" '
T-: " 'test' "
R-R: \\\\n
"#S-": 1
KW-T: '"'
AE: "'"
S: "double \\" and single '"
H-RB: "#"
HARB: '#"'
HAERB: "#'"
PW-RB: \\\\
AUL: " \\\\ # \\" '"
```
"""
        )

    def test_save_between_add(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text("")
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))
        dictionary[("HEL", "HRO")] = "hello"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """
## Added by Plover

```yaml
TEFT: test
HEL/HRO: hello
```
"""
        )

    def test_reload_between_add(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text("")
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        reloaded = MarkdownDictionary()
        reloaded._load(str(filepath))
        reloaded[("HEL", "HRO")] = "hello"
        reloaded._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """
## Added by Plover

```yaml
TEFT: test
HEL/HRO: hello
```
"""
        )

    def test_add_to_existing(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
"S-G":something  #comment
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("H-L", "WORLD")] = "hello world!"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
"S-G":something  #comment
```

## Added by Plover

```yaml
H-L/WORLD: hello world!
```
"""
        )

    def test_add_with_existing_adds(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

## Added by Plover

```yaml
'SPWREU' : 'entry'
```
Some text

"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("S-G",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

## Added by Plover

```yaml
'SPWREU' : 'entry'
S-G: something else
```
Some text

"""
        )

    def test_add_with_multiple_existing_adds(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

## Added by Plover

```yaml
'TEFT': test
```

## Added by Plover

Text

```yaml
'SPWREU' : 'entry'
```
Some text

"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("S-G",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

## Added by Plover

```yaml
'TEFT': test
```

## Added by Plover

Text

```yaml
'SPWREU' : 'entry'
S-G: something else
```
Some text

"""
        )

    def test_add_with_existing_adds_with_multiple_code_blocks(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

## Added by Plover

```yaml
'TEFT': test
```

```yaml
'SPWREU' : 'entry'
```
Some text
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("S-G",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

## Added by Plover

```yaml
'TEFT': test
```

```yaml
'SPWREU' : 'entry'
```
Some text

## Added by Plover

```yaml
S-G: something else
```
"""
        )

    # del ()
    # set ('P',)
    # del ('P',)
    # set ('P',) test

    def test_add_like_in_gui(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text("")
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = ""
        del dictionary[("TEFT",)]
        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """
## Added by Plover

```yaml
TEFT: test
```
"""
        )


class TestDelete:
    def test_delete_entry(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
"S-G":something  #comment
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        del dictionary[("S-G",)]
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
(DELETED) "S-G":something  #comment
```
"""
        )

    def test_delete_translation_multiple_appearances(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
S-G: something # first
S-G: something # second
```

## Section

```yaml
S-G: something # third
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        del dictionary[("S-G",)]
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
(DELETED) S-G: something # first
(DELETED) S-G: something # second
```

## Section

```yaml
(DELETED) S-G: something # third
```
"""
        )


class TestUpdate:
    def test_update_translation(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
"S-G":something  #comment
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("S-G",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
(UPDATED) "S-G":something else  #comment
```
"""
        )

    def test_update_translation_existing_updates(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
(UPDATED) 'SPWREU' : 'entry'     # existing entry
"S-G":something  #comment
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("S-G",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
(UPDATED) 'SPWREU' : 'entry'     # existing entry
(UPDATED) "S-G":something else  #comment
```
"""
        )

    def test_update_translation_multiple_appearances(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
S-G: something # first
S-G: something # second
```

## Section

```yaml
S-G: something # third
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        dictionary[("S-G",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
(UPDATED) S-G: something else # first
(UPDATED) S-G: something else # second
```

## Section

```yaml
(UPDATED) S-G: something else # third
```
"""
        )

    def test_update_translation_like_in_gui(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        del dictionary[("TEFT",)]
        dictionary[("TEFT",)] = "new test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: new test
```
"""
        )

    def test_update_stroke(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
"S-G":something  #comment
```
"""
        )

        dictionary = MarkdownDictionary()
        dictionary._load(filepath)

        del dictionary[("S-G",)]
        dictionary[("S-LG",)] = "something else"
        dictionary._save(filepath)

        text = filepath.read_text()

        assert (
            text
            == """# Test dictionary

```yaml
'SPWREU' : 'entry'     # existing entry
(DELETED) "S-G":something  #comment
```

## Added by Plover

```yaml
S-LG: something else
```
"""
        )


class TestMultiple:
    def test_add_delete(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("H-L",)] = "hello"
        del dictionary[("H-L",)]
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_add_delete_save_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("H-L",)] = "hello"
        dictionary._save(str(filepath))
        del dictionary[("H-L",)]
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_add_delete_reload_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("H-L",)] = "hello"
        dictionary._save(str(filepath))

        reloaded = MarkdownDictionary()
        reloaded._load(str(filepath))
        del reloaded[("H-L",)]
        reloaded._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```

## Added by Plover

```yaml
(DELETED) H-L: hello
```
"""
        )

    def test_add_delete_deleted(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
(DELETED) TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("H-L",)] = "hello"
        del dictionary[("H-L",)]
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(DELETED) TEFT: test
```
"""
        )

    def test_add_update(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("H-L",)] = "hello"
        dictionary[("H-L",)] = "hello !!!"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```

## Added by Plover

```yaml
H-L: hello !!!
```
"""
        )

    def test_update_undo(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test!!"
        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_update_undo_save_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test!!"
        dictionary._save(str(filepath))
        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_update_undo_reload_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test!!"
        dictionary._save(str(filepath))

        reloaded = MarkdownDictionary()
        reloaded._load(str(filepath))
        reloaded[("TEFT",)] = "test"
        reloaded._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: test
```
"""
        )

    def test_update_undo_updated(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
(UPDATED) TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        dictionary[("TEFT",)] = "test!!"
        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: test
```
"""
        )

    def test_delete_add(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        del dictionary[("TEFT",)]
        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_delete_add_save_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        del dictionary[("TEFT",)]
        dictionary._save(str(filepath))
        dictionary[("TEFT",)] = "test"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_delete_add_reload_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))
        del dictionary[("TEFT",)]
        dictionary._save(str(filepath))

        reloaded = MarkdownDictionary()
        reloaded._load(str(filepath))
        reloaded[("TEFT",)] = "test"
        reloaded._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
TEFT: test
```
"""
        )

    def test_delete_update(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        del dictionary[("TEFT",)]
        dictionary[("TEFT",)] = "test!"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: test!
```
"""
        )

    def test_delete_add_save_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))

        del dictionary[("TEFT",)]
        dictionary._save(str(filepath))
        dictionary[("TEFT",)] = "test!"
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: test!
```
"""
        )

    def test_update_deleted(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
(DELETED) TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))
        dictionary._save(str(filepath))
        dictionary[("TEFT",)] = "tests"
        dictionary._save(str(filepath))
        dictionary._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: tests
```
"""
        )

    def test_delete_update_reload_between(self, tmp_path):
        filepath = tmp_path / "file.md"
        filepath.write_text(
            """# Dictionary
```yaml
TEFT: test
```
"""
        )
        dictionary = MarkdownDictionary()
        dictionary._load(str(filepath))
        del dictionary[("TEFT",)]
        dictionary._save(str(filepath))

        reloaded = MarkdownDictionary()
        reloaded._load(str(filepath))
        reloaded[("TEFT",)] = "test!"
        reloaded._save(str(filepath))

        text = filepath.read_text()
        assert (
            text
            == """# Dictionary
```yaml
(UPDATED) TEFT: test!
```
"""
        )
