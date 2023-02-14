LV VR0 SR0                  # VR0 = VDMEM[1:64] = [1,2,3,...,64]
LS SR1 SR1 3                # SR1 = 100
SVI VR0 SR1 VR0             # VDMEM[102:165] = [1,2,3,...,64] Test 16
HALT