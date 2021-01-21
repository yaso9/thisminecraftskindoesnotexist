import os
import argparse
from uuid import uuid4
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download minecraft skins from planet minecraft."
    )
    parser.add_argument("pages", type=int, help="the number of pages to scrape")
    args = parser.parse_args()

    for page in tqdm(range(1, args.pages + 1), position=0):
        soup = BeautifulSoup(
            requests.get(get_url(page), headers=HEADERS).text, features="html.parser"
        )

        # Get the paths for all the skins on the page
        paths = [el["href"] for el in soup.findAll("a", {"class": "r-title"})]

        for skin_path in tqdm(paths, position=1):
            soup = BeautifulSoup(
                requests.get(resolve_path(skin_path), headers=HEADERS).text,
                features="html.parser",
            )

            # Extract the url to download the skin
            download_path = soup.find("a", {"title": "Download "})["href"]
            with open(os.path.join(SAVE_PATH, f"{uuid4()}.png"), "wb") as file:
                file.write(
                    requests.get(resolve_path(download_path), headers=HEADERS).content
                )
