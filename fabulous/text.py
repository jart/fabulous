
import os

import grapefruit

from fabulous import utils, image, color


DEFAULT_FONT = os.path.join(os.path.dirname(__file__), 'fonts', 'IndUni-H-Bold.otf')


class Text(image.Image):
    def __init__(self, text, fsize=20, color="#0099ff", font=DEFAULT_FONT,
                 shadow=False, scew=None):
        utils.pil_check()
        from PIL import Image, ImageFont, ImageDraw
        self.text = text
        self.color = grapefruit.Color.NewFromHtml(color)
        self.font = ImageFont.truetype(font, fsize)
        size = tuple([n + 3 for n in self.font.getsize(self.text)])
        self.img = Image.new("RGBA", size, (0, 0, 0, 0))
        cvs = ImageDraw.Draw(self.img)
        if shadow:
            cvs.text((2, 2), self.text, font=self.font, fill=(150, 150, 150, 150))
        cvs.text((1, 1), self.text, font=self.font, fill=self.color.html)
        if scew:
            self.img = self.img.transform(
                size, Image.AFFINE, (1.0, 0.1 * scew, -1.0 * scew,
                                     0.0, 1.0, 0.0))
        self.resize(None)
