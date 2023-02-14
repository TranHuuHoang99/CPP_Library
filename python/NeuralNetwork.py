from helper import *
from core import core

class CNN(core):
    def __init__(self, image: np.ndarray) -> None:
        super().__init__(image)
        #convolutional layers

        self.nn = self.conv3d(kernel_size=[3,3,3])
        self.nn = self.maxpooling(kernel_size=[2,2,3])

        self.nn = self.conv3d(kernel_size=[3,3,3])
        self.nn = self.maxpooling(kernel_size=[2,2,3])

        self.nn = self.conv3d(kernel_size=[3,3,3])
        self.nn = self.maxpooling(kernel_size=[2,2,3])

        #hidden layers
    
        self.nn = self.flatten()
        self.nn = self.linear(self.nn, 972)
        self.nn = self.relu()
        self.nn = self.drop_out(drop_expec=0.1)

        self.nn = self.linear(self.nn, 486)
        self.nn = self.relu()
        self.nn = self.drop_out(drop_expec=0.1)

        self.nn = self.linear(self.nn, 243)
        self.nn = self.relu()
        self.nn = self.drop_out(drop_expec=0.1)

        self.nn = self.linear(self.nn, 121)
        self.nn = self.relu()
        self.nn = self.drop_out(drop_expec=0.1)

        self.nn = self.linear(self.nn, 10)
        self.nn = self.relu()
        self.nn = self.drop_out(drop_expec=0.1)

    def feed_forward(self) -> np.ndarray:
        self.nn = self.softmax(self.nn)
        return self.nn

