from helper import *

class NeuralBase:
    def __init__(self, image: np.ndarray) -> None:
        self.image = image
        self.height, self.width, self.depth = self.image.shape

    def conv3d(self, kernel_size = [0,0,0], padding = 0, strides = 0) -> np.ndarray:
        self.height = self.height - (kernel_size[0] - 1)
        self.width = self.width - (kernel_size[1] - 1)
        self.depth = self.depth
        kernel_height, kernel_width, kernel_depth = kernel_size[:]
        output = np.zeros([self.height, self.width, self.depth], dtype=np.uint8)
        temp_arr = np.zeros([kernel_height, kernel_width], dtype=np.uint64)
        sum = np.zeros(kernel_width, dtype=np.uint64)
        for i in range(self.height):
            for j in range(self.width):
                temp_arr = self.image[i:(kernel_height+i), j:(kernel_width+j)]
                sum = temp_arr.sum(axis=0)
                sum = sum.sum(axis=0)
                sum = sum / 9
                output[i,j] = sum
        self.image = output
        return self.image

    def relu(self) -> np.ndarray:
        for i in range(self.height):
            for j in range(self.width):
                r,g,b = self.image[i,j]
                if r > 0:
                    r = r
                else:
                    r = 0
                if g > 0:
                    g = g
                else:
                    g = 0
                if b > 0:
                    b = b
                else:
                    b = 0
                self.image[i,j] = r, g, b
        return self.image
    
    # def maxpooling(self, kernel_size = [0,0]) -> np.ndarray:
    #     kernel_height, kernel_width = kernel_size[:]
    #     self.height = self.height / kernel_height
    #     self.width = self.width / kernel_width
    #     temp_arr = np.zeros([kernel_height, kernel_width], dtype=np.uint8)
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             temp_arr = self.image[i:(kernel_height+i),j:(kernel_width+j)]
                

if __name__ == "__main__":
    file_path = './dataset/tomato/tomato.jpg'
    file_des = './dataset/train_data/conv3d.jpg'

    # np_image = np.array(im.open(file_path))
    # _neuralBase = NeuralBase(np_image)
    # np_image = _neuralBase.conv3d(kernel_size=[3,3,3])
    # image = im.fromarray(np_image)
    # im.Image.save(image, file_des)

    arr = np.empty([4,4,3], dtype=np.uint8)
    print(arr, "\n")
    new_arr = arr[0:2,0:2,0]
    flatten = new_arr.reshape([4])
    max = max(flatten)
    print(flatten, "\n")
    print(max)
