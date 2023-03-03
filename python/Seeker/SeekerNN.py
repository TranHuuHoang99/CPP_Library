from lib import *
import helper as nn

class SeekerNN:
    def __init__(self) -> None:
        rand.seed(1234)
        self.brain = nn.Brain()
        self.model = nn.sequence(
            fc=[
                nn.linear(features_in=2,features_out=2),
                nn.relu(),

                nn.linear(features_in=2, features_out=1),
                nn.relu()
            ]
        )

    def save(self, path):
        self.brain.weight_linear = []
        self.brain.bias_linear = []

        for i in reversed(range):
            self.brain.weight_linear.append(self.model.linear[i].weight)
            self.brain.bias_linear.append(self.model.linear[i].bias)

        pickle.dump(self.brain, open(path, "wb"))
