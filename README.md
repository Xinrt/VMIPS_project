# VMIPS Project

## Part 2 - Timing Simulator

### Block Diagram

https://drive.google.com/file/d/1S4prlxiWLBiUCTZyhvQu7hd75QJbSpg1/view?usp=sharing



### Report

https://www.overleaf.com/6474812394bgkjvbmvrgps





## Part 1 - Functional Simulator

### TODO

- [ ] VMR should not affect execution, it should only affect WB and mem access

### Questions

- Q: Will S__VV S__VS also set the respective bit to 0?
  - A: **Yes**
- Q: What happends to the bits in VMR if we increase/decrease the VLR. Will they be the default value? Or will they remain what it is?
  - A: **VMR won't change**
- Q: Does **VLR** affect Memory Access operations?
  - **YES**, there will only be as many memory accesses as the number in VLR.
- Q: Does **VMR** affect Memory Access operations?
  - **YES**, we only write back data into those elements with their VM set to 1.

### VMIPS components

- DMEM: Xinran
  - Vector DMEM
  - Register DMEM
- Register Files: Tianheng
  - Scalar Register File
  - Vector Register File
- Vector Mask Register(int list): 64 bits
- Vector Length Register(int): 32 bits
- Add assert in DMEM and RF read, write on idx and val.
  - DMEM
    - type
    - range
    - val max min
  - RF
    - type
    - range
    - val max min

### Test Cases

- dot product function
- instruction verification functions
  verify all 22 instructions in the ISA and submit its output
  - test1:
    1 5 7 9 11 13 15 17 19 21
  - test2:
    2 4 6 8 10 12 14 18 20 22 24
  - test3:
    3
  - test4:
    16
  - test5:
    23
