from lib import *

input_text = "my name is hoang pro dn"
output_text = input_text.split()

sum_ascii = 0
dataset = []
for i in range(output_text.__len__()):
    sum_ascii = 0
    for j in range(output_text[i].__len__()):
        sum_ascii += ord(output_text[i][j])
    dataset.append(sum_ascii)

