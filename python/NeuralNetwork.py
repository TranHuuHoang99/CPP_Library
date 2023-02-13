from helper import *
from NeuralBase import NeuralBase

class CNN(NeuralBase):
    def __init__(self, image: np.ndarray) -> None:
        super().__init__(image)
        self.conv3d(kernel_size=[3,3,3])
        self.relu()
        self.conv3d(kernel_size=[3,3,3])
        self.relu()
        self.maxpooling(kernel_size=[2,2,3])

        self.conv3d(kernel_size=[3,3,3])
        self.relu()
        self.conv3d(kernel_size=[3,3,3])
        self.relu()
        self.maxpooling(kernel_size=[2,2,3])

        self.flatten()
        

