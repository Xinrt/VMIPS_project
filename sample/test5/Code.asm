LS SR1, SR0, 0
LS SR2, SR0, 6
ADD SR3, SR0, SR1
BNE SR3, SR2, -1
LS SR4, SR0, 3
SUB SR5, SR3, SR1
BGT SR3, SR5, 2
SUB SR5, SR5, SR1
ADD SR5, SR5, SR1
BEQ SR5, SR3, -1
BLT SR1, SR4, 3
SUB SR5, SR5, SR4
SUB SR5, SR5, SR4
ADD SR5, SR5, SR4
BGE SR3, SR2, 2
ADD SR5, SR5, SR4
SUB SR3, SR3, SR4
BLE SR5, SR3, -1
ADD SR5, SR5, SR4
HALT