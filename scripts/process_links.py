import typer
import json
import os
import requests
import logging
from urllib.parse import urlparse, unquote

app = typer.Typer()

# Set up logging
logging.basicConfig(level=logging.INFO)

def download_file(url, folder):
    """
    Download a file from a given URL into a specified folder.
    
    Args:
    url: URL of the file to download.
    folder: Folder where the file should be saved.
    """
    # Extract the file name from the URL
    file_name = unquote(urlparse(url).path.split('/')[-1])
    file_path = os.path.join(folder, file_name)

    # Check if file already exists
    if os.path.exists(file_path):
        logging.info(f"File already exists: {file_name}, skipping download.")
        return file_name

    # Download and save the file
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
        logging.info(f"File downloaded and saved: {file_name}")

    return file_name

@app.command()
def process_links(jsonl_file_path: str):
    """
    Process links from a JSONL file to download files into organized year folders.
    
    Args:
    jsonl_file_path: Path to the JSONL file containing links to process.
    """
    # Create data folder if it doesn't exist
    data_folder = 'data'  # Adjusted from '/data/' for relative path
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        logging.info(f"Data folder created at {data_folder}")

    with open(jsonl_file_path, 'r') as file:
        for line in file:
            # Load the link as a dictionary
            link_dict = json.loads(line)
            url = link_dict['link']

            # Extract the year from the URL
            year = url.split('/')[-3] # Adjust the index if necessary based on the URL structure

            # Create a subfolder for the year if it doesn't exist
            year_folder = os.path.join(data_folder, year)
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)
                logging.info(f"Created sub-folder: {year_folder}")

            # Download the file
            download_file(url, year_folder)

if __name__ == "__main__":
    app()
