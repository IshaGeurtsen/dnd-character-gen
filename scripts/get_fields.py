from pathlib import Path
from pypdf import PdfReader  # type: ignore
from os import fspath
from collections import OrderedDict
from typing import Optional
import json

if __name__ == "__main__":
    sheets = Path.cwd() / "doc" / "gen" / "5e-CHARACTERSHEETS"
    form = sheets / "DnD_5E_CharacterSheet - Form Fillable.pdf"
    page_paths = [
        sheets / "Character Sheet - Form Fillable.pdf",
        sheets / "Character Details (Optional) - Form Fillable.pdf",
        sheets / "Spellcasting Sheet (Optional) - Form Fillable.pdf",
    ]
    output: dict[str, dict[str, Optional[str]]] = OrderedDict()

    for page_path in page_paths:
        reader = PdfReader(fspath(page_path))
        output[fspath(page_path)] = reader.get_form_text_fields()
    for name in output:
        for key in output[name]:
            if not output[name][key]:
                output[name][key] = None
    form_layout = Path.cwd() / "doc" / "gen" / "form_layout.json"
    with open(form_layout, "wt") as file:
        json.dump(
            output,
            file,
            allow_nan=False,
            indent=4,
            separators=(
                ", ",
                ": ",
            ),
        )
