from helper import *

class NeuralBase:
    def __init__(self) -> None:
        rand.seed(1234)
        self.features = ...

    def update_data(self, input) -> None:
        self.features = input

    def linear(self, input, output):
        self.linear.value = 1999
        weight = np.zeros([output, input], dtype=np.float64)
        bias = np.zeros([output], dtype=np.float64)
        features_out = np.zeros([output], dtype=np.float64)

        for i in range(output):
            for j in range(input):
                weight[i,j] = rand.uniform(-1,1)
            bias[i] = 0

        print(weight, "\n")
        print("-----------", "\n")
        print(bias, "\n")
        print("==========================================================================================", "\n")

        if self.features is Ellipsis:
            return

        self.features = np.array(self.features, dtype=np.float64)
        
        for i in range(output):
            for j in range(input):
                features_out[i] += self.features[j] * weight[i,j]
            features_out[i] += bias[i]

        print(weight, "\n")
        print("-----------", "\n")
        print(bias, "\n")
        print("-----------", "\n")
        print(features_out, "\n")
        print("==========================================================================================", "\n")
        self.features = features_out