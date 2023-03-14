from lib import *


class Layer:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features):
        features = np.array(features, dtype=np.float64)

class conv1d(Layer):
    def __init__(self, kernel_length = 3) -> None:
        super().__init__()
        self.kernel_length = kernel_length

    def feedforward(self, features) -> np.ndarray:
        super().feedforward(features)
        features = features / features.size
        temp = np.zeros([features.size - (self.kernel_length - 1)], dtype=np.float64)
        for i in range(temp.size):
            temp[i] = (features[i:(i+self.kernel_length)].sum()) / self.kernel_length
        return temp

class maxpooling1d(Layer):
    def __init__(self, kernel_length = 2) -> None:
        super().__init__()
        self.kernel_length = kernel_length

    def feedforward(self, features) -> np.ndarray:
        super().feedforward(features)
        temp_length = (int(features.size/2)) if features.size % self.kernel_length == 0 else (int(features.size/2) + 1)
        temp = np.zeros([temp_length], dtype=np.float64)
        index = 0
        for i in range(0,features.size,self.kernel_length):
            temp[index] = max(features[i:(i+self.kernel_length)])
            index += 1
        return temp

class Layer:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features):
        features = np.array(features, dtype=np.float64)

class linear(Layer):
    def __init__(self, features_in, features_out) -> None:
        super().__init__()
        self.features_in = features_in
        self.features_out = features_out
        self.weight = np.random.uniform(-1, 1, [self.features_out, self.features_in])
        self.bias = np.zeros(self.features_out, dtype=np.float64)
        self.dW = np.zeros([self.features_out, self.features_in], dtype=np.float64)
        self.dB = np.zeros(self.features_out, dtype=np.float64)
        self.input = np.zeros(self.features_in, dtype=np.float64)
        self.Z = np.zeros(self.features_out, dtype=np.float64)

    def feedforward(self, features):
        super().feedforward(features)
        self.input = features
        self.Z = np.dot(self.weight, features) + self.bias
        return self.Z
    
class relu(Layer):
    def __init__(self, features_in) -> None:
        super().__init__()
        self.features_in = features_in
        self.A = np.zeros(self.features_in, dtype=np.float64)

    def __sigmoid(self, features):
        return 1 / (1+np.exp(-features))

    def feedforward(self, features):
        super().feedforward(features)
        self.A = self.__sigmoid(features=features)
        return self.A
    
class Brain:
    def __init__(self) -> None:
        self.weight = []
        self.bias = []
        self.model:sequence = ...

    def set_model(self, model):
        self.model = model

    def __load_params(self):
        for i in range(self.model.linear.__len__()):
            self.model.linear[i].weight = self.weight[i]
            self.model.linear[i].bias = self.bias[i]

    def predict(self, features, label):
        self.__load_params()
        label = np.array(label, dtype=np.uint8)
        self.model.forward_prop(features, label=label)

        print("PREDICTION IS : ", self.model.features, " LABEL IS : ", label, " LOSS IS : ", self.model.loss)
    
class sequence:
    def __init__(self, seed = 1) -> None:
        self.layers = []
        self.linear = []
        self.relu = []
        self.features = ...
        self.learning_rate = 0.1
        np.random.seed(seed)
        self.loss = 0
        self.brain = Brain()

    def add(self, layer):
        self.layers.append(layer)
        if layer.name == "linear":
            self.linear.append(layer)
        elif layer.name == "relu":
            self.relu.append(layer)
        else:
            pass

    def __relu(self, input):
        if input < 0:
            return -input
        return input

    def __cost(self, features, label):
        cost = 0 
        for i in range(label.size):
            cost += self.__relu(features[i] - label[i])
        return cost / label.size

    def forward_prop(self, features, label):
        self.features = np.array(features, dtype=np.float64)
        label = np.array(label, dtype=np.uint8)
        for i in range(self.layers.__len__()):
            self.features = self.layers[i].feedforward(self.features)
        self.loss = 0
        self.loss = self.__cost(self.features, label)

    def backward_prop(self, label):
        for i in reversed(range(self.linear.__len__())):
            for j in range(self.linear[i].features_out):
                for k in range(self.linear[i].features_in):
                    self.linear[i].dW[j,k] = self.__dWeight(label=label,i=i,j=j,k=k)
                self.linear[i].dB[j] = self.__dBias(label=label, i=i, j=j)

    def gradient_descend(self):
        for i in range(self.linear.__len__()):
            self.linear[i].weight -= self.learning_rate * self.linear[i].dW
            self.linear[i].bias -= self.learning_rate * self.linear[i].dB

    def save_model(self, path):
        self.brain.weight = []
        self.brain.bias = []
        for i in range(self.linear.__len__()):
            self.brain.weight.append(self.linear[i].weight)
            self.brain.bias.append(self.linear[i].bias)
        pickle.dump(self.brain, open(path, "wb"))
    
    def __dSigmoid_weight(self, a):
        return (1-a) 
    
    def __dSigmoid_bias(self, a):
        return a * (1 - a)

    def __dWeight(self, label, i, j, k):
        updated = 0
        if (i+1) >= self.linear.__len__():
            updated = (self.features[j] - label[j]) * self.relu[i-1].A[k]
            return updated
        
        for index in range(self.linear[i+1].features_out):
            if (i-1) < 0:
                updated += self.linear[i+1].dW[index][j] * self.linear[i+1].weight[index][j] * self.__dSigmoid_weight(self.relu[i].A[j]) * self.linear[i].input[k]
            else:
                updated += self.linear[i+1].dW[index][j] * self.linear[i+1].weight[index][j] * self.__dSigmoid_weight(self.relu[i].A[j]) * self.relu[i-1].A[k]
        return updated

    def __dBias(self, label, i, j):
        updated = 0
        if (i+1) >= self.linear.__len__():
            updated = (self.features[j] - label[j])
        else:
            for index in range(self.linear[i+1].features_out):
                updated += self.linear[i+1].dB[index] * self.linear[i+1].weight[index][j] * self.__dSigmoid_bias(self.relu[i].A[j])
        return updated


