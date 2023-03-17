from lib import *

DATA = 'Message'
LABEL = 'Category'
SPEC_CHAR = "`~!@#$%^&*()-_=+[]{\}|;:''"",<.>/?"
MAXIMUM_ASCII = 122

data = []
label = []

def make_raw_data():
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_file_path = root_path + "\\raw_data\spam_text.csv"
    excel_file = pandas.read_csv(root_file_path)

    raw_data = []
    raw_label = []

    for _data in excel_file[DATA]:
        for sp_char in SPEC_CHAR:
            _data = _data.replace(sp_char, '')
        raw_data.append(_data)

    for _label in excel_file[LABEL]:
        raw_label.append(_label)

    to_ascii(raw_data=raw_data, raw_label=raw_label)

def attach_label(name):
    if name == "spam":
        return [0,0]
    elif name == "ham":
        return [0,1]
    
def to_ascii(raw_data, raw_label):
    data_sp = []
    for i in range(raw_data.__len__()):
        data_sp.append(raw_data[i].split())

    data_ascii = []
    sum_of_ascii = 0
    for i in range(data_sp.__len__()):
        data_ascii = []
        for j in range(data_sp[i].__len__()):
            sum_of_ascii = 0
            for word in data_sp[i][j]:
                sum_of_ascii += ord(word) / MAXIMUM_ASCII
            data_ascii.append(sum_of_ascii / data_sp[i][j].__len__())
        data.append(data_ascii)

    for i in range(raw_label.__len__()):
        label.append(attach_label(raw_label[i]))
    