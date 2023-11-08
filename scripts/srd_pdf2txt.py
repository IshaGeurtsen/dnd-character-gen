from pathlib import Path
from os import fspath
from tika import parser  # type: ignore
import re
import string

translation_table = str.maketrans(
    {
        0xA0: " ",
        0xAD: None,
        0xD7: "*",
        0x336: "-",
        0x2010: "-",
        0x2011: "-",
        0x2012: "-",
        0x2013: "-",
        0x2014: "-",
        0x2019: "'",
        0x201C: '"',
        0x201D: '"',
        0x2022: "*",
        0x2028: "\n",
        0x2212: "-",
    }
)


def improve_text(text: str) -> str:
    text = text.translate(translation_table)
    text = text.replace(chr(0x2026), "...")
    # remove a lot of empty newlines
    text = re.sub("\n{2,}", "\n\n", text)
    # join paragraphs
    text = re.sub("\t\r  ", " ", text)
    text = re.sub(r"(?<=\w) \n(?=[a-z])", " ", text)
    # replace remaining tabs with spaces
    text = re.sub(r"\n\t(?=\w)", "\n    ", text)
    # shorten multiple dashes
    text = re.sub("--{2,}", "-", text)
    # remove trailing whitespace
    text = re.sub(" +(?=\n)", "", text)
    text = text.strip() + "\n"
    return text


if __name__ == "__main__":
    cwd = Path.cwd()

    srd = cwd / "doc" / "gen" / "SRD_CC_v5.1.pdf"
    srd_text = cwd / "doc" / "gen" / "SRD.txt"

    parsed = parser.from_file(fspath(srd))
    text = parsed["content"]

    text = improve_text(text)

    assert isinstance(text, str)
    known = {
        *string.digits,
        *string.ascii_letters,
        *string.punctuation,
        "\n",
        " ",
        "\r",
        chr(189),
    }
    unkown = set(text) - known
    assert not unkown

    with open(srd_text, "wb") as out:
        out.write(text.encode(encoding="utf-8"))
