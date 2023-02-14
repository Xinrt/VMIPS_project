# VMIPS_project
## **Questions**
- Q: Will S__VV S__VS also set the respective bit to 0?
- Q: What happends to the bits in VMR if we increase/decrease the VLR. Will they be the default value? Or will they remain what it is?
- Q: Does VMR affect Memory Access operations?
## Part 1 - Functional Simulator

### Task

#### complete the VMIPS components

- [x] DMEM: Xinran
  - Vector DMEM
  - Register DMEM
- [x] Register Files: Tianheng
  - Scalar Register File
  - Vector Register File
- [x] Vector Mask Register(int list): 64 bits
- [x] Vector Length Register(int): 32 bits
- [x] Add assert in DMEM and RF read, write on idx and val.
  - [x] DMEM
    - [x] type
    - [x] range
    - [x] val max min
  - [x] RF
    - [x] type
    - [x] range
    - [x] val max min

#### two functions

- dot product function
  **TODO:** 
  how to write dot product function in assembly?

  computes the dot product of two vectors of 450 elements each and store the result in to address 2048 of VDMEM

- instruction verify function

  verifies all 22 instructions in the ISA and submit its output



#### instructions
- 22 instructions
  - parsing
  - execute

- 24 instructions tests
  - test1:
    1 5 7 9 11 13 15 17 19 21
  - test3:
    3
  - test5:
    23







