from pathlib import Path
from .txt_loader import load_txt
from .pdf_loader import load_pdf
from .docx_loader import load_docx
from .excel_loader import load_excel

class LoadFiles:
    def __init__(self,
                 directory_path):
        self.directory_path = directory_path

    def load_file(self,
                  path):

        path = Path(path)

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return [load_txt(path)]

        elif suffix == ".pdf":
            return load_pdf(path)

        elif suffix == ".docx":
            return load_docx(path)

        elif suffix in [".xlsx", ".xls"]:
            return load_excel(path)

        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def load_directory(self):

        directory = Path(self.directory_path)

        all_documents = []
        for path in directory.iterdir():
            if not path.is_file():
                continue

            try:
                documents = self.load_file(path)

                all_documents.extend(documents)

            except ValueError as e:
                print(e)

        return all_documents