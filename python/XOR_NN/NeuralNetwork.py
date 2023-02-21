from core import *
from core import core


class NeuralNetwork(core):
    def __init__(self) -> None:
        super().__init__()
        # rand.seed(1234)
        self.model = sequence(
            fc=[
                linear(in_features=2, out_features=64),
                relu(),

                linear(in_features=64, out_features=128),
                relu(),

                linear(in_features=128, out_features=32),
                relu(),

                linear(in_features=32, out_features=1),
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
    
    # for i in range(200):
    #     arr = [rand.randint(0,1), rand.randint(0,1)]
    #     model.model.feedforward(arr)
    #     print("accuracy :", model.model.features, " loss: ", 1 - model.model.features)
    #     model.back_propagation(0.001, atttach_lable(arr=arr))
    # model.save("XOR_NN.brain")

    predict:Brain = pickle.load(open('XOR_NN.brain', "rb"))
    print(predict.predict([1,0], NeuralNetwork=model))

