from helper import (np, im, math)

class Preprocess:
    def __init__(self, file_path: str) -> None:
        self.image = im.open(file_path)
        self.image_np = np.array(self.image)
        self.height , self.width, self.depth = self.image_np.shape

    def resize_image(self, scale = []) -> None:
        self.image = im.Image.resize(self.image, scale)
        self.image_np = np.array(self.image)
        self.height , self.width, self.depth = self.image_np.shape

    def save_image(self, file_des: str) -> None:
        im.Image.save(self.image, file_des)

    def flip_upside_down(self) -> None:
        temp_arr = np.empty([self.height, self.width, self.depth], dtype=np.uint8)
        self.i = len(self.image_np) - 1
        self.j = len(self.image_np[self.i]) - 1
        self._i = 0
        self._j = 0
        for self.i in reversed(range(len(self.image_np))):
            self._j = 0
            for self.j in reversed(range(len(self.image_np[self.i]))):
                temp_arr[self._i, self._j] = self.image_np[self.i, self.j]
                self._j += 1
            self._i += 1
        self.image_np = temp_arr
        self.image = im.fromarray(self.image_np)


if __name__ == "__main__":
    file_path = './dataset/tomato/tomato.jpg'
    file_des = './dataset/train_data/result.jpg'
    file_des_rotation = './dataset/train_data/rotate.jpg'
    preprocess = Preprocess(file_path)
    preprocess.resize_image([100,100])
    preprocess.flip_upside_down()
    preprocess.save_image(file_des_rotation)

