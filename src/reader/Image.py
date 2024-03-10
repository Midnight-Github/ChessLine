from os import path
from typing import Iterator
from PIL import ImageTk as PilImageTk, Image as PilImage

class Image():
    def __init__(self, rel_path: str) -> None:
        self.path = path.dirname(__file__) + rel_path

    def pull(self) -> PilImageTk.PhotoImage:
        with PilImage.open(self.path) as img:
            return PilImageTk.PhotoImage(img)

    def pullCroppedImage(self, x1: int, y1: int, x2: int, y2: int) -> PilImage.Image:
        with PilImage.open(self.path) as img:
            return img.crop((x1, y1, x2, y2))

    def pullCroppedPhotoImage(self, x1: int, y1: int, x2: int, y2: int) -> PilImageTk.PhotoImage:
        with PilImage.open(self.path) as img:
            return PilImageTk.PhotoImage(img.crop((x1, y1, x2, y2)))

    def generate(self, x: int, y: int, height: int, width: int, inc_x: int, inc_y: int, no_of_images: int, 
        scale_factor: float) -> Iterator[PilImageTk.PhotoImage]:
        
        for i in range(no_of_images):
            img = self.pullCroppedImage(x, y, x + width, y + height)
            yield PilImageTk.PhotoImage(img.resize((int(width*scale_factor), int(height*scale_factor))))
            x += inc_x
            y += inc_y