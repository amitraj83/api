
from PIL import Image

def main():
    size = 580, 290

    try:
        im = Image.open("C:\\house-idea\\carimagery\\carimagery\\seat-ibiza-2017-2018-1508817347.77.jpg")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save("C:\\house-idea\\carimagery\\carimagery\\seat-ibiza-2017-2018-1508817347.77-scaled.jpg", "JPEG")
    except IOError:
        print
        "cannot create thumbnail for "

if __name__ == "__main__":
    main()