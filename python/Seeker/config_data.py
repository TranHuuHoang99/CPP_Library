from lib import *

root_path = os.path.abspath(os.path.dirname(__file__))
root_csv_path = root_path + '\\raw_data\spam_text.csv'
csv_file = pandas.read_csv(root_csv_path)
spam_text = []

def debug_data():
    print(csv_file)

def config_data():
    df= pandas.DataFrame(csv_file)
    df.loc[5570] = ['spam', 'Hoangprodn']
    df.to_csv(root_csv_path, index=False)


if __name__ == "__main__":
    # debug_data()
    config_data()