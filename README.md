# Website Downloader

A Python script to download a website and store it locally for offline access.

## Requirements

- Python 3.x
- `wget` command line tool

## Installation

1. Clone or download this repository to your local machine.
2. Install the required dependencies by running the following command in your terminal:

``bash
pip install -r requirements.txt

## Usage

To download a website, run the `download_website.py` script and provide the URL of the website you want to download, as well as the directory where you want to save the downloaded files:

``bash
python download_website.py

The script will display a progress bar as the website is being downloaded. If the download is interrupted for any reason, you can resume it by running the same command again.

By default, the script will download the entire website. If you want to limit the download size, you can provide a maximum size (in megabytes) using the following command:

``bash
python download_website.py --max-size <size>

Replace `<size>` with the maximum size you want to allow for the download.

## Example

To download the OpenAI homepage and save it to the directory `/home/user/Downloads/OpenAI`, run the following command:

``bash
python download_website.py --url https://accessquote.netlify.app/ --output /home/user/Downloads/OpenAI

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## Acknowledgements

This project uses the following open source libraries:

- [wget](https://pypi.org/project/wget/) - For downloading the website files.
- [tqdm](https://pypi.org/project/tqdm/) - For displaying the progress bar.

## Disclaimer

Please be aware that downloading websites without permission may violate copyright laws in some countries. Use this script responsibly and only download websites that you have permission to access.

## Contact

If you have any questions or comments about this project, please feel free to contact me at [your-email@example.com](mailto:your-email@example.com).
