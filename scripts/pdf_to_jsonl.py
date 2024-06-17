import os
import json
import hashlib
import typer

def pdf_to_jsonl(input_path: str, output_path: str) -> None:
    """
    Take a folder of PDFs (including subfolders) and output a .jsonl file with the names of all the PDF files,
    along with a unique 'id' key and hash value based on pdf_file, and a new field called 'md_file'.

    Args:
        input_path (str): Path to the folder of PDFs
        output_path (str): Path to the output .jsonl file
    """
    base_url = 'https://r.jina.ai/https://wesslen.github.io/hdc-agenda-retrieval/'
    with open(output_path, 'w') as f:
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file = os.path.join(root, file)
                    pdf_id = hashlib.md5(pdf_file.encode()).hexdigest()
                    md_file = os.path.join(base_url, pdf_file)
                    json.dump({'id': pdf_id, 'pdf_file': pdf_file, 'md_file': md_file}, f)
                    f.write('\n')

if __name__ == '__main__':
    typer.run(pdf_to_jsonl)