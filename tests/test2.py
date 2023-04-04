import os
import requests
from tqdm import tqdm

url = input("Enter URL to download: ")
response = requests.get(url, stream=True)

total_size = int(response.headers.get('content-length', 0))
filename = os.path.basename(url)

if not filename:
    filename = 'index.html'

mode = 'wb'

with open(filename, mode) as file, tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
    for data in response.iter_content(chunk_size=1024):
        # write data read to the file
        file.write(data)
        
        # update the progress bar
        pbar.update(len(data))
