import requests
import tkinter as tk
from tkinter import ttk

# Configuration
repo_owner = 'SlovakTastic'
repo_name = 'LearnAPP'
branch_name = 'main'  # Replace with the branch you want to fetch files from
file_paths = [
    'external/2-grade/matematika/chapter/subchapters/subchapter.py'
]  # List of files you want to download

api_base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'

def get_file_download_url(file_path):
    url = f'{api_base_url}/contents/{file_path}?ref={branch_name}'
    response = requests.get(url)
    response.raise_for_status()
    file_data = response.json()
    return file_data['download_url']

def download_file(file_url, local_filename, progress_var):
    response = requests.get(file_url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192

    with open(local_filename, 'wb') as file:
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                # Update progress bar in the GUI
                progress_var.set((downloaded_size / total_size) * 100)
                window.update_idletasks()

def start_download():
    for file_path in file_paths:
        try:
            file_url = get_file_download_url(file_path)
            local_filename = file_path.split('/')[-1]
            print(f'Downloading {file_path} from {file_url}...')
            download_file(file_url, local_filename, progress_var)
            print(f'{file_path} downloaded successfully.')
        except requests.RequestException as e:
            print(f'Error occurred while downloading {file_path}: {e}')

# GUI setup
window = tk.Tk()
window.title("Download Progress")

# Create and pack a label and progress bar
label = tk.Label(window, text="Downloading files...")
label.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, maximum=100, variable=progress_var)
progress_bar.pack(pady=10, padx=20, fill=tk.X)

# Start the download process with progress
def start_download_with_progress():
    try:
        start_download()
    except Exception as e:
        print(f'Error occurred: {e}')

# Start the download process
start_download_with_progress()

# Start the Tkinter main loop
window.mainloop()
