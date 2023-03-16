from lib import *

root_path = os.path.abspath(os.path.dirname(__file__))
root_csv_path = root_path + '\\raw_data\spam_text.csv'
spam_list = []

def config_data():
    csv_file = pandas.read_csv(root_csv_path)
    df = pandas.DataFrame(csv_file)
    spam_list.append(df.loc[123])
    

if __name__ == "__main__":
    config_data()
    print(spam_list)

