import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


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

        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                absolute_url = urljoin(base_url, href)
                if absolute_url.startswith(base_url):
                    download_page(absolute_url, output_dir, base_url, processed_urls, skipped_extensions)

        for img in soup.find_all('img'):
            src = img.get('src')
            if src is not None:
                absolute_url = urljoin(base_url, src)
                if absolute_url.startswith(base_url):
                    download_resource(absolute_url, output_dir, processed_urls, skipped_extensions)

        for script in soup.find_all('script'):
            src = script.get('src')
            if src is not None:
                absolute_url = urljoin(base_url, src)
                if absolute_url.startswith(base_url):
                    download_resource(absolute_url, output_dir, processed_urls, skipped_extensions)

        for link in soup.find_all('link'):
            href = link.get('href')
            if href is not None:
                absolute_url = urljoin(base_url, href)
                if absolute_url.startswith(base_url):
                    download_resource(absolute_url, output_dir, processed_urls, skipped_extensions)

    except Exception as e:
        print(f"Failed to process page {file_path}: {e}")


def download_resource(url, output_dir, processed_urls=set(), skipped_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx']):
    # Parse the URL
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]

    # Skip processing if the URL has already been processed or if the file extension is in the skipped list
    if url in processed_urls or parsed_url.path.split('.')[-1] in skipped_extensions:
        return
    else:
        processed_urls.add(url)

    # Build the local file path
    file_path = os.path.join(output_dir, file_name)

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
    url = input("Enter website URL: ")
    output_dir = '/home/jhembe/localWebSites'

    download_website(url, output_dir)
