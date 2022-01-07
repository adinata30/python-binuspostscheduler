import requests
import textwrap
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


    