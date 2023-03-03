from lib import *
from helper import *
from SeekerNN import SeekerNN

def atttach_lable(arr):
    if arr[0] == 0 and arr[1] == 1:
        return [1]
    elif arr[0] == 0 and arr[1] == 0:
        return [0]
    elif arr[0] == 1 and arr[1] == 1:
        return [0]
    else:
        return [1]

def none_minus(input) -> np.float64:
    if input < 0:
        return -input
    return input


if __name__ == "__main__":
    model = SeekerNN()
    
    for i in range(100000):
        arr = [np.float64(rand.randint(0,1)), np.float64(rand.randint(0,1))]
        model.model.forward_prop(arr)
        print("INPUT : ", arr[0], " ", arr[1], " LABEL IS: ", atttach_lable(arr=arr))
        print("accuracy : ", 1 - (none_minus(atttach_lable(arr=arr) - model.model.output[0])), " loss : ", (none_minus(atttach_lable(arr=arr) - model.model.output[0])))
        model.model.backward_prop(0.1, atttach_lable(arr=arr))

    root_path = os.path.abspath(os.path.dirname(__file__))
    model.save("%s/SeekerNN.brain"%(root_path))

    predict:Brain = pickle.load(open('%s/SeekerNN.brain'%(root_path), "rb"))
    predict.predict([1,1], NeuralNetwork=model)
