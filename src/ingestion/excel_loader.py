import pandas as pd
from pathlib import Path


def load_excel(path):

    path = Path(path)

    sheets = pd.read_excel(path,
                           sheet_name=None)

    documents = []

    for sheet_name, df in sheets.items():

        text = df.to_string(index=False)

        documents.append({"text": text,
                          "metadata": {"source": path.name,
                                       "file_type": "xlsx",
                                       "sheet": sheet_name}})

    return documents