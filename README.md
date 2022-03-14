# Plover Markdown Dictionary

This is a markdown file with embedded code blocks, in the style of literate programming. Each code block contains a YAML-like bit of text defining your entries.

This project was borne out of a desire for a dictionary format with these features:

- easy to read and write by hand
- simple for non programmers
- allows comments
- editable (add/update/delete) through the Plover interface, without losing comments

## Table of Contents

- [Installation](#installation)
  - [Git version](#git-version)
  - [Status](#status)
  - [For development](#for-development)
- [Format](#format)
  - [Where to put your definitions](#where-to-put-your-definitions)
  - [Definition Format](#definition-format)
  - [Comments](#comments)
  - [Repeat definitions](#repeat-definitions)
- [GUI Behaviour](#gui-behaviour)
  - [Adding](#adding)
  - [Deleting](#deleting)
  - [Updating](#updating)
- [Converting to/from other formats](#converting-tofrom-other-formats)
- [Example](#example)
- [Notes](#notes)
  - [Alternative dictionary formats](#alternative-dictionary-formats)
  - [Performance](#performance)
  - [Why use `(UPDATED)` or `(DELETED)` tags?](#why-use-updated-or-deleted-tags)
  - [Why this definition format?](#why-this-definition-format)
  - [Contributing](#contributing)

## Installation

Install via the Plover plugin manager.

### Git version

On the [command-line](https://plover.readthedocs.io/en/latest/cli_reference.html) (requires git):

```bash
plover -s plover_plugins install git+https://github.com/antistic/plover_markdown_dictionary.git
```

### Status

This plugin is experimental and might have some bugs. Feel free to [open an issue](./issues/new) if you find one, and read the changelog when upgrading.

### For development

```bash
git clone https://github.com/antistic/plover_markdown_dictionary
cd plover_markdown_dictionary
plover -s plover_plugins install -e .
```

## Format

- It's a Markdown file, so you can do all the [Markdown formatting](https://commonmark.org/help/) you like!

### Where to put your definitions

- Put your definitions in code blocks.

```
HRAOEUBG: like
TH: this
```

which in markdown looks

````md
```
HRAOEUBG: like
TH: this
```
````

- You can set the syntax formatting language to YAML

> **Note:** Although it looks like yaml, it isn't yaml.

```yaml
TH/STEUL: this still
WORBGS: works
```

which in markdown looks like

````md
```yaml
TH/STEUL: this still
WORBGS: works
```
````

- Code blocks defined as other formats will not be read as dictionary definitions. This makes it easy to comment out sections.

```text
KOPLT/-D: commented
OUT: out
```

which looks like

````md
```text
KOPLT/-D: commented
OUT: out
```
````

- `Inline` code blocks are will not be read as dictionary definitions.

- Code blocks defined by indentation (e.g. 4 spaces) will not be read as dictionary definitions.

### Definition Format

- The basic format is `STROKES: translation`. Both the left and right side of the colon are treated as strings, even though they may not be in YAML.

```yaml
#S: 1
2: 2
-T: the
*UR: you are
KWRE: yes
```

- You can quote these if you wish to preserve syntax formatting

```
'#S': '1'          # single quotes
'2': '2'
"-T": the           # double quotes
"*UR": you are
KWRE: "yes"
```

- There are some characters you will need to escape:

```yaml
SKW-T: \' # single quote character
KR-GS: \" # double quote character
HAERB: \# # hash character on the right hand side
'#-T': 9 # you should not escape the # in strokes
PW-RB: \\ # backslash
R-R: \\n # newline
R*R: \\r # other newline
TAB: \\t # tab
```

- But you might prefer to use quotes:

```yaml
SKW-T: "'"
KR-GS: '"'  # you can quote double quotes with single quotes
HAERB: '#'
PW-RB: "\\" # backslashes always need escaping, whether they're in quotes or not
R-R: "\\n" # same with newlines
R*R: "\\r"
TAB: "\\t" # and tabs
S-PS: ' ' # you'll need quotes for anything with starting or trailing spaces
```

### Comments

You can use comments after entries. These must be on the same line, and they're denoted by a `#` symbol.

```yaml
K-PLT: comment # this is a comment
```

### Repeat definitions

You should avoid specifying the same stroke(s) multiple times. If you choose to do this anyway, you should assign the same translation every time. The plugin will make a best effort to update all rows of the same chord when Plover updates or deletes entries.

```yaml
REPT: reptile  # this is overridden and ignored by Plover
REPT: repeat
```

```yaml
REPT: repeat
REPT: repeat # it will only appear once in Plover, but we'll try to reflect changes everywhere
```

## GUI Behaviour

> **NOTE**: You shouldn't edit the file both in the Plover GUI and in your text editor at the same time, because it might lead to inconsistencies.<br>
> If you have edited the file manually, you can reload it in Plover by unchecking and rechecking the box next to the dictionary, or reloading with `CTRL+R`.

### Adding

When you add an entry within the Plover interface, a section is created at the bottom of the file and entries are added. If the section already exists (defined by a heading with the text 'Added via Plover' then a single code block at the bottom of the file), it will add to that block.

Example of what you'll see at the bottom of the file:

````md
## Added via Plover

```yaml
TPHU: new
SPWREUS: entries
TKPW: go
HAOER: here
```
````

### Deleting

When you delete an entry, the line in the document is updated with a `(DELETED)` prefix and will be ignored when loading the dictionary in the future.

Example of deleting `TKHRAOET/PHE: delete me`

```yaml
KP-PL: example
(DELETED) TKHRAOET/PHE: delete me # this is ignored by Plover
TEGT: text
```

### Updating

When the translation is updated, the entry in the document is updated in place, and annotated with an `(UPDATED)` prefix for legibility; it is still read as normal by Plover.

Example of changing `KP-L: example` to `KP-L: excel`

```yaml
KP-PL: example
(UPDATED) KP-L: excel
KPW-PL: example
```

When the stroke is updated it is treated like a deletion of the old entry then the addition of the new one.

## Converting to/from other formats

1. In the dictionaries list, select the dictionaries you want to convert.
2. Right click, choose "Save dictionaries as...".
3. Choose whether you want to create a copy of each dictionary, or merge into a new one.
4. In the save file dialog, choose where to save the dictionary. To convert to JSON, save with the extension ".json". To convert to Markdown, save with the extension ".md".

## Example

This file is an example! You can see the raw markdown [here](https://raw.githubusercontent.com/antistic/plover_markdown_dictionary/main/README.md).

It is equivalent to [example.json](./example.json).

## Notes

This format is a work in progress and I'd love to get feedback on what works or doesn't work for you!

### Alternative dictionary formats

There are other plover dictionary formats that allow comments, but all of them have something that means they don't fit my original goals (as of June 2021).

| format                                                     | comments                                                                                                                                                            |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Excel](https://pypi.org/project/plover-excel-dictionary/) | Dropped support for keeping comments on changing translations (in the form of other columns) in version 1.0.0                                                       |
| [yaml](https://pypi.org/project/plover-yaml-dictionary/)   | Does not support keeping comments, citing performance reasons. Yaml also has weird catches with strings, like needing "no" in quotes (otherwise parsed as boolean). |
| rtf/cre ([built-in support][rtf-1], [better-rtf][rtf-2])   | The format is hard to read (personal opinion)                                                                                                                       |
| [hjson](https://pypi.org/project/plover-hjson-dictionary/) | Does not support keeping comments on dictionary updates                                                                                                             |

[rtf-1]: https://github.com/openstenoproject/plover/wiki/Supported-formats#rtf-aka-cre

[rtf-2]: https://pypi.org/project/plover-better-rtf/

### Performance

Basic tests with the plover main dictionary using [time.py](.scripts/time.py) on my laptop.

I haven't tried very hard to optimise this, so it's probably possible to go faster.

| Test                          | Time  |
| ----------------------------- | ----- |
| Load JSON                     | 0.44s |
| Load JSON + Save JSON         | 1.15s |
| Load JSON + Save Markdown     | 1.52s |
| Load Markdown                 | 1.48s |
| Load Markdown + Save Markdown | 2.36s |

### Why use `(UPDATED)` or `(DELETED)` tags?

It's important that people know what's been changed so that they can make sure any description or comment stays up to date.

This could have been done via a version control system like git, but git requires a learning curve that non-programmers might not be comfortable with. Since people are likely to have to update the surrounding comments anyway, I thought it would not be too much work to remove the tags.

For those who are comfortable, you can always clone this repository, alter `DELETED_PREFIX` and `UPDATED_PREFIX` in [./plover\_markdown\_dictionary.py](./plover_markdown_dictionary.py), and install your local version with `plover -s plover_plugins install -e .`.

### Why this definition format?

json does not support comments. hjson (& other json extensions) and yaml are are not performant enough to be viable (according to the people making the dictionary plugins. I haven't tried).

This particular format was chosen to be easy to read and write. It looks very similar to the default json, but does not require quotes nor commas. One downside is that it's not easy to copy and paste between this format and the default json, but I haven't decided how important that is for the format yet.

I've also gone for an unstructured format for metadata (comments and Markdown) since other formats (e.g. JSON) are probably better structured metadata.

### Contributing

If you have any questions or problems, feel free to open an issue! I'll also gladly take suggestions in the form of pull requests as well.
