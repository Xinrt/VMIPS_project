# SMEM 0: 0 the starting vaddr of kernel
# SMEM 1: kernel_dim**2 the starting vaddr of matrix, also the size of kernel
# SMEM 2: 70000 the starting vaddr of result
# SMEM 3: input_size the dimension of matrix
# SMEM 4: 1
# SMEM 5: input_size*input_size + kernel_dim*kernel_dim
# SMEM 6: (input_size-kernel_dim+1) = the ops needed for each row and col

# SR0 = constant 0
# SR1 = COL index start with 0
# SR2 = ROW index start with 0
# SR3
# SR4 is the address of memory to put
# SR5 
# SR6 = constant 1
# SR7 is the output row/col

# VR0 stores the current row stride offset of matrix
# VR1 stores the base stride offset of matrix
# VR2 stores the kernel
# VR3 stores the matrix
# Load addresses to scalar/vector reg
LS SR5 SR0 5        # SR5 = the stride offset
LS SR3 SR0 1        # SR3 = whole size of kernel = kernel_dim**2
LV VR1 SR5          # VR1 = base stride offset of matrix
MTCL SR3            # Set the VLR to whole size of kernel
LS SR4 SR0 2        # SR4 = starting addr of reduction array = 70000
LS SR6 SR0 4        # SR6 = 1
ADDVV VR0 VR0 VR1   # Load the scattered memory to base stride offset of matrix
LV VR2 SR0          # Load the kernel = VR2
LS SR7 SR0 6        # Set the SR7 to be the output row/col
# Start the COL
LVI VR3 SR1 VR0     # Load the current stride offset of matrix(VR0) + COL index to VR3
MULVV VR3 VR3 VR2   # Multiple first 16 of A and B to VR3
# Start of the array reduction, stored in VR3
SV VR3 SR4          # Loop2 start: reduction array now stored starting from addr 70000
BEQ SR3 SR6 7       # If SR3 == 1, reduced dp is already stored at 70000, branch to HALT
SRA SR3 SR3 SR6     # Shift right SR3 by 1 (SR3 /= 2)
MTCL SR3            # Set value in SR3 to VLR
ADD SR5 SR4 SR3     # SR5 is the addr of second half of the reduction array = 70000 + VLR
LV VR4 SR5          # Load the second half of the reduction array to VR4
ADDVV VR3 VR3 VR4   # Add the first and second half of the reduction array to VR3
BEQ SR7 SR7 -7      # jmp to reduction array store, Loop2 start
# Start of checking COL index
ADD SR4 SR4 SR6     # Increment SR4, the memory to put
LS SR3 SR0 1        # Set the SR3 to be the kernel_size
MTCL SR3            # Set the VLR to be the kernel_size
ADD SR1 SR1 SR6     # Increment the COL index
BLT SR1 SR7 -14     # If the COL index is less than output, branch to the start of COL
# Start of checking ROW index
ADD SR2 SR2 SR6     # Increment the ROW index
LS SR5 SR0 3        # Load the input matrix dim to SR5
ADDVS VR0 VR1 SR5   # Move the matrix to the next ROW
ADD SR1 SR0 SR0     # Reset SR1 to 0
BLT SR2 SR7 -19     # If the ROW index is less than output, branch to the start of COL
HALT