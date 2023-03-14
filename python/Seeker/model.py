from lib import *
from helper import *

# model for seeker
class SeekerNN:
    def __init__(self) -> None:
        rand.seed(2)
        self.model = sequence(seed=1234)
        self.model.learning_rate = 0.1

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

        self.model.add(linear(features_in=25, features_out=12))
        self.model.add(relu(12))

        self.model.add(linear(features_in=12, features_out=4))
        self.model.add(relu(4))

        self.model.add(linear(features_in=4, features_out=2))
        self.model.add(relu(features_in=2))

    def save(self, path):
        self.model.save_model(path)