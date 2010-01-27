
from grapefruit import Color
from PIL import Image, ImageFont, ImageDraw

from fabulous import image, color


class Text(image.Image):
    def __init__(self, text, fsize=20, color="#0099ff", bgcolor='black',
                 shadow=False, scew=None):
        self.text = text
        self.color = Color.NewFromHtml(color)
        self.bgcolor = Color.NewFromHtml(bgcolor)
        self.font = ImageFont.truetype(r'/home/jart/.fonts/IndUni-H-Bold.otf', fsize)
        # self.font = ImageFont.truetype(r'/home/jart/.fonts/LokiCola.ttf', fsize)
        # self.font = ImageFont.truetype(r'/home/jart/.fonts/Candice.ttf', fsize)
        size = tuple([n + 3 for n in self.font.getsize(self.text)])
        self.img = Image.new("RGBA", size, (0, 0, 0, 0))
        cvs = ImageDraw.Draw(self.img)
        if shadow:
            cvs.text((2, 2), self.text, font=self.font, fill='#444444')
        cvs.text((1, 1), self.text, font=self.font, fill=self.color.html)
        if scew:
            self.img = self.img.transform(
                size, Image.AFFINE, (1.0, 0.1 * scew, -1.0 * scew,
                                     0.0, 1.0, 0.0))
        self.resize(None)
