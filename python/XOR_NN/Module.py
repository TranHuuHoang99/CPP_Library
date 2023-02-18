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

        self.output_pred = ...

        self.weight = np.zeros([out_features, in_features], dtype=np.float16)
        self.bias = np.zeros([out_features], dtype=np.float16)

        for i in range(out_features):
            for j in range(in_features):
                self.weight[i,j] = rand.uniform(-1,1)
            self.bias[i] = 0

    def forward(self, features) -> np.ndarray:
        super().forward(features)
        self.output_pred = np.zeros([self.out_features], dtype=np.float16)
        for i in range(self.out_features):
            for j in range(self.in_features):
                self.output_pred[i] += features[j] * self.weight[i,j]
            self.output_pred[i] += self.bias[i]

        return self.output_pred

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
        self.linear = []
        for i in range(self.fc.__len__()):
            if self.fc[i].name == "linear":
                self.linear.append(self.fc[i])
        
    def feedforward(self, features):
        super().feedforward(features)

        for i in range(self.fc.__len__()):
            self.features = self.fc[i].forward(self.features)