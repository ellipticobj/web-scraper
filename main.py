from scraper import *

print("web scraper")
print()

while True:
    choice = input('''1. image
2. video
q. quit
> ''')
    print()

    if choice == "1":
        url = input("url\n> ")
        print()

        while numtoget := input("number of images to download\n> "):
            if numtoget.isdigit():
                break
            print("please enter a valid number")
        print()

        savepath = input("savepath\n> ")
        print()

        imgscraper(url, savepath, int(numtoget))
        print()

    elif choice == "2":
        url = input("url\n> ")
        print()

        while numtoget := input("number of videos to download\n> "):
            if numtoget.isdigit() and numtoget > 0:
                break
            print("please enter a valid integer")
        print()

        savepath = input("savepath\n> ")
        print()

        vidscraper(url, savepath, int(numtoget))
        print()

    elif choice == "q" or choice == "quit":
        print("quitting...")
        break
    
    else:
        print("invalid choice")

