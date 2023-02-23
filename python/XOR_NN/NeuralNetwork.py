from core import *
from core import core


class NeuralNetwork(core):
    def __init__(self) -> None:
        super().__init__()
        # rand.seed(4)
        self.model = sequence(
            fc=[
                linear(in_features=2, out_features=2),
                relu(),

                linear(in_features=2, out_features=1),
                relu()
            ]
        )

def atttach_lable(arr) -> np.float64:
    if arr[0] == 0 and arr[1] == 1:
        return 1
    elif arr[0] == 0 and arr[1] == 0:
        return 0
    elif arr[0] == 1 and arr[1] == 1:
        return 0
    else:
        return 1

def none_minus(input) -> np.float64:
        if input < 0:
            return -input
        return input

if __name__ == "__main__":
    model = NeuralNetwork()
    
    for i in range(100000):
        arr = [np.float64(rand.randint(0,1)), np.float64(rand.randint(0,1))]
        model.model.feedforward(arr)
        print("INPUT : ", arr[0], " ", arr[1], " LABEL IS: ", atttach_lable(arr=arr))
        print("accuracy : ", 1 - (none_minus(atttach_lable(arr=arr) - model.model.features[0])), " loss : ", (none_minus(atttach_lable(arr=arr) - model.model.features[0])))
        print()
        model.back_propagation(0.1, atttach_lable(arr=arr))

    model.save("XOR_NN.brain")

    print("\n")

    predict:Brain = pickle.load(open('XOR_NN.brain', "rb"))
    predict.predict([1,1], NeuralNetwork=model)

