from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os.path
import argparse

FOLDER = "/usr/share/fonts/truetype/ubuntu-font-family"
FONT = "ubuntu-fonrt-family/Ubuntu-R.ttf"
WIDTH = 70
FONTSIZE = 30
TEXT = "I love you aofei <3"
PAD = 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", type=int, default=WIDTH)
    parser.add_argument("-s", "--size", type=int, default=FONTSIZE)
    parser.add_argument("text")
    return parser.parse_args()


def asciify(text):

    # http://stackoverflow.com/questions/2672144/dump-characters-glyphs-from-truetype-font-ttf-into-bitmaps
    letters = []
    startidx = 0
    last = None
    for i, c in enumerate(text):

        im = Image.new("RGB", (800, 600))
        draw = ImageDraw.Draw(im)

        # use a truetype font
        font = ImageFont.truetype(os.path.join(FOLDER, FONT), FONTSIZE)

        draw.text((0, 0), text[startidx:(i + 1)], font=font)

        bbox = im.getbbox()

        if bbox[2] - bbox[0] > WIDTH:
            letters.append(last)
            startidx = i

        last = im
    if startidx != len(text) - 1:
        letters.append(last)

    left = 9999
    upper = 9999
    lower = 0
    right = 0
    for im in letters:
        left = min(left, im.getbbox()[0])
        upper = min(upper, im.getbbox()[1])
        right = max(right, im.getbbox()[2])
        lower = max(lower, im.getbbox()[3])

    cropped = []
    for im in letters:
        bbox = [left - PAD, upper - PAD, right + PAD, lower + PAD]
        cropped.append(im.crop(bbox))

    for im in cropped:
        width = im.width
        data = list(im.getdata(0))
        rows = [data[width * i:width * (i + 1)] for i in xrange(im.height)]
        pixels = [[1 if d > 128 else 0 for d in row] for row in rows]
        for row in pixels:
            print "".join(["X" if p else "." for p in row])


args = parse_args()
WIDTH = args.width
FONTSIZE = args.size
asciify(args.text)
