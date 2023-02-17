from core import core

class NeuralNetwork(core):
    def __init__(self) -> None:
        super().__init__()
        self.linear(input=2, output=2)
        test = self.linear.value


if __name__ == "__main__":
    neural = NeuralNetwork()