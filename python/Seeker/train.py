from util import label, data, make_raw_data
from lib import *
from helper import *
from model import SeekerNN
from predict import predict

make_raw_data()
label = np.array(label, dtype=np.uint8)
max_len = 171
for i in range(data.__len__()):
    if data[i].__len__() < max_len:
        for time in range(max_len - data[i].__len__()):
            data[i].append(0)

data = np.array(data, dtype=np.float64)
    

def fit(model: SeekerNN, path):
    count = 0
    for epoch in range(50):
        count = 0
        for i in range(label.shape[0]):
            model.model.forward_prop(features=data[i], label=label[i])
            model.model.backward_prop(label=label[i])
            model.model.gradient_descend()
            if (i/label.size) >= (count/50):
                print("#", sep= ' ', end='', flush=True)
                count += 1
        print(" LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)
    model.save(path=path)

def predict():
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_brain_file = root_path + '\\seeker.brain'
    model = SeekerNN()
    brain:Brain = pickle.load(open(root_brain_file, "rb"))
    brain.set_model(model=model.model)
    brain.predict(features=data[159], label=label[159])

if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_bin_file = root_path + '\\seeker.brain'
    model = SeekerNN()
    # fit(model=model, path=root_bin_file)
    predict()