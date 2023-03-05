from lib import *

# input = "hg pr"

# avg_ascii = 0
# word_order = 0
# index = 0

# features_in = []
# for i  in input:
#     index += 1
#     if i == " ":
#         avg_ascii = avg_ascii / word_order
#         features_in.append(avg_ascii)
#         avg_ascii = 0
#         word_order = 0
#         if index == input.__len__():
#             pass
#         else:
#             continue
#     word_order += 1
#     avg_ascii += ord(i)

#     if index == input.__len__():
#         avg_ascii = avg_ascii / word_order
#         features_in.append(avg_ascii)

root_path = os.path.abspath(os.path.dirname(__file__))
root_file_path = root_path + '\\raw_data\spam_text.csv'
excel_file = open(root_file_path, "r")
count = 0
for i in excel_file:
    print(i[0])
    count += 1
    if count == 10:
        break
    
    