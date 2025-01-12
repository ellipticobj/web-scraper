import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import mimetypes

def cleanfilenamefromurl(url: str) -> str:
    parsedurl = urlparse(url)
    filename = os.path.basename(parsedurl.path)
    return filename

def cleantext(text: str) -> str:
    # from chatgpt
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF]"  # Match emojis (Unicode Supplementary Multilingual Plane)
        "|[\u2600-\u26FF]"          # Match miscellaneous symbols
        "|[\u2700-\u27BF]"          # Match dingbats
        "|[\U0001F300-\U0001F5FF]"  # Match various symbols
        "|[\U0001F600-\U0001F64F]"  # Match emoticons
        "|[\U0001F680-\U0001F6FF]"  # Match transport & map symbols
    )
    text = emoji_pattern.sub("", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    text = " ".join(text.split())

    return text

def getfileext(url: str, response: requests.Response) -> str:
    parsedurl = urlparse(url)
    ext = os.path.splitext(parsedurl.path)[1]
    if ext:
        return ext
    
    # from chatgpt
    contenttype = response.headers.get('content-type')
    ext = mimetypes.guess_extension(contenttype)
    return ext or ""

def download(url: str, savepath: str = "./scraperdownloads/", name: str = None):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    basename = cleantext(name) or cleanfilenamefromurl(url)
    filename = f"{basename}{getfileext(url, response)}"
    filepath = os.path.join(savepath, filename)

    print(f"downloading {filename}")

    if response.status_code == 200:
        with open(filepath, 'wb') as file:
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

    try:
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
                except Exception as e:
                    print(f"failed to download image {imgurl}: {e}")

            else: print(f"image url does not exist, skipping")
            
            count += 1
            if count >= numtoget:
                break
    except:
        print()
        print("no images found")
    
    print()
    print()
    print(f"scraped {numtoget} images")
    print(f"stored at {savepath}{filename}")

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
    try:
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

            isblacklistedclasses = [cls for cls in clsblacklist if cls in vidclasses]
            isblacklistedalts = [alt for alt in altblacklist if alt in vidalt]

            if isblacklistedclasses:
                print(f"skipping video with blacklisted class {isblacklistedclasses}")
                continue
            
            if isblacklistedalts:
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
    except:
        print()
        print("no videos found")

    print()
    print()
    print(f"scraped {count} videos")
    print(f"stored at {savepath}")


# debugging
imgscraper("https://reddit.com/r/femboy", numtoget=1)
vidscraper("https://reddit.com/r/femboy", numtoget=1)