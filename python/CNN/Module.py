from lib import *


class ModuleBase:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features: np.ndarray) -> np.ndarray:
        ...

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

        self.z = np.zeros([self.features_out], dtype=np.float64)

        for i in range(self.features_out):
            for j in range(self.features_in):
                self.weight[i,j] = rand.uniform(-1,1)
            self.bias[i] = 0

    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        for i in range(self.features_out):
            for j in range(self.features_in):
                self.z[i] += features[j] * self.weight[i,j]
            self.z[i] += self.bias[i]
        return self.z
    
class relu(ModuleBase):
    def __init__(self) -> None:
        super().__init__()
        self.a: np.ndarray = ...

    def __relu(self, input) -> np.float64:
        return 1 / (1 + np.exp(-input))

    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        self.a = np.zeros([features.size], dtype=np.float64)
        for i in range(features.size):
            self.a[i] = self.__relu(features[i])
        return self.a
    
class drop_out(ModuleBase):
    def __init__(self, drop_alpha: np.float64) -> None:
        super().__init__()
        self.a: np.ndarray = ...
        self.drop_alpha = drop_alpha

    def feedforward(self, features: np.ndarray) -> np.ndarray:
        super().feedforward(features)
        for i in range(features.size):
            self.a[i] = self.drop_alpha * features[i]
        return self.a
    
class sequence:
    def __init__(self, conv = [], fc = []) -> None:
        self.fc = fc
        self.conv = conv
        self.output: np.ndarray = ...

        self.linear = []
        self.relu = []
        self.drop_out = []

        for i in range(self.fc.__len__()):
            if self.fc[i].name == "linear":
                self.linear.append(self.fc[i])
            elif self.fc[i].name == "relu":
                self.relu.append(self.fc[i])
            elif self.fc[i].name == "drop_out":
                self.drop_out.append(self.fc[i])
            else:
                pass

        self.layer_cout = self.linear.__len__()

    def forward_prop(self, features) -> None:
        self.output = features
        self.none_updated_features = features
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

    def backward_prop(self, learning_rate, label):
        for label_index in range(label.__len__()):
            for layer_index in reversed(range(self.layer_cout)):
                for features_out_index in range(self.linear[layer_index].features_out):
                    for features_in_index in range(self.linear[layer_index].features_in):
                        self.linear[layer_index].dWeight[features_out_index, features_in_index] = self.__deriv_weight(
                            label=label[label_index],
                            label_index=label_index,
                            layer_index = layer_index,
                            features_out_index = features_out_index,
                            features_in_index = features_in_index
                        )

                        self.linear[layer_index].weight[features_out_index, features_in_index] -= learning_rate \
                        * self.linear[layer_index].dWeight[features_out_index, features_in_index]

                    self.linear[layer_index].dBias[features_out_index] = self.__deriv_bias(
                        label=label[label_index],
                        label_index = label_index,
                        layer_index = layer_index,
                        features_out_index = features_out_index
                    )

                    self.linear[layer_index].bias[features_out_index] -= learning_rate \
                    * self.linear[layer_index].dBias[features_out_index]


    def __deriv_weight(self, label, label_index, layer_index, features_out_index, features_in_index):
        sum_deriv_weight = 0
        a_deriv = 0
        input_features = 0

        if (layer_index + 1) >= self.linear.__len__():
            a_deriv = 1
            sum_deriv_weight = 1
        else:
            a_deriv = 1 - self.relu[layer_index][features_out_index]
            for i in range(self.linear[layer_index+1].features_out):
                sum_deriv_weight += (self.output[label_index] - label) * self.linear[layer_index+1].dWeight[i][features_out_index] \
                * self.linear[layer_index+1].weight[i][features_out_index]

        if (layer_index - 1) < 0:
            input_features = self.none_updated_features[features_in_index]
        else:
            input_features = self.relu[layer_index-1][features_in_index]

        return (self.output[label_index] - label) * sum_deriv_weight * a_deriv * input_features
    
    def __deriv_bias(self, label, label_index, layer_index, features_out_index):
        sum_deriv_weight = 0
        a_deriv = 0

        if (layer_index + 1) >= self.linear.__len__():
            a_deriv = 1
            sum_deriv_weight = 1
        else:
            a_deriv = 1 - self.relu[layer_index][features_out_index]
            for i in range(self.linear[layer_index+1].features_out):
                sum_deriv_weight += (self.output[label_index] - label) * self.linear[layer_index+1].dWeight[i][features_out_index] \
                * self.linear[layer_index+1].weight[i][features_out_index]

        return (self.output[label_index] - label) * sum_deriv_weight * a_deriv


