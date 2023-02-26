from lib import *

image_path = './data/dataset'
image_folder = os.listdir(image_path + '/Training')

for index, val in enumerate(image_folder):
    image_file = os.listdir(image_path + '/Training/' + ""+val+"")
    print(image_file.__len__())