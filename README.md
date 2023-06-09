# Website Downloader

A Python script to download a website and store it locally for offline access.

## Requirements

- Python 3.x
- `wget` command line tool

## Installation

1. Clone or download this repository to your local machine.

    ```bash
    git clone https://github.com/jhembe/website-downloader.git
    ```

2. Install the required dependencies by running the following command in your terminal:

    ```bash
    cd website-downloader
    ```

    ```bash
    pip install pipenv
    ```

    ```bash
    pipenv install

    ```

    ```bash
    pipenv shell
    ```

## Usage

To download a website, run the `download_website.py`, you'll be asked to provide the URL of the website you want to download, as well as the size of data you want to download (for v1 variant)

```bash
python download_website.py
```

The script will display a progress bar as the website is being downloaded. If the download is interrupted for any reason, you can resume it by running the same command again.

By default, the script will download the entire website. If you want to limit the download size, you can provide a maximum size (in megabytes) using the following command:

![A Screenshot](./assets/screen.png)


## Example

To download my accessquote site and save it to the directory `/home/user/{username}/localWebsites`, run the following command:

```bash
python download_website.py
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## Acknowledgements

This project uses the following open source libraries:

- [requests](https://pypi.org/project/requests/) - For downloading the website files.
- [tqdm](https://pypi.org/project/tqdm/) - For displaying the progress bar.
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) - For parsing HTML and XML documents.
- [certifi](https://pypi.org/project/certifi/) - For providing Mozilla's CA Bundle for SSL verification.
- [charset-normalizer](https://pypi.org/project/charset-normalizer/) - For detecting the character encoding of downloaded content.

## Disclaimer

Please be aware that downloading websites without permission may violate copyright laws in some countries. Use this script responsibly and only download websites that you have permission to access.

## Contact

If you have any questions or comments about this project, please feel free to contact me at [jhembe202@gmail.com](mailto:jhembe202@gmail.com).
