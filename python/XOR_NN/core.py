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

    def reset_weight(self):
        for i in reversed(range(self.model.linear.__len__())):
            self.model.linear[i].delta_weight = np.zeros([self.model.linear[i].out_features, self.model.linear[i].in_features], dtype=np.float16)
            self.model.linear[i].delta_bias = np.zeros([self.model.linear[i].out_features], dtype=np.float16)
    
    def back_propagation(self, learning_rate, lable):
        if self.model == Ellipsis:
            return

        self.reset_weight()

        delta_bias = 0

        for i in reversed(range(self.model.linear.__len__())):
            for j in range(self.model.linear[i].out_features):
                for k in range(self.model.linear[i].in_features):
                    self.model.linear[i].delta_weight[j,k] = self.delta_weight(label=lable, i=i, j=j, k=k)
                    self.model.linear[i].weight[j,k] -= learning_rate * self.model.linear[i].delta_weight[j,k]
                    delta_bias = self.delta_bias(label=lable, i=i, j=j, k=k)
                self.model.linear[i].bias[j] -= learning_rate * delta_bias

    def delta_weight(self, label, i, j, k) -> np.float16:
        updated_weight = 1
        sumof_before_weight = 0
        deriv = 0
        input_features = 0

        if (i + 1) > self.model.linear.__len__():
            deriv = 1
        else:
            deriv = (1 - self.model.a[i][j])

        if (i - 1) < 0:
            input_features = self.model.first_features[0][k]
        else:
            input_features = self.model.a[i-1][k]

        if (i + 2) > self.model.linear.__len__():
            sumof_before_weight = 1
        else:
            for index in range(self.model.linear[i+1].out_features):
                sumof_before_weight += (self.model.linear[i+1].delta_weight[index][k] * self.model.linear[i+1].weight[index][k])

        updated_weight = (self.model.features[0] - label) * sumof_before_weight * deriv * input_features
        return updated_weight

    def delta_bias(self, label, i, j, k) -> np.float16:
        updated_bias = 1
        sumof_before_weight = 0
        deriv = 0
        deriv_z_of_bias = 1

        if (i + 1) > self.model.linear.__len__():
            deriv = 1
        else:
            deriv = (1 - self.model.a[i][j])

        if (i + 2) > self.model.linear.__len__():
            sumof_before_weight = 1
        else:
            for index in range(self.model.linear[i+1].out_features):
                sumof_before_weight += (self.model.linear[i+1].delta_weight[index][k] * self.model.linear[i+1].weight[index][k])

        updated_bias = (self.model.features[0] - label) * sumof_before_weight * deriv * deriv_z_of_bias
        return updated_bias
