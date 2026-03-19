from pathlib import Path
from typing import Dict, List

from pypdf import PdfReader

# DATA_PATH = Path("data/pdfs")

"""
Doc loader function.
Load every pdf, with source and pages.
"""

def load_pdfs(data_path:str) -> List[Dict]:
    documents = []
    DATA_PATH = Path(data_path)
    # Load the list of pdfs.
    pdf_files = DATA_PATH.glob("*.pdf")

    for pdf_file in pdf_files:
        # Read the pages and text.
        reader = PdfReader(pdf_file)

        # organize page and text
        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()
            # Clean white space in leadin & trailing
            if text and text.strip():
                documents.append(
                    {
                        "content": text,
                        "metadata":{
                            "source": pdf_file.name,
                            "page": page_number + 1
                        }
                    }
                )

    return documents


if __name__=='__main__':
    documentos = load_pdfs("data/pdfs")

    print(f"number of pages: {len(documentos)}")
    print("*"*100)
    # print(documentos[114]["content"])
    print(documentos[:2])