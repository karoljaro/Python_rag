from pathlib import Path
import pandas as pd


def load_txt_file(folder: str) -> pd.DataFrame:
    data = []

    for filepath in Path(folder).glob("*.txt"):
        with open(filepath, "r", encoding="utf-8") as file:
            data.append({"filename": filepath.name, "content": file.read()})

    return pd.DataFrame(data)
