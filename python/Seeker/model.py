from lib import *
import helper as nn


class SeekerNN:
    def __init__(self) -> None:
        rand.seed(1234)
        self.brain = nn.Brain()
        self.model = nn.sequence(
            # conv=[
            #     nn.conv1d(kernel_length=3),
            #     nn.conv1d(kernel_length=3),
            #     nn.maxpooling1d(kernel_length=2),
                
            #     nn.conv1d(kernel_length=3),
            #     nn.conv1d(kernel_length=3),
            #     nn.maxpooling1d(kernel_length=2),

            #     nn.conv1d(kernel_length=3),
            #     nn.conv1d(kernel_length=3),
            #     nn.maxpooling1d(kernel_length=2)
            # ],
            fc= [
                nn.linear(features_in=910, features_out=220),
                nn.relu(),

                nn.linear(features_in=220, features_out=100),
                nn.relu(),

                nn.linear(features_in=100, features_out=2),
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