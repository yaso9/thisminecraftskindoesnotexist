import os
import argparse
from uuid import uuid4
import xml.etree.ElementTree as ET
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Path to the folder in which to store downloaded skins
SAVE_PATH = "../data/raw"

# Set the user agent to mimic Chrome
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

# Convert a path to the full planet minecraft url
def resolve_path(path):
    return f"https://www.planetminecraft.com{path}"


# Get the URL for a given page number.
def get_url(page):
    return resolve_path(f"/skins/human/?op2=0&p={page}")


def extract_skin_download_links(url):
    try:
        soup = BeautifulSoup(
            requests.get(url, headers=HEADERS).text,
            features="html.parser",
        )

        # Extract the url to download the skin
        return resolve_path(soup.find("a", {"title": "Download "})["href"])
    except:
        return None


# Download file
def download_file(url):
    try:
        with open(os.path.join(SAVE_PATH, f"{uuid4()}.png"), "wb") as file:
            file.write(requests.get(url, headers=HEADERS).content)
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download minecraft skins from planet minecraft."
    )
    parser.add_argument(
        "sitemap", type=str, help="the planet minecraft sitemap url to use"
    )
    parser.add_argument("skins", type=int, help="the number of skins to download")
    args = parser.parse_args()

    # Get skin page urls
    root = ET.fromstring(
        requests.get(
            args.sitemap,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
            },
        ).text
    )
    urls = [
        el.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
        for el in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        if el.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text.startswith(
            "https://www.planetminecraft.com/skin"
        )
    ][: args.skins]

    with Pool(256) as p:
        list(
            tqdm(
                p.imap_unordered(
                    download_file,
                    filter(
                        lambda x: x is not None,
                        tqdm(
                            p.imap_unordered(extract_skin_download_links, urls),
                            total=len(urls),
                        ),
                    ),
                ),
                total=len(urls),
            )
        )
