from lib import *


class ModuleBase:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features) -> np.ndarray:
        features = np.array(features, dtype=np.float64)

class conv3d(ModuleBase):
    def __init__(self, kernel_size = [0,0,0], padding = 0, strides = 0) -> None:
        super().__init__()
        self.features: np.ndarray = ...
        self.height: int = ...
        self.width: int = ...
        self.depth: int = ...
        self.kernel_size = kernel_size
        self.padding = padding
        self.strides = strides

    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        self.height, self.width, self.depth = features.shape
        self.height = self.height - (self.kernel_size[0] - 1)
        self.width = self.width - (self.kernel_size[1] - 1)
        self.depth = self.depth
        kernel_height, kernel_width, kernel_depth = self.kernel_size[:]
        self.features = np.zeros([self.height, self.width, self.depth], dtype=np.uint8)
        temp_arr = np.zeros([kernel_height, kernel_width], dtype=np.uint64)
        sum = np.zeros(kernel_width, dtype=np.uint64)
        
        for i in range(self.height):
            for j in range(self.width):
                temp_arr = features[i:(kernel_height+i), j:(kernel_width+j)]
                sum = temp_arr.sum(axis=0)
                sum = sum.sum(axis=0)
                sum = sum / 9
                self.features[i,j] = sum
        return self.features
    
class maxpooling(ModuleBase):
    def __init__(self, kernel_size = [0,0,0]) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.features: np.ndarray = ...
        self.height: int = ...
        self.width: int = ...
        self.depth: int = ...
    
    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        self.height, self.width, self.depth = features.shape

        self.height = int(self.height / self.kernel_size[0])
        self.width = int(self.width / self.kernel_size[1])
        self.depth = self.kernel_size[2]

        self.features = np.zeros([self.height, self.width, self.depth], dtype=np.uint8)
        red = np.zeros([self.kernel_size[0], self.kernel_size[1], 1], dtype=np.uint8)
        green = np.zeros([self.kernel_size[0], self.kernel_size[1], 1], dtype=np.uint8)
        blue = np.zeros([self.kernel_size[0], self.kernel_size[1], 1], dtype=np.uint8)
        _i = 0
        _j = 0
        for i in range(self.height):
            _j = 0
            for j in range(self.width):
                red = features[_i:(self.kernel_size[0]+_i), _j:(self.kernel_size[1]+_j), 0]
                red = red.reshape(self.kernel_size[0] * self.kernel_size[1])

                green = features[_i:(self.kernel_size[0]+_i), _j:(self.kernel_size[1]+_j), 1]
                green = green.reshape(self.kernel_size[0] * self.kernel_size[1])

                blue = features[_i:(self.kernel_size[0]+_i), _j:(self.kernel_size[1]+_j), 2]
                blue = blue.reshape(self.kernel_size[0] * self.kernel_size[1])

                _output = [max(red), max(green), max(blue)]
                _output = np.array(_output, dtype=np.uint8)
                self.features[i,j] = _output
                _j = _j + self.kernel_size[1]
            _i = _i + self.kernel_size[0]

        return self.features
    
class flatten(ModuleBase):
    def __init__(self) -> None:
        super().__init__()
        self.height: np.float64 = ...
        self.width: np.float64 = ...
        self.depth: np.float64 = ...
        self.features: np.ndarray = ...
    
    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        self.height, self.width, self.depth = features.shape
        self.features = np.zeros([self.height, self.width, self.depth], dtype=np.float64)
        
        for i in range(self.height):
            for j in range(self.width):
                self.features[i,j] = features[i,j] / 255
        self.features = self.features.reshape(self.height * self.width * self.depth)

        return self.features

class linear(ModuleBase):
    def __init__(self, features_in:int, features_out:int) -> None:
        super().__init__()
        self.features_in = features_in
        self.features_out = features_out

        self.weight = np.zeros([self.features_out, self.features_in], dtype=np.float64)
        self.bias = np.zeros([self.features_out], dtype=np.float64)

        self.dWeight = np.zeros([self.features_out, self.features_in], dtype=np.float64)
        self.dBias = np.zeros([self.features_out], dtype=np.float64)

        for i in range(self.features_out):
            for j in range(self.features_in):
                self.weight[i,j] = rand.uniform(-1,1)
            self.bias[i] = 0

    def feedforward(self, features) -> np.ndarray:
        super().feedforward(features)
        output_pred = np.zeros([self.features_out], dtype=np.float64)
        for i in range(self.features_out):
            for j in range(self.features_in):
                output_pred[i] += features[j] * self.weight[i,j]
            output_pred[i] += self.bias[i]
        return output_pred
    
class relu(ModuleBase):
    def __init__(self) -> None:
        super().__init__()

    def feedforward(self, features) -> np.ndarray:
        super().feedforward(features)
        for i in range(features.size):
            features[i] = 1 / (1 + np.exp(-features[i]))
        return features
    
class drop_out(ModuleBase):
    def __init__(self, drop_alpha: np.float64) -> None:
        super().__init__()
        self.drop_alpha = drop_alpha

    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        for i in range(features.size):
            features[i] = self.drop_alpha * features[i]
        return features
    
class sequence: ...

class Brain:
    def __init__(self) -> None:
        self.weight_linear = []
        self.bias_linear = []
        self.prediction = 0

    def __loadparam(self, NeuralNetwork) -> sequence:
        index_reversed = 0

        for i in reversed(range(NeuralNetwork.model.linear.__len__())):
            for j in range(NeuralNetwork.model.linear[i].features_out):
                for k in range(NeuralNetwork.model.linear[i].features_in):
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

    def __none_minus(self, input) -> np.float64:
        if input < 0:
            return -input
        return input
    
    def __predict(self, input_features, NeuralNetwork):
        nn:sequence = self.__loadparam(NeuralNetwork=NeuralNetwork)
        nn.forward_prop(input_features)
        nn.output[0]
        self.prediction = nn.output[0]

        return 1 if nn.output[0] >= 0.6 else 0
        
    def predict(self, input_features, NeuralNetwork):
        loss = self.__none_minus(self.prediction - self.__predict(input_features=input_features, NeuralNetwork=NeuralNetwork))
        accuracy = 1 - loss
        print("LABEL IS : %d"%(self.__predict(input_features=input_features, NeuralNetwork=NeuralNetwork)),
                " accuracy is : %f"%(accuracy),
                " loss is : %f"%(loss)      
        )
    
class sequence:
    def __init__(self, conv = [], fc = []) -> None:
        self.fc = fc
        self.conv = conv
        self.output: np.ndarray = ...

        self.linear = []
        self.relu = []
        self.drop_out = []

        self.a = []
        self.z = []

        for i in range(self.fc.__len__()):
            if self.fc[i].name == "linear":
                self.linear.append(self.fc[i])
            elif self.fc[i].name == "relu":
                self.relu.append(self.fc[i])
            elif self.fc[i].name == "drop_out":
                self.drop_out.append(self.fc[i])
            else:
                pass

    def forward_prop(self, features) -> None:
        self.output = features
        self.none_updated_features = features

        self.a = []
        self.z = []
        
        if self.conv == []:
            pass
        else:
            for i in range(self.conv.__len__()):
                self.output = self.conv[i].feedforward(self.output)
        
        if self.fc == []:
            pass
        else:
            for i in range(self.fc.__len__()):
                self.output = self.fc[i].feedforward(self.output)
                if self.fc[i].name == "linear":
                    self.z.append(self.output)
                elif self.fc[i].name == "relu":
                    self.a.append(self.output)
                else:
                    pass

    def backward_prop(self, learning_rate, label):
        for label_i in range(label.__len__()):
            for i in reversed(range(self.linear.__len__())):
                for j in range(self.linear[i].features_out):
                    for k in range(self.linear[i].features_in):
                        self.linear[i].dWeight[j,k] = self.__dWeight(label=label[label_i],label_i=label_i,i=i,j=j,k=k)
                        self.linear[i].weight[j,k] -= learning_rate * self.linear[i].dWeight[j,k]

                    self.linear[i].dBias[j] = self.__dBias(label=label,label_i=label_i,i=i,j=j)
                    self.linear[i].bias[j] -= learning_rate * self.linear[i].dBias[j]

    def __dWeight(self, label, label_i, i, j, k) ->np.float64:
        sum_dWeight = 0
        deriv = 0
        input_features = 0
        if (i+1) >= self.linear.__len__():
            deriv = 1
        else:
            deriv = 1 - self.a[i][j]
        if (i-1) < 0:
            input_features = self.none_updated_features[k]
        else:
            input_features = self.a[i-1][k]
        if (i+1) >= self.linear.__len__():
            sum_dWeight = 1
        else:
            for index in range(self.linear[i+1].features_out):
                sum_dWeight += (self.output[label_i]-label) * self.linear[i+1].dWeight[index][j] \
                            * self.linear[i+1].weight[index][j]
        return (self.output[label_i]-label) * sum_dWeight * deriv * input_features
    
    def __dBias(self, label, label_i, i, j) -> np.float64:
        sum_dBias = 0
        deriv = 0
        if (i+1) >= self.linear.__len__():
            deriv = 1
        else:
            deriv = 1 - self.a[i][j]
        if (i+1) >= self.linear.__len__():
            sum_dBias = 1
        else:
            for index in range(self.linear[i+1].features_out):
                sum_dBias += (self.output[label_i]-label) * self.linear[i+1].dWeight[index][j]\
                *self.linear[i+1].weight[index][j]
        return (self.output[label_i]-label) * sum_dBias * deriv

