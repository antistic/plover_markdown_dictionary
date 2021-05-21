import re
from dataclasses import dataclass


from plover.steno_dictionary import StenoDictionary


DELETED_PREFIX = "(DELETED) "
UPDATED_PREFIX = "(UPDATED) "


@dataclass
class Prose:
    kind = "prose"
    text: str
    is_new: bool = False

    def __str__(self):
        return self.text


@dataclass
class Entry:
    kind = "entry"
    key: str
    key_quote: str
    value: str
    updated_value: str
    value_quote: str
    separator: str
    comment_padding: str
    comment: str
    is_deleted: bool
    is_new: bool

    def __str__(self):
        prefix_string = (
            DELETED_PREFIX
            if self.is_deleted
            else UPDATED_PREFIX
            if self.value != self.updated_value
            else ""
        )

        value_to_write = (self.updated_value or self.value).replace("\\", "\\\\")
        if self.value_quote == "":
            value_to_write = (
                value_to_write.replace('"', '\\"')
                .replace("'", "\\'")
                .replace("#", "\\#")
                .replace("\n", "\\\\n")
            )
        elif self.value_quote == "'":
            value_to_write = value_to_write.replace("'", "\\'")
        else:
            value_to_write = value_to_write.replace('"', '\\"')

        return (
            prefix_string
            + self.key_quote
            + "/".join(self.key)
            + self.key_quote
            + self.separator
            + self.value_quote
            + value_to_write
            + self.value_quote
            + self.comment_padding
            + self.comment
            + "\n"
        )

    @property
    def is_updated(self):
        return self.value != self.updated_value


first_pattern = re.compile(
    rf"((?:"
    + re.escape(DELETED_PREFIX)
    + ")?(?:"
    + re.escape(UPDATED_PREFIX)
    + ")?)"
    + r"([^:\s]+)(\s*:\s*)([^\n]+)\n"
)
left_pattern = re.compile(r"([\'\"]?)([#STKPWHRAO\*-EUFRPBLGTSDZ/]+)([\'\"]?)")
right_quote_pattern = {}
for q in ['"', "'"]:
    right_quote_pattern[q] = re.compile(
        rf"{q}((?:[^{q}\n\\]|\\\\|\\{q})*){q}"  # quoted value
        + r"([^\n\S]*)"  # spaces before comment
        + r"(#[^\n]*)?"  # comment
    )
right_no_quote_pattern = re.compile(
    r"""((?:[^'"\\\#\n\s]|\\\\|\\"|\\'|\\\#|[^\S\n]+(?:[^\#\s\\]|\\\\|\\"|\\'|\\\#))*)"""  # value
    + r"([^\n\S]*)"  # spaces before comment
    + r"((?:#[^\n]*)?)"  # comment
)


def entry_from_text(text, is_new=False):
    if text == "":
        raise ValueError("Unexpected empty line")

    match = first_pattern.fullmatch(text)

    if match is None:
        raise ValueError(f"Couldn't parse {text}")

    prefix, left, separator, right = match.groups()

    is_deleted = False
    is_updated = False
    if prefix == DELETED_PREFIX:
        is_deleted = True
    elif prefix == UPDATED_PREFIX:
        is_updated = True

    left_match = left_pattern.fullmatch(left)
    if left_match is None:
        raise ValueError(f"Couldn't parse the left side of {text}")
    key_start_quote, key, key_end_quote = left_match.groups()
    assert key_start_quote == key_end_quote

    q = right[0]
    if q == '"' or q == "'":
        value_quote = q
        right_match = right_quote_pattern[q].fullmatch(right)
        if not right_match:
            raise ValueError(f"Couldn't parse the right side of {text}")
        value, padding, comment = right_match.groups()

        value = value.replace(f"\\{q}", q).replace("\\\\", "\\")
    else:
        value_quote = ""
        right_match = right_no_quote_pattern.fullmatch(right)
        if not right_match:
            raise ValueError(f"Couldn't parse the right side of {text}")
        value, padding, comment = right_match.groups()
        for c in ["'", '"', "#", "\\"]:
            value = value.replace(f"\\{c}", c)
        value = value.replace("\\n", "\n")

    return Entry(
        key=tuple(key.split("/")),
        key_quote=key_start_quote,
        value=None if is_updated else value,
        updated_value=value,
        value_quote=value_quote,
        separator=separator,
        comment_padding=padding,
        comment=comment or "",
        is_deleted=is_deleted,
        is_new=is_new,
    )


ignored_code_block_start_pattern = re.compile(r"(```+)\w*\s*\n")
code_block_start_pattern = re.compile(r"(```+)(?:yaml)?\s*\n")


class MarkdownDictionary(StenoDictionary):

    PLOVER_ADDS_TITLE = "## Added by Plover\n"

    def __init__(self):
        super().__init__()
        self.rich_lines = []
        self.plover_adds_section_end_index = None

    def _load(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()

        in_code_block = None
        in_ignored_code_block = None
        in_adds_section = False

        for i, line in enumerate(lines):
            try:
                if in_code_block:
                    if re.fullmatch(rf"{in_code_block}\s*\n", line):
                        if in_adds_section:
                            if self.plover_adds_section_end_index:
                                in_adds_section = False
                                self.plover_adds_section_end_index = None
                            else:
                                self.plover_adds_section_end_index = len(
                                    self.rich_lines
                                )

                        in_code_block = False
                        self.rich_lines.append(Prose(line))
                    else:
                        self.rich_lines.append(entry_from_text(line))
                    continue

                self.rich_lines.append(Prose(line))
                if line == self.PLOVER_ADDS_TITLE:
                    in_adds_section = True
                    self.plover_adds_section_end_index = None

                if in_ignored_code_block:
                    if re.fullmatch(rf"{in_ignored_code_block}\s*\n", line):
                        in_ignored_code_block = None
                else:
                    code_block_match = code_block_start_pattern.fullmatch(line)
                    if code_block_match:
                        (ticks,) = code_block_match.groups()
                        in_code_block = ticks
                    else:
                        ignored_block_match = (
                            ignored_code_block_start_pattern.fullmatch(line)
                        )
                        if ignored_block_match:
                            (ticks,) = ignored_block_match.groups()
                            in_ignored_code_block = ticks
            except Exception as e:
                raise Exception(f"Problem on line {i}: '{line}'") from e

        if in_code_block or in_ignored_code_block:
            raise ValueError("Found unclosed code block(s) at end of file")

        self.update(
            {
                entry.key: entry.updated_value
                for entry in self.rich_lines
                if entry.kind == "entry" and not entry.is_deleted
            }
        )

    def _save(self, filename):
        self.rich_lines = [line for line in self.rich_lines if not line.is_new]

        for entry in self.rich_lines:
            if entry.kind == "entry":
                current_value = self._dict.get(entry.key)
                entry.updated_value = current_value
                if entry.is_new:
                    entry.value = current_value
                entry.is_deleted = current_value is None

        new_adds_lines = []
        known_keys = [entry.key for entry in self.rich_lines if entry.kind == "entry"]
        new_keys = [key for key in self._dict.keys() if key not in known_keys]

        for new_key in new_keys:
            new_value = self._dict.get(new_key)
            if new_value:
                key_quote = (
                    '"'
                    if (new_key[0].startswith("#") or new_key[0].startswith("*"))
                    else ""
                )

                value_quote = ""
                if (
                    '"' not in new_value
                    and (
                        new_value.startswith(" ")
                        or new_value.endswith(" ")
                        or "'" in new_value
                        or "#" in new_value
                    )
                    or ('"' in new_value and "'" in new_value)
                ):
                    value_quote = '"'
                elif "'" not in new_value and (
                    new_value.startswith(" ")
                    or new_value.endswith(" ")
                    or '"' in new_value
                    or "#" in new_value
                ):
                    value_quote = "'"

                new_adds_lines.append(
                    Entry(
                        key=new_key,
                        key_quote=key_quote,
                        value=new_value,
                        updated_value=new_value,
                        value_quote=value_quote,
                        separator=": ",
                        comment_padding="",
                        comment="",
                        is_deleted=False,
                        is_new=True,
                    )
                )

        if len(new_adds_lines) > 0:
            if self.plover_adds_section_end_index:
                self.rich_lines[
                    self.plover_adds_section_end_index : self.plover_adds_section_end_index
                ] = new_adds_lines
            else:
                self.rich_lines.append(Prose("\n", True))
                self.rich_lines.append(Prose(self.PLOVER_ADDS_TITLE, True))
                self.rich_lines.append(Prose("\n", True))
                self.rich_lines.append(Prose("```yaml\n", True))
                self.rich_lines.extend(new_adds_lines)
                self.rich_lines.append(Prose("```\n", True))

        with open(filename, "w") as f:
            f.write("".join([str(rich_line) for rich_line in self.rich_lines]))
