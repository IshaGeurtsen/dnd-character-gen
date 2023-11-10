from pathlib import Path

import requests


url = "https://media.wizards.com/2022/dnd/downloads/5E-CHARACTERSHEETS.zip"
zip_path = Path.cwd() / "doc" / "gen" / "5E-CHARACTERSHEETS.zip"


if __name__ == "__main__":
    response = requests.get(url)

    response.raise_for_status()
    zip_path.write_bytes(response.content)
