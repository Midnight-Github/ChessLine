from os import path
from PIL import ImageTk as PilImageTk, Image as PilImage

class Image():
    def __init__(self, rel_path):
        self.path = path.dirname(__file__) + rel_path

    def pull(self):
        with PilImage.open(self.path) as img:
            return PilImageTk.PhotoImage(img)

    def pullCropped(self, x1, y1, x2, y2, photo_image=True):
        with PilImage.open(self.path) as img:
            if photo_image:
                return PilImageTk.PhotoImage(img.crop((x1, y1, x2, y2)))
            return img.crop((x1, y1, x2, y2))

    def generate(self, x, y, height, width, inc_x, inc_y, no_of_images, scale_factor):
        for i in range(no_of_images):
            img = self.pullCropped(x, y, x + width, y + height, False)
            yield PilImageTk.PhotoImage(img.resize((int(width*scale_factor), int(height*scale_factor))))
            x += inc_x
            y += inc_y