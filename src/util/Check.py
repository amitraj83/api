
from PIL import Image

def main():
    size = 580, 290

    try:
        im = Image.open("C:\\house-idea\\carimagery\\carimagery\\maserati-granturismo-2007-2017-1462430872.64.png")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save("C:\\house-idea\\carimagery\\carimagery\\maserati-granturismo-2007-2017-1462430872.64-scaled.png")
    except IOError:
        print
        "cannot create thumbnail for "

if __name__ == "__main__":
    main()