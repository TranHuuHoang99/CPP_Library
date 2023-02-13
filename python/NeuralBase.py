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

    def relu(self, value: np.float64) -> np.float64:
        if value > 0:
            return value
        return 0
    
    def maxpooling(self, kernel_size = [0,0,0]) -> np.ndarray:
        self.height = int(self.height / kernel_size[0])
        self.width = int(self.width / kernel_size[1])
        self.depth = kernel_size[2]
        output = np.zeros([self.height, self.width, self.depth], dtype=np.uint8)
        red = np.zeros([kernel_size[0], kernel_size[1], 1], dtype=np.uint8)
        green = np.zeros([kernel_size[0], kernel_size[1], 1], dtype=np.uint8)
        blue = np.zeros([kernel_size[0], kernel_size[1], 1], dtype=np.uint8)
        _i = 0
        _j = 0
        for i in range(self.height):
            _j = 0
            for j in range(self.width):
                red = self.image[_i:(kernel_size[0]+_i), _j:(kernel_size[1]+_j), 0]
                red = red.reshape(kernel_size[0] * kernel_size[1])

                green = self.image[_i:(kernel_size[0]+_i), _j:(kernel_size[1]+_j), 1]
                green = green.reshape(kernel_size[0] * kernel_size[1])

                blue = self.image[_i:(kernel_size[0]+_i), _j:(kernel_size[1]+_j), 2]
                blue = blue.reshape(kernel_size[0] * kernel_size[1])

                _output = [max(red), max(green), max(blue)]
                _output = np.array(_output, dtype=np.uint8)
                output[i,j] = _output
                _j = _j + kernel_size[1]
            _i = _i + kernel_size[0]
        self.image = output
        return self.image

    def flatten(self) -> np.ndarray:
        output = np.zeros([self.height, self.width, self.depth], dtype=np.float64)
        for i in range(self.height):
            for j in range(self.width):
                output[i,j] = self.image[i,j] / 255
        output = output.reshape(self.height * self.width * self.depth)
        return output

    def feed_forward(self, features_in = np.ndarray, features_out = 0) -> np.ndarray:
        _features_in = features_in.size
        self.ff_output = np.zeros([features_out], dtype=np.float64)
        for i in range(features_out):
            for j in range(_features_in):
                self.ff_output[i] = self.ff_output[i] + (features_in[j] * random.uniform(-1,1))
            self.ff_output[i] = self.ff_output[i] + random.uniform(-1,1)
        return self.ff_output

    def softmax(self) -> np.ndarray:
        len_ff_output = self.ff_output.size
        for i in range(len_ff_output):
            self.ff_output[i] = self.relu(self.ff_output[i])
        return self.ff_output

    def show_shape(self) -> None:
        print("HEIGHT: ", self.height, "\n")
        print("WIDTH: ", self.width, "\n")
        print("DEPTH: ", self.depth, "\n")

if __name__ == "__main__":
    file_path = './dataset/tomato/tomato.jpg'
    file_des = './dataset/train_data/maxpooling.jpg'

    np_image = np.array(im.open(file_path))
    _neuralBase = NeuralBase(np_image)

    np_image = _neuralBase.conv3d(kernel_size=[3,3,3])
    np_image = _neuralBase.maxpooling(kernel_size=[2,2,3])

    np_image = _neuralBase.conv3d(kernel_size=[3,3,3])
    np_image = _neuralBase.maxpooling(kernel_size=[2,2,3])

    np_image = _neuralBase.conv3d(kernel_size=[3,3,3])
    np_image = _neuralBase.maxpooling(kernel_size=[2,2,3])

    np_image = _neuralBase.flatten()
    np_image = _neuralBase.feed_forward(np_image, 972)
    np_image = _neuralBase.softmax()

    np_image = _neuralBase.feed_forward(np_image, 486)
    np_image = _neuralBase.softmax()

    np_image = _neuralBase.feed_forward(np_image, 243)
    np_image = _neuralBase.softmax()

    np_image = _neuralBase.feed_forward(np_image, 121)
    np_image = _neuralBase.softmax()

    np_image = _neuralBase.feed_forward(np_image, 10)
    np_image = _neuralBase.softmax()

    print(np_image[:])