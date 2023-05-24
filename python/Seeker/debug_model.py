from lib import *
from helper import *

class XOR:
    def __init__(self) -> None:
        self.model = sequence(seed=1234)
        self.model.learning_rate = 0.1

        self.model.add(linear(features_in=2, features_out=8))
        self.model.add(relu(features_in=8))

        self.model.add(linear(features_in=8, features_out=2))
        self.model.add(relu(features_in=2))

def make_label(arr):
    if arr[0] == 0 and arr[1] == 0:
        return [0,0]
    elif arr[0] == 1 and arr[1] == 1:
        return [0,1]
    elif arr[0] == 0 and arr[1] == 1:
        return [1,0]
    return [1,1]

if __name__ == "__main__":
    model = XOR()
    for i in range(100000):
        data = [rand.randint(0,1), rand.randint(0,1)]
        model.model.forward_prop(features=data, label=make_label(data))
        model.model.backward_prop(label=make_label(data))
        model.model.gradient_descend()
        if (i%10000) == 0:
            print(" LABEL IS : ", data)
            print(" LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)

    print()
    print(" LABEL PRED IS : ", [0,0])
    model.model.forward_prop(features=[0,0], label=make_label([0,0]))
    print(" LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)

    print(" LABEL PRED IS : ", [1,1])
    model.model.forward_prop(features=[1,1], label=make_label([1,1]))
    print(" LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)

    print(" LABEL PRED IS : ", [0,1])
    model.model.forward_prop(features=[0,1], label=make_label([0,1]))
    print(" LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)

    print(" LABEL PRED IS : ", [1,0])
    model.model.forward_prop(features=[1,0], label=make_label([1,0]))
    print(" LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)


