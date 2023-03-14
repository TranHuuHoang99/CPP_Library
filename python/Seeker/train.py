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
    for epoch in range(100000):
        rand_value = rand.randint(0,5571)
        model.model.forward_prop(features=data[rand_value], label=label[rand_value])
        model.model.backward_prop(label=label[rand_value])
        model.model.gradient_descend()
        if (epoch % 10000) == 0:
            print("LABEL IS : ", label[rand_value])
            print("LOSS IS : ", model.model.loss, " PRED IS : ", model.model.features)
    model.save(path=path)

if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_bin_file = root_path + '\\seeker.brain'
    model = SeekerNN()
    # fit(model=model, path=root_bin_file)
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_brain_file = root_path + '\\seeker.brain'
    model = SeekerNN()
    brain:Brain = pickle.load(open(root_brain_file, "rb"))
    brain.set_model(model=model.model)
    brain.predict(features=data[159], label=label[159])