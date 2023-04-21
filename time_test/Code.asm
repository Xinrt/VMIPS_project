# A address: SDMEM 0: 0 TODO: Set A and B to 0,1,2,...,449
# B address: SDMEM 1: 450
# array size: SDMEM 1: 450
LS SR1 SR0 0        # SR1 = A address = 0
LS SR2 SR0 1        # SR2 = B address = 450
ADD SR7 SR2 SR0     # SR7 = array length = 450
# Start of the length 2 array dp
LS SR3 SR0 2        # SR3 = first length size = 2
MTCL SR3            # Load first array op length to 2
LV VR1 SR1          # Load first two of A in VR1
LV VR2 SR2          # Load first two of B in VR2
MULVV VR1 VR1 VR2   # Multiple first two of A and B to VR1
ADDVV VR0 VR0 VR1   # Add dp of first two of A and B to VR0
ADD SR1 SR1 SR3     # Increment addr of A by 2
ADD SR2 SR2 SR3     # Increment addr of B by 2
# Start of the length 64 array dp loop
LS SR3 SR0 3        # SR3 = rest length size = 64
MTCL SR3            # Set VLR to 64
LV VR1 SR1          # Loop1 start: Load first 64 of A in VR1
LV VR2 SR2          # Load first 64 of B in VR2
MULVV VR1 VR1 VR2   # Multiple first 64 of A and B to VR1
ADDVV VR0 VR0 VR1   # Add dp of first 64 of A and B to VR0
ADD SR1 SR1 SR3     # Increment addr of A by 64
ADD SR2 SR2 SR3     # Increment addr of B by 64
BLT SR1 SR7 -6      # If start addr of A(SR1) less than 450, branch to Loop1 start
# Start of the array reduction, stored in VR0
LS SR6 SR0 4        # SR6 = 1
LS SR7 SR0 5        # SR7 = starting addr of reduction array = 2048
SV VR0 SR7          # Loop2 start: reduction array now stored starting from addr 2048
BEQ SR3 SR6 7       # If SR3 == 1, reduced dp is already stored at 2048, branch to HALT
SRA SR3 SR3 SR6     # Shift right SR3 by 1 (SR3 /= 2)
MTCL SR3            # Set value in SR3 to VLR
ADD SR5 SR7 SR3     # SR5 is the addr of second half of the reduction array = 2048 + VLR
LV VR1 SR5          # Load the second half of the reduction array to VR1
ADDVV VR0 VR0 VR1   # Add the first and second half of the reduction array to VR0
BEQ SR0 SR0 -7      # jmp to reduction array store, Loop2 start
HALT                # End of execution, address 2048 in VDMEM should be 30273825