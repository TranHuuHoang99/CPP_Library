from helper import *
from Module import (
    Module,
    relu,
    linear,
    sequence
)


class core:
    def __init__(self) -> None:
        self.model: sequence = ...
    
    def back_propagation(self, learning_rate, lable):
        if self.model == Ellipsis:
            return
        
        updated_value = 0.1
        for i in range(self.model.linear.__len__()):
            for j in range(self.model.linear[i].out_features):
                for k in range(self.model.linear[i].in_features):
                    self.model.linear[i].weight[j][k] -= learning_rate * self.deriv_total_loss(lable=lable, pred=self.model.features[0])

    def deriv_total_loss(self, lable, pred) -> np.float16:
        if lable == 0:
            return 0
        loss = np.float16(-(lable / pred) + ((1-lable) / (1-pred)))
        return loss
