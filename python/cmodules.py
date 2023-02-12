from helper import ctypes

c_function = ctypes.CDLL("c_output/matrix.so")

print(c_function.multiply_matrices(1,2))