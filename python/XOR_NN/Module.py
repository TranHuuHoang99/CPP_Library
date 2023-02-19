from helper import *

class Module:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def feedforward(self, features):
        self.features = features

    def forward(self, features) -> np.ndarray:
        features = np.array(features, dtype=np.float16)

class linear(Module):
    def __init__(self, in_features, out_features) -> None:
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        self.weight = np.zeros([out_features, in_features], dtype=np.float16)
        self.bias = np.zeros([out_features], dtype=np.float16)
        
        self.delta_weight = np.zeros([out_features, in_features], dtype=np.float16)
        self.delta_bias = np.zeros([out_features], dtype=np.float16)

        for i in range(out_features):
            for j in range(in_features):
                self.weight[i,j] = rand.uniform(-1,1)
            self.bias[i] = 0

    def forward(self, features) -> np.ndarray:
        super().forward(features)
        output_pred = np.zeros([self.out_features], dtype=np.float16)
        for i in range(self.out_features):
            for j in range(self.in_features):
                output_pred[i] += features[j] * self.weight[i,j]
            output_pred[i] += self.bias[i]

        return output_pred

class relu(Module):
    def __init__(self) -> None:
        super().__init__()
        ...

    def forward(self, features) -> np.ndarray:
        super().forward(features)
        for i in range(features.size):
            features[i] = 1 / (1 + np.exp(-features[i]))

        return features

class sequence(Module):
    def __init__(self,conv:Module = [], fc:Module = []) -> None:
        super().__init__()
        self.fc = fc
        self.conv = conv
        self.z = []
        self.a = []
        self.linear = []
        for i in range(self.fc.__len__()):
            if self.fc[i].name == "linear":
                self.linear.append(self.fc[i])
        
    def feedforward(self, features):
        super().feedforward(features)
        self.z = []
        self.a = []
        self.first_features = []
        for i in range(self.fc.__len__()):
            self.features = self.fc[i].forward(self.features)
            if i == 0:
                self.first_features.append(self.features)
            if self.fc[i].name == "linear":
                self.z.append(self.features)
            elif self.fc[i].name == "relu":
                self.a.append(self.features)