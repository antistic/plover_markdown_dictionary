# using plover tests
from pathlib import Path

from plover_build_utils.testing import dictionary_test

from plover_markdown_dictionary import MarkdownDictionary

TEST_DATA = Path("./test/data")


@dictionary_test
class TestMarkdownDictionary:
    DICT_CLASS = MarkdownDictionary
    DICT_EXTENSION = "md"
    DICT_SAMPLE = (TEST_DATA / "weird_entries.md").read_bytes()
    DICT_REGISTERED = True
    DICT_LOAD_TESTS = (
        lambda: (
            (TEST_DATA / "empty.md").read_bytes(),
            "",
        ),
        lambda: (
            (TEST_DATA / "small.md").read_bytes(),
            """
            'KP-PL': 'example',
            'KP-PL/KOPLT': "example with comment",
            """,
        ),
        lambda: (
            (TEST_DATA / "weird_entries.md").read_bytes(),
            """
            "HAERB": '"#"',
            "TEFT": "test ",
            "T": " 'test' ",
            "T-FT": " test",
            "T-T": ' "test" ',
            "R-R": "\\n",
            "1": "1",
            "-9": "9",
            "-RL": "recall",
            "KW-T": '"',
            "AE": "'",
            "S": "double \\" and single '",
            "H-RB": "#",
            "HARB": '#"',
            "HA*ERB": "#'",
            "PW-RB": "\\\\",
            "AUL": " \\\\ # \\" '",
            "SKWRAOEURBGS": "{^~|\\\\n\\\\n^}",
            "KOED/KWRAPL": "```yaml",
            """,
        ),
        lambda: (
            (TEST_DATA / "code_blocks.md").read_bytes(),
            """
            "S-G": "something",
            "TEFT": "test",
            "TWO": "two",
            "HEU": "hi",
            "THRAOE": "three",
            """,
        ),
        lambda: (
            (TEST_DATA / "changes.md").read_bytes(),
            """
            "AUPTD": "updated",
            "AD/-D": "added",
            """,
        ),
    )

    DICT_SAVE_TESTS = (
        lambda: (
            """
            "HAERB": '"#"',
            "TEFT": "test ",
            "T": " 'test' ",
            "T-FT": " test",
            "T-T": ' "test" ',
            "R-R": "\\n",
            "1": "1",
            "-9": "9",
            "-RL": "recall",
            "KW-T": '"',
            "AE": "'",
            "S": "double \\" and single '",
            "H-RB": "#",
            "HARB": '#"',
            "HA*ERB": "#'",
            "PW-RB": "\\\\",
            "AUL": " \\\\ # \\" '",
            "SKWRAOEURBGS": "{^~|\\n\\n^}",
            "KOED/KWRAPL": "```yaml",
            """,
            b"""
## Added by Plover

```yaml
HAERB: '"#"'
TEFT: "test "
T: " 'test' "
T-FT: " test"
T-T: ' "test" '
R-R: \\\\n
1: 1
-9: 9
-RL: recall
KW-T: '"'
AE: "'"
S: "double \\" and single '"
H-RB: "#"
HARB: '#"'
HA*ERB: "#'"
PW-RB: \\\\
AUL: " \\\\ # \\" '"
SKWRAOEURBGS: {^~|\\\\n\\\\n^}
KOED/KWRAPL: ```yaml
```
""",
        ),
    )
