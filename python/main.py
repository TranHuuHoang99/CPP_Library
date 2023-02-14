from helper import *
from NeuralNetwork import CNN


def train():
    file_path = './dataset/tomato/tomato.jpg'
    file_des = './dataset/train_data/maxpooling.jpg'
    image = np.array(im.open(file_path))
    model = CNN(image)
    arr = model.feed_forward()
    print( 1 - arr[1])

if __name__ == "__main__":
    train()