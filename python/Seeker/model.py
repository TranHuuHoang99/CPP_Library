from lib import *
from helper import *
# from CNN_Module import linear, sequence, softmax

# model for seeker
class SeekerNN:
    def __init__(self) -> None:
        self.model = sequence(seed=1234)
        self.model.learning_rate = 0.01

        self.model.add(linear(features_in=171, features_out=342))
        self.model.add(relu(features_in=342))

        self.model.add(linear(features_in=342, features_out=2))
        self.model.add(relu(features_in=2))

    def save(self, path):
        self.model.save_model(path)