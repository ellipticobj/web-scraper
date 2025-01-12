import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def cleanfilenamefromurl(url: str) -> str:
    parsedurl = urlparse(url)
    filename = os.path.basename(parsedurl.path)
    return filename


def download(url: str, savepath: str = "./scraperdownloads/"):
    filename = cleanfilenamefromurl(url)
    filename = os.path.join(savepath, filename)

    print(f"downloading {filename}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"downloaded {filename}")
        return filename

    else:
        print(f"failed to download {filename}")

def imgscraper(url: str, savepath: str = "./scraperdownloads/img/", numtoget: int = 1, blacklistedclasses: list = ['community_banner', 'thumbnail_img', 'shreddit-subreddit-icon__icon', 'avatar', ''], blacklistedalt: list = ['icon']):
    '''
    scrapes images from the specified website
    '''
    os.makedirs(savepath, exist_ok=True)
    clsblacklist = blacklistedclasses or []
    altblacklist = blacklistedalt or []

    response = requests.get(url)
    response.raise_for_status()

    if response.status_code != 200:
        print(f"failed to connect to {url}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')

    count = 0
    for imgtag in soup.find_all('img'):
        imgclasses = imgtag.get("class", [])
        imgalt = imgtag.get("alt", "")

        if any(cls in clsblacklist for cls in imgclasses):
            print(f"skipping image with blacklisted class {imgclasses}")
            continue
        
        if any(alt in altblacklist for alt in imgalt):
            print(f"skipping image with blacklisted alt {imgalt}")
            continue

        imgurl = urljoin(url, imgtag.get("src"))
        if imgurl:
            try:
                filename = download(imgurl, savepath)
                count += 1
                print(f"scraped image: {filename}")
            except Exception as e:
                print(f"failed to scrape image {imgurl}: {e}")
        
        if count >= numtoget:
            break

    print(f"scraped {numtoget} images")
    print(f"stored at {savepath}")

# TODO: remove this when shipping
imgscraper("https://reddit.com/r/femboy")

def vidscraper(url: str, savepath: str="./scraperdownloads/vids/", numtoget: int = 1):
    '''
    scrapes images video from the specified website
    '''
    os.makedirs(savepath, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    if response.status_code != 200:
        print(f"failed to connect to {url}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')

    count = 0
    for vidtag in soup.find('video'):
        videosources = vidtag.findall("source")
        for source in videosources:
            vidurl = urljoin(url, source.get("src"))
            if vidurl:
                try:
                    filename = download(vidurl, savepath)
                    count += 1
                    print(f"scraped video: {filename}")
                except Exception as e:
                    print(f"failed to scrape video {vidurl}: {e}")
        
        if count >= numtoget:
            break

    print(f"scraped {numtoget} videos")
    print(f"stored at {savepath}")
