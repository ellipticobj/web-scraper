import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def cleanfilenamefromurl(url: str) -> str:
    parsedurl = urlparse(url)
    filename = os.path.basename(parsedurl.path)
    return filename


def download(url: str, savepath: str = "./scraperdownloads/", name: str = None):
    filename = name or cleanfilenamefromurl(url)
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

def imgscraper(url: str, savepath: str = "./scraperdownloads/img/", numtoget: int = 1, blacklistedclasses: list = ['community_banner', 'thumbnail_img', 'shreddit-subreddit-icon__icon', 'avatar', 'preview-img', 'post-background-image-filter'], blacklistedalt: list = ['icon', 'avatar']):
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
        print()
        print()
        print(f"image {count}/{numtoget}")
        print()

        imgclasses = imgtag.get("class", [])
        imgalt = imgtag.get("alt", "")

        print(f"checking image with tags:")
        print(f"classes: {imgclasses}")
        print(f"alts: {imgalt}")

        isblacklistedclasses = [cls for cls in clsblacklist if cls in imgclasses]
        isblacklistedalts = [alt for alt in altblacklist if alt in imgalt]

        if isblacklistedclasses:
            print(f"skipping image with blacklisted class {isblacklistedclasses}")
            continue
        
        if isblacklistedalts:
            print(f"skipping image with blacklisted alt {isblacklistedalts}")
            continue

        print()
        print("image passes checks")
        print("downloading image")
        print()

        imgurl = urljoin(url, imgtag.get("src"))
        if imgurl:
            try:
                filename = download(imgurl, savepath, name=imgtag.get("alt"))
                print(imgurl)
                print(f"downloaded image: {filename}")
                count += 1
            except Exception as e:
                print(f"failed to download image {imgurl}: {e}")

        else: print(f"image url does not exist, skipping")
        
        if count >= numtoget:
            break
    
    print()
    print()
    print(f"scraped {numtoget} images")
    print(f"stored at {savepath}")

# TODO: remove this when shipping
imgscraper("https://reddit.com/r/femboy", numtoget=2)

def vidscraper(url: str, savepath: str="./scraperdownloads/vids/", numtoget: int = 1, blacklistedclasses: list = ['promo-video'], blacklistedalt: list = ['promo']):
    '''
    scrapes images video from the specified website
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
    for vidtag in soup.find('video'):
        print()
        print()
        print(f"video {count}/{numtoget}")
        print()

        vidclasses = vidtag.get("class", [])
        vidalt = vidtag.get("alt", "")

        print(f"checking video with tags:")
        print(f"classes: {vidclasses}")
        print(f"alts: {vidalt}")

        isblacklistedclasses = (cls in clsblacklist for cls in vidclasses)
        isblacklistedalts = (alt in altblacklist for alt in vidalt)

        if any(isblacklistedclasses):
            print(f"skipping video with blacklisted class {isblacklistedclasses}")
            continue
        
        if any(isblacklistedalts):
            print(f"skipping video with blacklisted alt {isblacklistedalts}")
            continue

        print()
        print("video passes checks")
        print("downloading video")
        print()

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
            else: print(f"video url does not exist, skipping")
        
        if count >= numtoget:
            break

    print()
    print()
    print(f"scraped {numtoget} videos")
    print(f"stored at {savepath}")
