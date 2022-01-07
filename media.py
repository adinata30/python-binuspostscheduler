import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

class Media:
    def __init__(self):
        print("Initialize media..")

    def download_image(self,url,idx):
        # url = 'https://picsum.photos/720/1280/?random'
        r = requests.get(url = url)
        with open(f"download{idx}.png", 'wb') as f:
            f.write(r.content)
        # print("download finished")

    # def save_image(self,filename):


    def process_image(self, text, author):
        text = textwrap.fill(text, width=35)
        image = Image.open("downloaded_bg.png").filter(ImageFilter.GaussianBlur(10))
        image = ImageEnhance.Brightness(image)
        image.enhance(0.5).save('image.png')
        image = Image.open('image.png')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('Livvic-Regular.ttf', size = 29)
        w, h = draw.textsize(text, font = font)
        draw.text(((720 - w) / 2, (1280 - h) / 2), text, (255, 255, 255), align="center", font = font)
        if author is not None:
            _author = '@%s' % str(author)
            x, y = draw.textsize(_author, font =  font)
            font = ImageFont.truetype('Livvic-Bold.ttf', size = 29)
            draw.text(((720 - x) / 2, ((1280 / 2) + h) + 60), _author, (255, 255, 255),font = font, align="bottom")
        image.save('ready.png')