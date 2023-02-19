from core import *
from core import core


class NeuralNetwork(core):
    def __init__(self) -> None:
        super().__init__()
        rand.seed(1234)
        self.model = sequence(
            fc=[
                linear(in_features=2, out_features=2),
                relu(),

                linear(in_features=2, out_features=1),
                relu()
            ]
        )

def atttach_lable(arr) -> int:
    if arr[0] == 0 and arr[1] == 1:
        return 1
    elif arr[0] == 0 and arr[1] == 0:
        return 0
    elif arr[0] == 1 and arr[1] == 1:
        return 0
    else:
        return 1


if __name__ == "__main__":
    model = NeuralNetwork()
    arr = [rand.randrange(0,1), rand.randrange(0,1)]
    for i in range(100):
        model.model.feedforward(arr)

        print(model.model.features)
        model.back_propagation(0.1, atttach_lable(arr=arr))
        

