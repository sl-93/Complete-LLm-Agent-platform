from pathlib import Path
from pypdf import PdfReader


def load_pdf(path):

    path = Path(path)

    reader = PdfReader(path)

    documents = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if not text:
            continue

        documents.append({"text": text, 
                          "metadata": {"source": path.name,
                                       "file_type": "pdf",
                                       "page": page_number + 1}})

    return documents