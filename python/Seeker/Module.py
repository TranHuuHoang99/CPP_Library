from lib import *


class Layer:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features):
        features = np.array(features, dtype=np.float64)

class Brain:
    def __init__(self) -> None:
        self.weight = []
        self.bias = []
        self.model:sequence = ...

    def set_model(self, model):
        self.model = model

    def __load_params(self):
        self.weight = np.array(self.weight, dtype=np.float64)
        self.bias = np.array(self.bias, dtype=np.float64)
        for i in range(self.model.linear.__len__()):
            self.model.linear[i].weight = self.weight[i]
            self.model.linear[i].bias = self.bias[i]

    def predict(self, features, label):
        self.__load_params()
        label = np.array(label, dtype=np.uint8)
        self.model.forward_prop(features, label=label)

        print("PREDICTION IS : ", self.model.features, " LABEL IS : ", label, " LOSS IS : ", self.model.loss)

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
        features = features * 0.5
        temp_length = (int(features.size/2)) if features.size % self.kernel_length == 0 else (int(features.size/2) + 1)
        temp = np.zeros([temp_length], dtype=np.float64)
        index = 0
        for i in range(0,features.size,self.kernel_length):
            temp[index] = (features[i:(i+self.kernel_length)].sum() / self.kernel_length)
            index += 1
        return temp

class linear(Layer):
    def __init__(self, features_in, features_out) -> None:
        super().__init__()
        self.features_out = features_out
        self.features_in = features_in
        self.weight = np.random.uniform(-1,1,[features_out, features_in])
        self.bias = np.zeros(features_out, dtype=np.float64)
        self.Z = np.zeros(features_out, dtype=np.float64)
        self.input = np.zeros(features_in, dtype=np.float64)
        self.dW = np.zeros([features_out, features_in], dtype=np.float64)
        self.dB = np.zeros([features_out], dtype=np.float64)

    def feedforward(self, features):
        super().feedforward(features)
        self.input = np.zeros(self.features_in, dtype=np.float64)
        self.input = features
        self.Z = np.dot(self.weight, features) + self.bias
        return self.Z
    
class relu(Layer):
    def __init__(self, features_in) -> None:
        super().__init__()
        self.A = np.zeros(features_in, dtype=np.float64)

    def __sigmoid(self, features):
        return 1 / (1+np.exp(-features))

    def feedforward(self, features):
        super().feedforward(features)
        self.A = self.__sigmoid(features=features)
        return self.A

class sequence:
    def __init__(self) -> None:
        self.layers = []
        self.loss = 0
        self.linear = []
        self.relu = []
        self.learning_rate = 0.1
        self.seed = 1
        np.random.seed(self.seed)
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
    
    def __dCost(self, pred, label):
        _dCost = -((label/pred) - ((1-label)/(1-pred)))
        return _dCost
    
    def __dSigmoid(self, a):
        return a * (1-a)

    def forward_prop(self, features, label):
        label = np.array(label, dtype=np.uint8)
        self.features = features
        self.loss = 0
        for i in range(self.layers.__len__()):
            self.features = self.layers[i].feedforward(self.features)

        for i in range(label.size):
            self.loss += self.__relu(self.features[i] - label[i])
        self.loss /= label.size

    def backward_prop(self, label):
        label = np.array(label, dtype=np.uint8)
        for lab_i in range(label.size):
            for i in reversed(range(self.linear.__len__())):
                for j in range(self.linear[i].features_out):
                    for k in range(self.linear[i].features_in):
                        self.linear[i].dW[j,k] = self.__cal_dW(label=label, lab_i=lab_i, i=i,j=j,k=k)
                    self.linear[i].dB[j] = self.__cal_dB(label=label, lab_i=lab_i, i=i, j=j)

    def gradient_descend(self):
        for i in range(self.linear.__len__()):
            self.linear[i].weight -= self.learning_rate * self.linear[i].dW
            self.linear[i].bias -= self.learning_rate * self.linear[i].dB

    def save(self, path):
        for i in range(self.linear.__len__()):
            self.brain.weight.append(self.linear[i].weight)
            self.brain.bias.append(self.linear[i].bias)

        pickle.dump(self.brain, open(path, "wb"))

    def __cal_dW(self, label, lab_i, i, j, k):
        updated = 0
        input_features = 0
        sum_of_dW = 0

        if (i-1) < 0:
            input_features = self.linear[i].input[k]
        else:
            input_features = self.relu[i-1].A[k]

        if (i+1) >= self.linear.__len__():
            sum_of_dW = 1
        else:
            for index in range(self.linear[i+1].features_out):
                sum_of_dW += self.__dCost(self.features[lab_i], label[lab_i]) * self.linear[i+1].dW[index][j] * self.linear[i+1].weight[index][j]
            sum_of_dW /= (self.relu[i].A[j])
        updated = self.__dCost(self.features[lab_i], label[lab_i]) * self.__dSigmoid(self.relu[i].A[j]) * input_features * sum_of_dW
        return updated
    
    def __cal_dB(self, label, lab_i, i, j):
        updated = 0
        sum_of_dB = 0

        if (i+1) >= self.linear.__len__():
            sum_of_dB = 1
        else:
            for index in range(self.linear[i+1].features_out):
                sum_of_dB += self.__dCost(self.features[lab_i], label[lab_i]) * self.linear[i+1].dW[index][j] * self.linear[i+1].weight[index][j]
        updated = self.__dCost(self.features[lab_i], label[lab_i]) * self.__dSigmoid(self.relu[i].A[j]) * sum_of_dB
        return updated


