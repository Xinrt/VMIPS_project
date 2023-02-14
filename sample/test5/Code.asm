LS SR1 SR0 0            # SR1 = 1 Test17
LS SR2 SR0 6            # SR2 = 7 Test17
ADD SR3 SR0 SR1         # SR3 = 8 Test19
BNE SR3 SR2 1           # PC = 4 Test23
LS SR4 SR0 3            # SR4 = 4 Test17
SUB SR5 SR3 SR1         # SR5 = 7 Test19
BGT SR3 SR5 2           # PC = 8 Test23
SUB SR5 SR5 SR1         # SR5 = 6 Test19
ADD SR5 SR5 SR1         # SR5 = 7 Test19 ... SR5 = 8
BEQ SR5 SR3 -1          # PC = 8 Test23
BLT SR1 SR4 3           # PC = 13 Test23
SUB SR5 SR5 SR4         # SR5 = 4 Test19
SUB SR5 SR5 SR4         # SR5 = 0 Test19
ADD SR5 SR5 SR4         # SR5 = 4 Test19
BGE SR3 SR2 2           # PC = 15 Test23
ADD SR5 SR5 SR4         # SR5 = 8 Test19
SUB SR3 SR3 SR4         # SR3 = 4 Test19
BLE SR5 SR3 -1          # PC = 18 Test23
ADD SR5 SR5 SR4         # SR5 = 12 Test19
HALT                    # Test 24