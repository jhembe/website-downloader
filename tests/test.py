import os
import requests
import sys
from tqdm import tqdm

url = sys.argv[1]
filename = os.path.basename(url)

# Check if file already exists and prompt user to resume or overwrite
if os.path.exists(filename):
    choice = input("File already exists. Do you want to resume the download (r) or overwrite the existing file (o)? ")
    if choice == 'r':
        resume_header = {'Range': f'bytes={os.path.getsize(filename)}-'}
        response = requests.get(url, headers=resume_header, stream=True)
        mode = 'ab'
        total_size = int(response.headers.get('content-length', 0)) + os.path.getsize(filename)
    else:
        response = requests.get(url, stream=True)
        mode = 'wb'
        total_size = int(response.headers.get('content-length', 0))
else:
    response = requests.get(url, stream=True)
    mode = 'wb'
    total_size = int(response.headers.get('content-length', 0))

# Download the file
if response.status_code == 200:
    with open(filename, mode) as file, tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                file.flush()
                if total_size > 0:
                    pbar.update(len(chunk))
else:
    print(f"Download failed with status code {response.status_code}")
