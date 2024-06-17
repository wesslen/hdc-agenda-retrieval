import os
import json
import requests
import time
import typer

def save_md_files(input_path: str, output_path: str, override_save: bool = False) -> None:
    """
    Take a .jsonl file and save each of the .md files specified in the 'md_file' key.

    Args:
        input_path (str): Path to the .jsonl file
        output_path (str): Path to the output folder where the .md files will be saved
        override_save (bool): Whether to save the file even if it already exists (default: False)
    """
    start_time = time.time()
    request_count = 0
    with open(input_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            md_file_url = data['md_file']
            md_file_path = os.path.join(output_path, md_file_url.split('data/')[1] + '.md')
            os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
            if not os.path.exists(md_file_path) or override_save:
                response = requests.get(md_file_url)
                request_count += 1
                if response.status_code == 200:
                    with open(md_file_path, 'w') as md_file:
                        md_file.write(response.text)
                else:
                    print(f"Failed to download {md_file_url}")
                if request_count >= 25:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 60:
                        time.sleep(60 - elapsed_time)
                    request_count = 0
                    start_time = time.time()
            else:
                print(f"Skipping {md_file_path} as it already exists")

if __name__ == '__main__':
    typer.run(save_md_files)