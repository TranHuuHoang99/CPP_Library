from lib import *
import helper as nn

# model for seeker
class SeekerNN:
    def __init__(self) -> None:
        rand.seed(2)
        self.brain = nn.Brain()
        self.model = nn.sequence(
            conv=[
                nn.conv1d(kernel_length=3),
                nn.conv1d(kernel_length=3),
                nn.maxpooling1d(kernel_length=2),
                
                nn.conv1d(kernel_length=3),
                nn.conv1d(kernel_length=3),
                nn.maxpooling1d(kernel_length=2),

                nn.conv1d(kernel_length=3),
                nn.conv1d(kernel_length=3),
                nn.maxpooling1d(kernel_length=2),

                nn.conv1d(kernel_length=3),
                nn.conv1d(kernel_length=3),
                nn.maxpooling1d(kernel_length=2)
            ],
            fc= [
                nn.linear(features_in=54, features_out=120),
                nn.relu(),

                nn.linear(features_in=120, features_out=240),
                nn.relu(),

                nn.linear(features_in=240, features_out=2),
                nn.relu()
            ]
        )

    def save(self, path):
        self.brain.weight_linear = []
        self.brain.bias_linear = []
        for i in reversed(range(self.model.linear.__len__())):
            self.brain.weight_linear.append(self.model.linear[i].weight)
            self.brain.bias_linear.append(self.model.linear[i].bias)
        pickle.dump(self.brain, open(path, "wb"))

class XORNN:
    def __init__(self) -> None:
        rand.seed(2)
        self.brain = nn.Brain()
        self.model = nn.sequence(
            fc= [
                nn.linear(features_in=2, features_out=16),
                nn.relu(),

                nn.linear(features_in=16, features_out=32),
                nn.relu(),

                nn.linear(features_in=32, features_out=1),
                nn.relu()
            ]
        )

    def save(self, path):
        self.brain.weight_linear = []
        self.brain.bias_linear = []
        for i in reversed(range(self.model.linear.__len__())):
            self.brain.weight_linear.append(self.model.linear[i].weight)
            self.brain.bias_linear.append(self.model.linear[i].bias)
        pickle.dump(self.brain, open(path, "wb"))