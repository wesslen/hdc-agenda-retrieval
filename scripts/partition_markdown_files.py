import os
import typer
from unstructured.partition.md import partition_md

app = typer.Typer()

@app.command()
def partition_markdown_files(input_path: str, output_path: str):
    """
    Partition a folder of markdown files using unstructured.

    Args:
        input_path (str): Path to the folder containing markdown files.
        output_path (str): Path to the output folder where partitioned files will be saved.
    """
    if not os.path.exists(input_path):
        typer.echo(f"Error: Input path '{input_path}' does not exist.")
        raise typer.Exit(1)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    md_text = f.read()
                partitions = partition_md(md_text)
                output_file_path = os.path.join(output_path, file)
                with open(output_file_path, 'w') as f:
                    for partition in partitions:
                        f.write(partition + '\n\n')

    typer.echo(f"Partitioned markdown files saved to '{output_path}'")

if __name__ == "__main__":
    app()