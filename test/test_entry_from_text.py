import pytest

from plover_markdown_dictionary import entry_from_text


@pytest.mark.parametrize(
    "input, key, key_quote, value, value_quote, separator, comment_padding, comment",
    [
        (
            "#S: 1\n",
            ("1",),
            "",
            "1",
            "",
            ": ",
            "",
            "",
        ),
        (
            "2 : 2\n",
            ("2",),
            "",
            "2",
            "",
            " : ",
            "",
            "",
        ),
        (
            "-T: the\n",
            ("-T",),
            "",
            "the",
            "",
            ": ",
            "",
            "",
        ),
        (
            "*UR: you are\n",
            ("*UR",),
            "",
            "you are",
            "",
            ": ",
            "",
            "",
        ),
        (
            "'#S': '1'          # single quotes\n",
            ("1",),
            "'",
            "1",
            "'",
            ": ",
            "          ",
            "# single quotes",
        ),
        (
            "'2' : '2'\n",
            ("2",),
            "'",
            "2",
            "'",
            " : ",
            "",
            "",
        ),
        (
            '"-T" : the\n',
            ("-T",),
            '"',
            "the",
            "",
            " : ",
            "",
            "",
        ),
        (
            '"*UR": you are\n',
            ("*UR",),
            '"',
            "you are",
            "",
            ": ",
            "",
            "",
        ),
        (
            "HAERB: \\# # hash character in the right hand side\n",
            ("HAERB",),
            "",
            "#",
            "",
            ": ",
            " ",
            "# hash character in the right hand side",
        ),
        (
            "'#-T': 9 # note that you don't have to escape the # in the left side\n",
            ("-9",),
            "'",
            "9",
            "",
            ": ",
            " ",
            "# note that you don't have to escape the # in the left side",
        ),
        (
            "SKW-T: \\' # escaped single quote character\n",
            ("SKW-T",),
            "",
            "'",
            "",
            ": ",
            " ",
            "# escaped single quote character",
        ),
        (
            'KR-GS : \\" # double quote character\n',
            ("KR-GS",),
            "",
            '"',
            "",
            " : ",
            " ",
            "# double quote character",
        ),
        (
            "PW-T : \\\" \\' # both\n",
            ("PW-T",),
            "",
            "\" '",
            "",
            " : ",
            " ",
            "# both",
        ),
        (
            "HAERB: '#' # hash character in the right hand side\n",
            ("HAERB",),
            "",
            "#",
            "'",
            ": ",
            " ",
            "# hash character in the right hand side",
        ),
        (
            'SKW-T: "\'" # quotes can be surrounded by a different kind of quotes\n',
            ("SKW-T",),
            "",
            "'",
            '"',
            ": ",
            " ",
            "# quotes can be surrounded by a different kind of quotes",
        ),
        (
            "KR-GS: '\"'\n",
            ("KR-GS",),
            "",
            '"',
            "'",
            ": ",
            "",
            "",
        ),
        (
            "S-PS: ' ' # space\n",
            ("S-PS",),
            "",
            " ",
            "'",
            ": ",
            " ",
            "# space",
        ),
        (
            "TAB: \\\\t # tab\n",
            ("TAB",),
            "",
            "\t",
            "",
            ": ",
            " ",
            "# tab",
        ),
        (
            "R-R: \\\\n # newline\n",
            ("R-R",),
            "",
            "\n",
            "",
            ": ",
            " ",
            "# newline",
        ),
        (
            "R*R: \\\\r # return\n",
            ("R*R",),
            "",
            "\r",
            "",
            ": ",
            " ",
            "# return",
        ),
        (
            "4: '\\\\r\\\\n\\\\t' # special\n",
            ("4",),
            "",
            "\r\n\t",
            "'",
            ": ",
            " ",
            "# special",
        ),
        (
            'TEFT :  "test"#comment\n',
            ("TEFT",),
            "",
            "test",
            '"',
            " :  ",
            "",
            "#comment",
        ),
        (
            'TEFT/KAEUS : "##"#d\n',
            (
                "TEFT",
                "KAEUS",
            ),
            "",
            "##",
            '"',
            " : ",
            "",
            "#d",
        ),
        (
            '6:"##"#\n',
            ("-6",),
            "",
            "##",
            '"',
            ":",
            "",
            "#",
        ),
        (
            'KW-T/HAERB:"#"\n',
            (
                "KW-T",
                "HAERB",
            ),
            "",
            "#",
            '"',
            ":",
            "",
            "",
        ),
        (
            'KA*US : "cause\'"\n',
            ("KA*US",),
            "",
            "cause'",
            '"',
            " : ",
            "",
            "",
        ),
        (
            'TEFT: "test"  # quoted value\n',
            ("TEFT",),
            "",
            "test",
            '"',
            ": ",
            "  ",
            "# quoted value",
        ),
        (
            '"TEFT" : "ab#cde"     # # hash in comment\n',
            ("TEFT",),
            '"',
            "ab#cde",
            '"',
            " : ",
            "     ",
            "# # hash in comment",
        ),
        (
            'SKAEP:"abc\\\\def\\""     # " backslash, quote in comment\n',
            ("SKAEP",),
            "",
            'abc\\def"',
            '"',
            ":",
            "     ",
            '# " backslash, quote in comment',
        ),
        (
            "HAESH: \\## escape hash\n",
            ("HAESH",),
            "",
            "#",
            "",
            ": ",
            "",
            "# escape hash",
        ),
        (
            "PW-RB: \\\\ # backslash\n",
            ("PW-RB",),
            "",
            "\\",
            "",
            ": ",
            " ",
            "# backslash",
        ),
        (
            "HAERB/TPRAEUS/WAO : \\# phrase  woo  # comment\n",
            (
                "HAERB",
                "TPRAEUS",
                "WAO",
            ),
            "",
            "# phrase  woo",
            "",
            " : ",
            "  ",
            "# comment",
        ),
        (
            "S-T: # empty translation\n",
            ("S-T",),
            "",
            "",
            "",
            ": ",
            "",
            "# empty translation",
        ),
    ],
)
def test_entry(
    input,
    key,
    key_quote,
    value,
    value_quote,
    separator,
    comment_padding,
    comment,
):
    entry = entry_from_text(input)

    assert entry.key == key
    assert entry.key_quote == key_quote
    assert entry.value == value
    assert entry.value_quote == value_quote
    assert entry.separator == separator
    assert entry.comment_padding == comment_padding
    assert entry.comment == comment


def test_deleted():
    entry = entry_from_text("(DELETED) SPH/TEGT: some text? # this was deleted\n")

    assert entry.is_deleted == True


def test_updated():
    entry = entry_from_text("(UPDATED) AUPT/-D  :  updated~ #  this was updated\n")

    assert entry.is_updated == True


@pytest.mark.parametrize(
    "input",
    [
        "",
        "\n",
        'KW-T: "',
        "PW-RBL: \\",
    ],
)
def test_entry_fails(input):
    with pytest.raises(ValueError):
        entry_from_text(input)

@pytest.mark.parametrize(
    "input",
    [
        "invalid: steno\n",
    ],
)
def test_entry_soft_fails(input, caplog):
    entry_from_text(input)
    assert "ValueError: invalid steno: " in caplog.text
