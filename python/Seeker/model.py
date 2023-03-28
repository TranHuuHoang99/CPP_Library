from lib import *
# from helper import *
from CNN_Module import linear, sequence, softmax

# model for seeker
class SeekerNN:
    def __init__(self) -> None:
        self.model = sequence(seed=4321)
        self.model.learning_rate = 0.0005

        self.model.add(linear(features_in=171, features_out=16, activation='relu'))
        self.model.add(linear(features_in=16, features_out=2, activation='relu'))
        self.model.add(softmax(2))

    def save(self, path):
        self.model.save_model(path)