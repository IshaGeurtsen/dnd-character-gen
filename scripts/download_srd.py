from pathlib import Path
import requests

url = "https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf"
pdf_path = Path.cwd() / "doc" / "gen" / "SRD_CC_v5.1.pdf"

if __name__ == "__main__":
    response = requests.get(url)
    response.raise_for_status()
    pdf_path.write_bytes(response.content)
