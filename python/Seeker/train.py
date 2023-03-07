from lib import *
from model import SeekerNN, XORNN

LABEL = 'Category'
DATA = 'Message'


'''
    reshape all input array into 100 words
'''
def make_data(data_path):
    excel_file = pandas.read_csv(data_path)
    data_arr = []
    label_arr = []
    
    max_length = 100

    sum_ascii = 0
    get_word_total_ascii_int = []
    split_word = []
    for i in range(int(excel_file[LABEL].__len__() / 2)):
        label_arr.append(excel_file[LABEL][i])
        split_word = []
        split_word = excel_file[DATA][i].split()
        get_word_total_ascii_int = []
        for j in range(split_word.__len__()):
            sum_ascii = 0
            for k in range(split_word[j].__len__()):
                sum_ascii += ord(split_word[j][k])
            get_word_total_ascii_int.append(sum_ascii)
        data_arr.append(get_word_total_ascii_int)

    for i in range(data_arr.__len__()):
        if data_arr[i].__len__() > 910:
            data_arr[i][:] = data_arr[i][: (data_arr[i].__len__() - (data_arr[i].__len__() - 100))]
        elif data_arr[i].__len__() < 910:
            for new in range(int(910) - int(data_arr[i].__len__())):
                data_arr[i].append(int(0))
        else:
            pass
    
    data_arr = np.array(data_arr, dtype=np.uint32)
    length = data_arr.__len__()
    return label_arr, data_arr, length

def make_lable(input):
    if input == "ham":
        return [1,0]
    return [0,1]

def relu(input: float):
    if (input < 0).any():
        return -input
    return input

def cal_loss(pred, label):
    avg_pred = 0
    for i in range(label.__len__()):
        avg_pred += (relu((pred[i] - label[i])))
    return avg_pred / label.__len__()

def seeker_fit():
    model = SeekerNN()
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_brain = root_path + '\\seeker_nn.brain'
    root_excel_path = root_path + '\\raw_data\spam_text.csv'
    data = make_data(root_excel_path)
    learning_rate = 0.01

    for i in range(data[2]):
        print("EPOCH : %d, LABEL : %a, %s"%(i,make_lable(data[0][i]), data[0][i]))
        model.model.forward_prop(data[1][i])
        loss = cal_loss(pred=model.model.output, label=make_lable(data[0][i]))
        print("loss : ", loss)
        model.model.backward_prop(learning_rate=learning_rate, label=make_lable(data[0][i]))

    model.save(root_brain)
    # print(data[0][159])
    # predict = pickle.load(open(root_brain, "rb"))
    # print(predict.prediction_value(data[1][159], model))

def atttach_lable(arr) -> np.float64:
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

def xor_fit():
    model = XORNN()
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_brain = root_path + '\\xornn.brain'
    for i in range(100000):
        arr = [np.float64(rand.randint(0,1)), np.float64(rand.randint(0,1))]
        model.model.forward_prop(arr)
        print("INPUT : ", arr[0], " ", arr[1], " LABEL IS: ", atttach_lable(arr=arr))
        print("accuracy : ", 1 - (none_minus(atttach_lable(arr=arr) - model.model.output[0])), "loss : ", (none_minus(atttach_lable(arr=arr) - model.model.output[0])))
        print()
        model.model.backward_prop(0.1, atttach_lable(arr=arr))

    model.save("XOR_NN.brain")

    print("\n")

    predict = pickle.load(open(root_brain, "rb"))
    predict.prediction_value([1,1], NeuralNetwork=model)
    

if __name__ == "__main__":
    # xor_fit()
    seeker_fit()