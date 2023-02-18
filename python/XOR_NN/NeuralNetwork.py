from core import *
from core import core


class NeuralNetwork(core):
    def __init__(self) -> None:
        super().__init__()
        rand.seed(1234)
        self.model = sequence(fc=[
            linear(in_features=2, out_features=2),
            relu(),
            
            linear(in_features=2, out_features=1),
            relu()
        ])



if __name__ == "__main__":
    model = NeuralNetwork()
    for i in range(2):
        model.model.feedforward([rand.randrange(0,1),1])
        model.back_propagation(1,1)

        print("epoch end ------------------------------------------------------------------------------------------")