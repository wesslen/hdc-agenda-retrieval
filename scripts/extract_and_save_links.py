import typer
from bs4 import BeautifulSoup
import json
from datetime import datetime

app = typer.Typer()

@app.command()
def extract_and_save_links(html_file_path: str, output_jsonl_file: str = "data/output_links.jsonl"):
    """
    Extracts links from the given HTML file and saves them as a JSONL file.
    
    Args:
    html_file_path: The path to the HTML file to process.
    output_jsonl_file: The path where the output JSONL file will be saved.
    """
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Find all links and add the current date to each link dictionary
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append({
            "link": f"https://www.charlottenc.gov{a_tag['href']}",
            "date": current_date  # Add the current date
        })

    # Write links to a .jsonl file
    with open(output_jsonl_file, 'w', encoding='utf-8') as file:
        for link in links:
            json_record = json.dumps(link)
            file.write(json_record + '\n')
    
    print(f"Links extracted and saved to {output_jsonl_file}")

if __name__ == "__main__":
    app()


