from pathlib import Path
from zipfile import ZipFile

zip_path = Path.cwd() / "doc" / "gen" / "5E-CHARACTERSHEETS.zip"
character_sheets = Path.cwd() / "doc" / "gen" / "5e-CHARACTERSHEETS"

if __name__ == "__main__":
    character_sheets.mkdir(exist_ok=True)
    with ZipFile(zip_path, "r") as zipfile:
        for zipinfo in zipfile.infolist():
            zipfile.extract(zipinfo, character_sheets)
