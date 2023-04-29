# SMEM 0: 0 the starting vaddr of kernel
# SMEM 1: 16 the starting vaddr of matrix, also the size of kernel
# SMEM 2: 70000 the starting vaddr of result
# SMEM 3: 256 the size of matrix
# SMEM 4: 1
# SMEM 5: 65536 + 16
# SMEM 6: 64009 the ops needed
# Load addresses to scalar/vector reg
LS SR1 SR0 5        # SR1 = the stide offset = 65552
LV VR1 SR1          # VR1 = (0,1,2,3,64,65,66,67,128,129,130,131)
LS SR3 SR0 1        # SR3 = size of kernel = 16
MTCL SR3            # Set the VLR to 16
LS SR4 SR0 2        # SR4 = starting addr of reduction array = 70000
LS SR7 SR0 3        # SR7 = size of matrix = 256
LS SR6 SR0 4        # SR6 = 1
LV VR2 SR0          # Load the kernel = VR2
LS SR1 SR0 6        # SR1 = 64009 the ops needed
# Start of one conv
LVI VR3 SR0 VR1     # Loop1 start: Load the scattered memory
MULVV VR3 VR3 VR2   # Multiple first 16 of A and B to VR3
ADDVV VR0 VR0 VR3   # Add dp of first 16 of A and B to VR0
# Start of the array reduction, stored in VR0
SV VR0 SR4          # Loop2 start: reduction array now stored starting from addr 70000
BEQ SR3 SR6 7       # If SR3 == 1, reduced dp is already stored at 70000, branch to HALT
SRA SR3 SR3 SR6     # Shift right SR3 by 1 (SR3 /= 2)
MTCL SR3            # Set value in SR3 to VLR
ADD SR5 SR4 SR3     # SR5 is the addr of second half of the reduction array = 70000 + VLR
LV VR4 SR5          # Load the second half of the reduction array to VR1
ADDVV VR0 VR0 VR4   # Add the first and second half of the reduction array to VR0
BEQ SR0 SR0 -7      # jmp to reduction array store, Loop2 start
SUB SR1 SR1 SR6     # Decrement number of time still left
ADDVS VR1 VR1 SR6   # Increment VR1
ADD SR4 SR4 SR6     # The memory to put the result increment by 1
ADD SR2 SR2 SR6     # Increment SR2 once to indicate how many ops has been done
LS SR3 SR0 1        # SR3 = size of kernel = 16
MTCL SR3            # Set the VLR to 16
ADDVV VR0 VR5 VR5   # Clear the VR0
BNE SR0 SR1 -18     # If number of execution not reach the targeting number, start the conv again
HALT