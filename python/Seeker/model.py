from lib import *
from helper import *

# model for seeker
class SeekerNN:
    def __init__(self) -> None:
        rand.seed(2)
        self.model = sequence()
        self.model.seed = 1
        self.model.learning_rate = 0.01

        self.model.add(conv1d(kernel_length=3))
        self.model.add(conv1d(kernel_length=3))
        self.model.add(maxpooling1d(kernel_length=2))

        self.model.add(conv1d(kernel_length=3))
        self.model.add(conv1d(kernel_length=3))
        self.model.add(maxpooling1d(kernel_length=2))

        self.model.add(conv1d(kernel_length=3))
        self.model.add(conv1d(kernel_length=3))
        self.model.add(maxpooling1d(kernel_length=2))

        self.model.add(linear(features_in=111, features_out=50))
        self.model.add(relu(features_in=50))

        self.model.add(linear(features_in=50, features_out=25))
        self.model.add(relu(25))

        self.model.add(linear(features_in=25, features_out=2))
        self.model.add(relu(features_in=2))

    def save(self, path):
        self.model.save(path)