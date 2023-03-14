from lib import *
from model import SeekerNN
from Module import linear, relu, sequence

LABEL = 'Category'
DATA = 'Message'


'''
    reshape all input array into 100 words
'''
def make_data(data_path):
    excel_file = pandas.read_csv(data_path)
    data_arr = []
    label_arr = []
    max_length = 910

    sum_ascii = 0
    get_word_total_ascii_int = []
    split_word = []
    for i in range(int(excel_file[LABEL].__len__())):
        label_arr.append(excel_file[LABEL][i])
        split_word = []
        split_word = excel_file[DATA][i].split()
        get_word_total_ascii_int = []
        for j in range(split_word.__len__()):
            sum_ascii = 0
            for k in range(split_word[j].__len__()):
                sum_ascii += (ord(split_word[j][k]) / 126)
            get_word_total_ascii_int.append(sum_ascii)
        data_arr.append(get_word_total_ascii_int)

    for i in range(data_arr.__len__()):
        if data_arr[i].__len__() > max_length:
            data_arr[i][:] = data_arr[i][: (data_arr[i].__len__() - (data_arr[i].__len__() - 100))]
        elif data_arr[i].__len__() < max_length:
            for new in range(int(max_length) - int(data_arr[i].__len__())):
                data_arr[i].append(int(0)) #32 equal to " " (space)
        else:
            pass
    
    data_arr = np.array(data_arr, dtype=np.uint32)
    length = data_arr.__len__()
    return label_arr, data_arr, length

def make_lable(input):
    if input == "ham":
        return [0,0]
    return [0,1]

def fit():
    model = SeekerNN()
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_brain = root_path + '\\seeker_nn.brain'
    root_excel_path = root_path + '\\raw_data\spam_text.csv'
    data = make_data(root_excel_path)

    # for epoch in range(100000):
    #     rand_sample = rand.randint(0,5571)
    #     model.model.forward_prop(data[1][rand_sample], label=make_lable(data[0][rand_sample]))
    #     model.model.backward_prop(label=make_lable(data[0][rand_sample]))
    #     model.model.gradient_descend()
    #     if (epoch%1000) == 0:
    #         print(model.model.features)
    #         print("LOSS IS : ", model.model.loss, " LABEL IS : ", data[0][rand_sample])
    #         print()
            
    # model.save(root_brain)
    print(data[0][111])
    predict = pickle.load(open(root_brain, "rb"))
    predict.set_model(model.model)
    predict.predict(data[1][111], make_lable(data[0][111]))


if __name__ == "__main__":
    fit()