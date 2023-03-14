from helper import Brain
from lib import pickle, os
from model import SeekerNN
from util import data, label, make_raw_data


def predict():
    root_path = os.path.abspath(os.path.dirname(__file__))
    root_brain_file = root_path + '\\seeker.brain'
    model = SeekerNN()
    brain:Brain = pickle.load(open(root_brain_file, "rb"))
    brain.set_model(model=model.model)
    brain.predict(features=data[111], label=label[111])
