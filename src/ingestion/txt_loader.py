from pathlib import Path


def load_txt(path):

    path = Path(path)

    text = path.read_text(encoding="utf-8")

    return {"text": text,
            "metadata": {"source": path.name,
                         "file_type": "txt"}}