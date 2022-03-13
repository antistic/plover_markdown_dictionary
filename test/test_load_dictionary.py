from pathlib import Path
import pytest

from plover_markdown_dictionary import MarkdownDictionary

TEST_DATA = Path("./test/data")


class TestLoad:
    @pytest.mark.parametrize(
        "test_path, expected",
        [
            ("empty.md", {}),
            (
                "small.md",
                {
                    ("KP-PL",): "example",
                    ("KP-PL", "KOPLT"): "example with comment",
                },
            ),
            (
                "weird_entries.md",
                {
                    ("HAERB",): '"#"',
                    ("TEFT",): "test ",
                    ("T-",): " 'test' ",
                    ("T-FT",): " test",
                    ("T-T",): ' "test" ',
                    ("R-R",): "\n",
                    ("#S-",): "1",
                    ("KW-T",): '"',
                    ("AE",): "'",
                    ("S",): "double \" and single '",
                    ("H-RB",): "#",
                    ("HARB",): '#"',
                    ("HA*ERB",): "#'",
                    ("PW-RB",): "\\",
                    ("AUL",): " \\ # \" '",
                    ("SKWRAOEURBGS",): "{^~|\\n\\n^}",
                    ("KOED", "KWRAPL"): "```yaml",
                },
            ),
            (
                "code_blocks.md",
                {
                    ("S-G",): "something",
                    ("TEFT",): "test",
                    ("TWO",): "two",
                    ("HEU",): "hi",
                    ("THRAOE",): "three",
                },
            ),
            (
                "changes.md",
                {
                    ("AUPTD",): "updated",
                    ("AD", "-D"): "added",
                },
            ),
        ],
    )
    def test_load(self, test_path, expected):
        dictionary = MarkdownDictionary()
        dictionary._load(str(TEST_DATA / test_path))
        assert dict(dictionary.items()) == expected

    @pytest.mark.parametrize("test_path", ["error_unequal_code_block.md"])
    def test_load_fails(self, test_path):
        dictionary = MarkdownDictionary()
        with pytest.raises(Exception):
            dictionary._load(str(TEST_DATA / test_path))
