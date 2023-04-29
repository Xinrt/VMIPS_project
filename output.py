import numpy as np
import argparse
import os

def convolution2d(image, kernel, bias):
    m, n = kernel.shape
    if (m == n):
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y,x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i+m, j:j+m]*kernel) + bias
    return new_image

parser = argparse.ArgumentParser(description='Vector Core Performance Model')
parser.add_argument('-o', '--iodir', default="", type=str,
                        help='Path to the folder containing the input files - instructions and data.')
parser.add_argument('-k', '--kernel', default="", type=int,
                        help='dimention of the kernel')
parser.add_argument('-m', '--matrix', default="", type=int,
                        help='dimention of the matrix')
args = parser.parse_args()
iodir = os.path.abspath(args.iodir)
vdm_filepath = os.path.abspath(os.path.join(iodir, "VDMEM.txt"))
sdm_filepath = os.path.abspath(os.path.join(iodir, "SDMEM.txt"))
kernel_size = args.kernel
input_size = args.matrix
output_string = ""
with open(vdm_filepath, 'w') as f:
    # First write the kernel
    for _ in range(kernel_size):
        for j in range(1, kernel_size + 1):
            f.write(str(j) + '\n')
    # Then write the matrix
    for _ in range(input_size):
        for j in range(1, input_size + 1):
            f.write(str(j) + '\n')
    # Last write the scattered address
    for i in range(kernel_size):
        for j in range(kernel_size):
            f.write(str(kernel_size**2 + i * input_size + j) + '\n')

with open(sdm_filepath, 'w') as f:
    f.write("0" + "\n")
    f.write(str(kernel_size**2) + "\n")
    f.write("70000" + "\n")
    f.write(str(input_size) + "\n")
    f.write("1" + "\n")
    f.write(str(input_size**2 + kernel_size**2) + "\n")
    f.write(str(input_size - kernel_size + 1) + "\n")
    f.write(str(input_size) + "\n")

# Define the input matrix
input_matrix = np.array([list(range(1, input_size+1)) for _ in range(input_size)])
print("Matrix: ")
print(input_matrix)

# Define the kernel
num_rows = num_cols = kernel_size
kernel = np.array([[j for j in range(1, kernel_size + 1)] for i in range(num_rows)])
print("Kernel: ")
print(kernel)

# Define stride and output size
stride = 1
output_size = (input_matrix.shape[0] - kernel.shape[0]) // stride + 1
print("output_size: ", output_size)
# Perform convolution
# Print the output matrix
print("Expected Conv: ")
print(convolution2d(input_matrix, kernel, 0))