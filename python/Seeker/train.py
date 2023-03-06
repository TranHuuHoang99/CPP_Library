from lib import *

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
    for i in range(int(excel_file[LABEL].__len__() / 2)):
        label_arr.append(excel_file[LABEL][i])
        get_word_total_ascii_int = []
        for j in range(excel_file[DATA][i].split().__len__()):
            sum_ascii = 0
            for k in range(excel_file[DATA][i].split()[j].__len__()):
                sum_ascii += ord(excel_file[DATA][i].split()[j][k])
            get_word_total_ascii_int.append(sum_ascii)
        data_arr.append(get_word_total_ascii_int)

    for i in range(data_arr.__len__()):
        if data_arr[i].__len__() > 100:
            data_arr[i][:] = data_arr[i][: (data_arr[i].__len__() - (data_arr[i].__len__() - 100))]
        elif data_arr[i].__len__() < 100:
            for new in range(int(100) - int(data_arr[i].__len__())):
                data_arr[i].append(int(0))
        else:
            pass



if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_excel_path = root_path + '\\raw_data\spam_text.csv'
    make_data(root_excel_path)