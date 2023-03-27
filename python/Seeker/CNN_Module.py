from lib import *

class Layer:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features):
        self.features = np.array(features, dtype=np.float64)

class linear(Layer):
    def __init__(self, features_in, features_out, activation = None) -> None:
        super().__init__()
        self.features_in = features_in
        self.features_out = features_out
        self.weight = np.random.uniform(-1,1, [self.features_out, self.features_in])
        self.bias = np.zeros(self.features_out, dtype=np.float64)
        self.Z = np.zeros(self.features_out, dtype=np.float64)
        self.dWeight = np.zeros([self.features_out, self.features_in], dtype=np.float64)
        self.dBias = np.zeros(self.features_out, dtype=np.float64)
        self.sample_in = np.zeros(self.features_in, dtype=np.float64)
        self.activation = activation

    def __relu(self, input):
        if self.activation == "relu":
            return np.maximum(0, input)

    def feedforward(self, features):
        super().feedforward(features)
        self.sample_in = features
        self.Z = np.dot(self.weight, features) + self.bias
        return self.__relu(self.Z)
    
class softmax(Layer):
    def __init__(self, features_in) -> None:
        super().__init__()
        self.features_in = features_in
        self.child = ...
        self.mother = ...
        self.E = np.zeros(self.features_in, dtype=np.float64)
        
    def feedforward(self, features):
        super().feedforward(features)
        self.child = np.exp(features)
        self.mother = np.sum(self.child)
        self.E = self.child / self.mother
        return self.E
    
class sequence:
    def __init__(self, seed = 1) -> None:
        self.layers = []
        self.linear = []
        self.softmax: softmax = ...
        self.features = ...
        self.loss = 0
        self.learning_rate = 0.1
        np.random.seed(seed=seed)

    def add(self, layer):
        self.layers.append(layer)
        if layer.name == "linear":
            self.linear.append(layer)
        elif layer.name == "softmax":
            self.softmax = layer
        else:
            pass

    def __none_minus(self, input):
        if input < 0:
            return -input
        return input

    def __cost(self, features, label):
        cost = 0 
        for i in range(label.size):
            cost += self.__none_minus(features[i] - label[i])
        return cost / label.size

    def forward_prop(self, features, label):
        label = np.array(label, dtype=np.uint8)
        self.features = np.array(features, dtype=np.float64)
        for i in range(self.layers.__len__()):
            self.features = self.layers[i].feedforward(self.features)

        self.loss = 0
        self.loss = self.__cost(self.features, label=label)

    def backward_prop(self, label):
        for i in reversed(range(self.linear.__len__())):
            for j in range(self.linear[i].features_out):
                for k in range(self.linear[i].features_in):
                    self.linear[i].dWeight[j,k] = self.__dWeight(i=i,j=j,k=k,label=label)
                self.linear[i].dBias[j] = self.__dBias(i=i,j=j,label=label)

    def gradient_descend(self):
        for i in range(self.linear.__len__()):
            self.linear[i].weight -= self.learning_rate * self.linear[i].dWeight
            self.linear[i].bias -= self.learning_rate * self.linear[i].dBias

    def __dSoftmax(self, input):
        return input * (1 - input)
    
    def __dRelu(self, input):
        return input > 0

    def __dWeight(self, i, j, k, label):
        updated = 0
        if (i+1) >= self.linear.__len__():
            updated = (self.features[j] - label[j]) * self.__dSoftmax(self.softmax.E[j]) * \
            self.__dRelu(self.linear[i-1].Z[k]) * self.linear[i-1].Z[k]
            return updated
        
        for index in range(self.linear[i+1].features_out):
            if (i-1) < 0:
                updated += self.linear[i+1].dWeight[index][j] * self.linear[i+1].weight[index][j] * \
                self.linear[i].sample_in[k]
            else:
                updated += self.linear[i+1].dWeight[index][j] * self.linear[i+1].weight[index][j] * \
                self.linear[i-1].Z[k]
        return updated
    
    def __dBias(self, i, j, label):
        updated = 0
        if (i+1) >= self.linear.__len__():
            updated = (self.features[j] - label[j]) * self.__dSoftmax(self.softmax.E[j])
        else:
            for index in range(self.linear[i+1].features_out):
                updated += self.linear[i+1].dBias[index] * self.linear[i+1].weight[index][j]
        return updated
        
        