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

        self.model.add(linear(features_in=18, features_out=36))
        self.model.add(relu(features_in=36))

        self.model.add(linear(features_in=36, features_out=42))
        self.model.add(relu(features_in=42))

        self.model.add(linear(features_in=42, features_out=2))
        self.model.add(relu(2))

    def save(self, path):
        self.model.save_model(path)