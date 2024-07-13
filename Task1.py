import os
import shutil
import asyncio
import aiofiles
import logging
import argparse

# Setting up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path, output_folder):
    try:
        _, extension = os.path.splitext(file_path)
        extension = extension[1:]  # Remove the dot from the extension
        target_folder = os.path.join(output_folder, extension)

        # Create target folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)

        # Copy file to the target folder
        target_path = os.path.join(target_folder, os.path.basename(file_path))
        async with aiofiles.open(file_path, 'rb') as src:
            async with aiofiles.open(target_path, 'wb') as dest:
                await dest.write(await src.read())
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")

async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            tasks.append(copy_file(file_path, output_folder))

    await asyncio.gather(*tasks)

# Function to run the asynchronous code
def run_async_function(func):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        task = loop.create_task(func)
    else:
        asyncio.run(func)

# Argument parser setup
def main():
    parser = argparse.ArgumentParser(description="Copy and organize files by extension asynchronously.")
    parser.add_argument('source_folder', type=str, nargs='?', default='/Users/HP/Desktop/4_Computer_systems_Tier2/goit-cs-hw-05/Folder2', help="The source folder to read files from.")
    parser.add_argument('output_folder', type=str, nargs='?', default='/Users/HP/Desktop/4_Computer_systems_Tier2/goit-cs-hw-05/Folder1', help="The output folder to copy files to.")
    args = parser.parse_args()

    source_folder = args.source_folder
    output_folder = args.output_folder

    # Execute the asynchronous file sorting
    run_async_function(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()

