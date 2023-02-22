from helper import *
from Module import (
    Module,
    relu,
    linear,
    sequence
)

class Brain:
    def __init__(self) -> None:
        self.weight_linear = []
        self.bias_linear = []

    def loadparam(self, NeuralNetwork) -> sequence:
        index_reversed = 0

        print(self.weight_linear, "\n")
        print(self.bias_linear)

        for i in reversed(range(NeuralNetwork.model.linear.__len__())):
            for j in range(NeuralNetwork.model.linear[i].out_features):
                for k in range(NeuralNetwork.model.linear[i].in_features):
                    NeuralNetwork.model.linear[i].weight = self.weight_linear[index_reversed][j][k]
                NeuralNetwork.model.linear[i].bias = self.bias_linear[index_reversed][j]
            index_reversed += 1

        index = NeuralNetwork.model.linear.__len__() - 1
        for i in range(NeuralNetwork.model.fc.__len__()):
            if NeuralNetwork.model.fc[i].name == "linear":
                NeuralNetwork.model.fc[i].weight = self.weight_linear[index]
                NeuralNetwork.model.fc[i].bias = self.bias_linear[index]
                index -= 1

        return NeuralNetwork.model
        
    def predict(self, input_features, NeuralNetwork) -> np.float64:
        nn:sequence = self.loadparam(NeuralNetwork=NeuralNetwork)
        nn.feedforward(input_features)
        nn.features[0]

        if nn.features[0] >= 0.6:
            print(1)
        elif nn.features[0] <= 0.5:
            print(0)
        
        return nn.features[0]

class core:
    def __init__(self) -> None:
        self.model: sequence = ...
        self.brain = Brain()
        self.epoch = 0
    
    def back_propagation(self, learning_rate, lable):
        if self.model == Ellipsis:
            return
        self.epoch += 1

        for i in reversed(range(self.model.linear.__len__())):
            for j in range(self.model.linear[i].out_features):
                for k in range(self.model.linear[i].in_features):
                    self.model.linear[i].delta_weight[j,k] += self.delta_weight(label=lable, i=i, j=j, k=k)
                    self.model.linear[i].delta_weight[j,k] *= (1/self.epoch)
                    self.model.linear[i].weight[j,k] -= learning_rate * self.model.linear[i].delta_weight[j,k]

                self.model.linear[i].delta_bias[j] += self.delta_bias(label=lable, i=i, j=j, k=0)
                self.model.linear[i].delta_bias[j] *= (1/self.epoch)
                self.model.linear[i].bias[j] -= learning_rate * self.model.linear[i].delta_bias[j]

    def save(self, path):
        self.brain.weight_linear = []
        self.brain.bias_linear = []

        for i in reversed(range(self.model.linear.__len__())):
            self.brain.weight_linear.append(self.model.linear[i].weight)
            self.brain.bias_linear.append(self.model.linear[i].bias)

        pickle.dump(self.brain, open(path, "wb"))
        
    def delta_weight(self, label, i, j, k) -> np.float64:
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
                sumof_before_weight += (self.model.linear[i+1].delta_weight[index][j] * self.model.linear[i+1].weight[index][j])

        updated_weight = (self.model.features[0] - label) * sumof_before_weight * deriv * input_features
        return updated_weight

    def delta_bias(self, label, i, j, k) -> np.float64:
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
                sumof_before_weight += (self.model.linear[i+1].delta_weight[index][j] * self.model.linear[i+1].weight[index][j])

        updated_bias = (self.model.features[0] - label) * sumof_before_weight * deriv * deriv_z_of_bias
        return updated_bias

