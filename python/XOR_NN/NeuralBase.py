from helper import *

class Model: ...

class NeuralBase:
    def __init__(self) -> None:
        self.weight = []
        self.bias = []
        self.model = Model()

    def linear(self, input: int, output: int) -> None:
        weight = np.zeros([output, input], dtype=np.float64)
        bias = np.zeros([output], dtype=np.float64)

        for i in range(output):
            for j in range(input):
                weight[i,j] = rand.uniform(-1,1)
            bias[i] = 0
        self.weight.append(weight)
        self.bias.append(bias)

if __name__ == "__main__":
    neural = NeuralBase()
    neural.linear(2,2)
    neural.linear(2,1)
    print(neural.weight, "\n", neural.bias)