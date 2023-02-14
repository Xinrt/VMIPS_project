LV VR0 SR0              # VR0 = [2,2,2,...,2] Test11
ADDVV VR2 VR1 VR0       # VR2 = [2,2,2,...,2] Test1
SUBVV VR3 VR0 VR1       # VR3 = [-2,-2,-2,...,-2] Test1
SEQVV VR3 VR2           # VMR = [0,0,0,...,0] Test5
SNEVV VR3 VR2           # VMR = [1,1,1,...,1] Test5
SGTVV VR3 VR2           # VMR = [0,0,0,...,0] Test5
SLTVV VR3 VR2           # VMR = [1,1,1,...,1] Test5
SGEVV VR3 VR2           # VMR = [0,0,0,...,0] Test5
SLEVV VR3 VR2           # VMR = [1,1,1,...,1] Test5
CVM                     # VMR = [1,1,1,...,1] Test7
LS SR1 SR0 0            # SR1 = [6] Test17
MTCL SR1                # VLR = 6 Test9
LVWS VR4 SR0 SR1        # VR4 = [2,2,2,2,2,2,0,...,0] Test13
LVI VR5 SR0 VR0         # VR5 = [2,2,2,2,2,2,0,...,0] Test15
ADD SR2 SR0 SR1         # SR2 = [6] Test19
SUB SR3 SR0 SR1         # SR3 = [-6] Test19
SLL SR4 SR1 SR2         # SR4 = 6 (0000...0110) left shift 6 = (000110000...000) = 402653184 Test21
SRL SR5 SR1 SR2         # SR4 = 6 (0000...0110) right shift 6 = (0000...0011000000) = 384 Test21
HALT                    # Test 24