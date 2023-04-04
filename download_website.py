import os
import requests
import getpass
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tqdm import tqdm


def download_website(url, output_dir):
    # Parse the base URL
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc
    site_name = parsed_url.netloc

    # Create the output directory if it doesn't exist
    output_dir = os.path.join(output_dir, site_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the initial page
    download_page(url, output_dir, base_url)

    print(f"Website downloaded successfully to {output_dir}")


def download_page(url, output_dir, base_url, processed_urls=set(), skipped_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx']):
    # Parse the URL
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]
    if file_name == '':
        file_name = 'index.html'

    # Build the local file path
    file_path = os.path.join(output_dir, file_name)

    # Skip processing if the URL has already been processed or if the file extension is in the skipped list
    if url in processed_urls or parsed_url.path.split('.')[-1] in skipped_extensions:
        return
    else:
        processed_urls.add(url)

    # Download the page if it doesn't exist locally
    if not os.path.exists(file_path):
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Failed to download page {url}: {e}")
            return

        # Write the page content to a local file
        with open(file_path, 'wb') as f:
            f.write(response.content)

    # Parse the page content and download all linked pages and resources
    try:
        with open(file_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        links = soup.find_all('a')
        images = soup.find_all('img')
        scripts = soup.find_all('script')
        stylesheets = soup.find_all('link')

        total = len(links) + len(images) + len(scripts) + len(stylesheets)
        with tqdm(total=total, desc=file_name) as pbar:
            for link in links:
                href = link.get('href')
                if href is not None:
                    absolute_url = urljoin(base_url, href)
                    if absolute_url.startswith(base_url):
                        download_page(absolute_url, output_dir, base_url, processed_urls, skipped_extensions)
                pbar.update()

            for img in images:
                src = img.get('src')
                if src is not None:
                    absolute_url = urljoin(base_url, src)
                    if absolute_url.startswith(base_url):
                        download_resource(absolute_url, output_dir, processed_urls, skipped_extensions)
                pbar.update()

            for script in scripts:
                src = script.get('src')
                if src is not None:
                    absolute_url = urljoin(base_url, src)
                    if absolute_url.startswith(base_url):
                        download_resource(absolute_url, output_dir, processed_urls, skipped_extensions)
                pbar.update()

            for stylesheet in stylesheets:
                href = stylesheet.get('href')
                if href is not None and href.endswith('.css'):
                    absolute_url = urljoin(base_url, href)
                    if absolute_url.startswith(base_url):
                        download_resource(absolute_url, output_dir, processed_urls, skipped_extensions)
                pbar.update()


    except Exception as e:
        print(f"Failed to parse page {file_path}: {e}")
        return


def download_resource(url, output_dir, processed_urls, skipped_extensions):
    # Parse the URL
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]

    # Build the local file path
    file_path = os.path.join(output_dir, file_name)

    # Skip processing if the URL has already been processed or if the file extension is in the skipped list
    if url in processed_urls or parsed_url.path.split('.')[-1] in skipped_extensions:
        return
    else:
        processed_urls.add(url)

    # Download the resource if it doesn't exist locally
    if not os.path.exists(file_path):
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Failed to download resource {url}: {e}")
            return

        # Write the resource content to a local file
        with open(file_path, 'wb') as f:
            f.write(response.content)

if __name__ == '__main__':
    user_name = getpass.getuser()
    url = input("Enter website URL: ")
    # output_dir = '/home/{username}/localWebSites'
    output_dir = f'/home/{user_name}/localWebSites'

    download_website(url, output_dir)