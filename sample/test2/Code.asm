LS SR0 SR0 1            # SR0 = 4
ADDVS VR0 VR0 SR0       # VR0 = [4,4,4,...,4] Test2
SUBVS VR1 VR1 SR0       # VR1 = [-4,-4,-4,...,-4] Test2
ADDVS VR2 VR2 SR0       # VR2 = [4,4,4,...,4]
SUBVS VR3 VR3 SR0       # VR3 = [-4,-4,-4,...,-4]
MULVS VR2 VR2 SR0       # VR2 = [16,16,16,...,16] Test4
DIVVS VR3 VR3 SR0       # VR2 = [-1,-1,-1,...,-1] Test4
LS SR1 SR1 2            # SR1 = 5
SEQVS VR0 SR1           # VLM = [0,0,0,...,0,0,0] Test6
SNEVS VR0 SR1           # VLM = [1,1,1,...,1,1,1] Test6
SGTVS VR0 SR1           # VLM = [0,0,0,...,0,0,0] Test6
SLTVS VR0 SR1           # VLM = [1,1,1,...,1,1,1] Test6
SGEVS VR0 SR1           # VLM = [0,0,0,...,0,0,0] Test6
SLEVS VR0 SR0           # VLM = [1,1,1,...,1,1,1] Test6
POP SR2                 # SR2 = 64 Test8
MFCL SR3                # SR3 = 64 Test10
SV VR4 SR0              # VDMEM[5,68] = [0,0,0,...,0] Test12
LS SR4 SR4 0            # SR4 = 2
LS SR5 SR5 3            # SR5 = 100
SVWS VR0 SR5 SR4        # VDMEM[101,103,105,...,227] = [4,4,4,...,4] Test 14
SS SR5 SR4 10           # SDMEM[13] = 100 Test18
AND SR1 SR1 SR0         # SR1 = 5 & 4 = 4 Test20
OR SR4 SR4 SR0          # SR4 = 2 | 4 = 6 Test20
XOR SR5 SR5 SR4         # SR5 = 100 ^ 6 = 98 Test20
LS SR6 SR6 4            # SR6 = -98
SRA SR6 SR6 SR1         # SR6 = -98 >> 4 = -7 Test 22 
HALT                    # Test 24