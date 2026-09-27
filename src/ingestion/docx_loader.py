from pathlib import Path
from docx import Document


def load_docx(path):

    path = Path(path)

    document = Document(path)

    text = "\n".join(paragraph.text
                     for paragraph in document.paragraphs
                     if paragraph.text.strip())

    return [{"text": text,
             "metadata": {"source": path.name,
                          "file_type": "docx"}}]