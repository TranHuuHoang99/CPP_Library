from lib import *

root_path = os.path.abspath(os.path.dirname(__file__))
root_csv_path = root_path + '\\raw_data\spam_text.csv'
csv_file = pandas.read_csv(root_csv_path)
spam_text = []

def debug_data():
    print(csv_file)

def __get_spam_text():
    _sub_spamtext = []
    for index in range(csv_file.shape[0]):
        _sub_spamtext = []
        if csv_file['Category'][index] == "spam":
            _sub_spamtext.append(csv_file['Category'][index])
            _sub_spamtext.append(csv_file['Message'][index])
            spam_text.append(_sub_spamtext)

def config_data():
    __get_spam_text()
    df= pandas.DataFrame(csv_file)
    step_item = 0

    for i in range(4482):
        step_item = i if i < (spam_text.__len__() - 1) else rand.randint(0,spam_text.__len__() - 1)
        df.loc[rand.randint(0,5570) + 0.5] = [spam_text[step_item][0], spam_text[step_item][1]]
        df = df.sort_index().reset_index(drop=True)
    df.to_csv(root_csv_path, index=False)

if __name__ == "__main__":
    # debug_data()
    config_data()