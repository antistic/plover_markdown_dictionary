from pathlib import Path
import pytest

from plover_markdown_dictionary import MarkdownDictionary

TEST_DATA = Path("./test/data")


@pytest.mark.parametrize("test_path", ["error_unequal_code_block.md"])
def test_load_fails(test_path):
    dictionary = MarkdownDictionary()
    with pytest.raises(Exception):
        dictionary._load(str(TEST_DATA / test_path))
