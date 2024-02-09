import typer
import json
import os
import requests
import logging
import re
from urllib.parse import urlparse, unquote
from pathlib import Path

app = typer.Typer()

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_year_from_path(file_path: Path):
    """Extract the year from the file path."""
    year_match = re.search(r'/(\d{4})/', str(file_path))
    if year_match:
        return year_match.group(1)
    return None

def get_category(file_name: str):
    """Determine the category of a file based on regex pattern matching in its filename."""
    patterns = {
        'supplement': re.compile(r'supplement', re.IGNORECASE),
        'agenda': re.compile(r'agenda', re.IGNORECASE),
        'minutes': re.compile(r'minutes', re.IGNORECASE),
    }
    for category, pattern in patterns.items():
        if re.search(pattern, file_name):
            return category
    return None

def download_file(url, base_folder):
    """
    Download a file from a given URL into a specified category and year folder.
    
    Args:
    url: URL of the file to download.
    base_folder: Base folder where the file should be categorized and saved.
    """
    # Extract the file name from the URL
    file_name = unquote(urlparse(url).path.split('/')[-1])
    
    # Determine the category of the file
    category = get_category(file_name)
    if not category:
        category = "uncategorized"
    
    # Assume year from the URL or set a default one
    year = "unknown"
    year_match = re.search(r'/(\d{4})/', url)
    if year_match:
        year = year_match.group(1)
    
    # Construct the category and year folder path
    category_folder = os.path.join(base_folder, category)
    year_folder = os.path.join(category_folder, year)
    
    # Create the year folder if it doesn't exist
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
        logging.info(f"Created folder: {year_folder}")
    
    file_path = os.path.join(year_folder, file_name)

    # Check if file already exists
    if os.path.exists(file_path):
        logging.info(f"File already exists: {file_name}, skipping download.")
        return file_name

    # Download and save the file
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
        logging.info(f"File downloaded and saved in {category}/{year}: {file_name}")

    return file_name

@app.command()
def process_links(jsonl_file_path: str):
    """
    Process links from a JSONL file to download files into organized category and year folders.
    
    Args:
    jsonl_file_path: Path to the JSONL file containing links to process.
    """
    # Create base data folder if it doesn't exist
    data_folder = 'data'  # Adjusted from '/data/' for relative path
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        logging.info(f"Data folder created at {data_folder}")

    with open(jsonl_file_path, 'r') as file:
        for line in file:
            # Load the link as a dictionary
            link_dict = json.loads(line)
            url = link_dict['link']

            # Download the file into the categorized and year-organized folder
            download_file(url, data_folder)

if __name__ == "__main__":
    app()

