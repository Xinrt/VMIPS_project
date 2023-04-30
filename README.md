# VMIPS Project

## Part 2 - Timing Simulator

### Environment Request
```
python >= 3.11.0
```
### Usage
```
<!-- Generate the required resolved_Code.asm and the vlr.txt for timing simulator -->
python xt2191_tx701_funcsimulator.py --iodir [path/to/the/test]
<!-- Perform performance test on the assembly -->
<!-- All the three test case are in sample folder called conv, dp and fc -->
<!-- The output should be an instruction_latency.txt contains -->
<!-- total cycle count, the current config and the per-instruction latency -->
python xt2191_tx701_timingsimulator.py --iodir [path/to/the/test]
```

### Block Diagram

https://drive.google.com/file/d/1S4prlxiWLBiUCTZyhvQu7hd75QJbSpg1/view?usp=sharing



**IMEM**: stores all instructions that can be read (Code.asm file)

**VRF**: contains 8 Vector Registers each with a maximum capacity of 2048 bits or 256 bytes or 64

32-bit elements. Maximum Vector Length is set to 64

**SRF**: contains 8 Scalar Registers of 32 bits each

**VDMEM:** Vector Data Memory with a capacity of **512 KB**, word addressable

**SDMEM:** Scalar Data Memory with a capacity of **32 KB**, word addressable.

### Question to ask
- [x] Q: If there is a stall should I still IF?
  - A: 
- [x] Q: how will stall number be calculated? 
  - A: it does not have to be calculated
- [x] Q: what is VDM partition?
  - A: Banks partition the memories in interleaved way.
- [x] Q: for the vlsPipelineDepth, can I assume each vector mem load/store will simply cost vlsPipelineDepth cycle? Or they should also be vlsPipelineDepth + number of vector elements load/store - 1?
  - A:
- [x] Q: what determines stall in mem access? ![bank_conflict](readme_pic/WeChat%20Image_20230420232250.png)
  - A: The formula should be greatest common divisor
- [x] Q: what about Scalar MEM? should I also resolve the scalar memory conflict? Or they simply take one cycle so they don't need to resolve the conflict? suppose I have LV VR0 (0, 1, 2, …. 63) then LV VR1 (0, 1, 2, …. 63), do I need to stall the second instruction? **code line 541**
  - A: 
- [x] Q: expected output? per cycle or per instruction, or both?
  - A: only need an overall cycle time
- [x] Q: Cycle needed for Vector Mask Register Operations? **code line 408**
  - A:keep it same with add
- [x] Q: What will happen in the vector compute if the VLR == 0? **code line 186**
  - A: only go throught the pipelineDepth cycle
- [x] Q: Are Vmem access complete as a whole, or it can be cleared from VMEM Busyboard one by one? **code line 208**
  - A: It is access one memory by one memory
- [x] Q: If not, how frequently will the memory back? **code line 300**
  - A: One memory by one memory
- [x] Q: What registers will be count as busy, all of them? Or only the write back one?
  - A: only the WB one
- [x] Q: Do both LV(read mem) or SV(write) mems counted as busy, all of them? Or only the write back one?
  - A: The busy one is the bank, not the mem address
- [x] Q: naming of resolved code file?
  - A: Depending on my own implementation
- [x] Q: use of vlr.txt? what is its conventional name?
  - A: That's OK
- [x] Q: performance of your design for all three functions: what three? DP, FC, and?
  - A: Depending on my own implementation
- [x] Q: When WB to vector register, do I need to check whether rd is also busy? code line 412(Vector compute), 538(Vector mem) Maybe because there are two pipeline for compute and mem access and ordering for WB is important
  - A: Yes WB still needed to be checked
- [x] Q: What about WB to scalar register, since they are all 1 cycle, do I really need to care whether rd will have conflict? code line 566(Scalar mem), 590(Scalar compute)
  - A: Yes WB still needed to be checked
- [x] Q: The busyboard update seems have some bugs, for example when two consecutive instructions are going to write to a same register rd, then when the first one got back the busyborad will be cleared but the second one still have to secure the rd, **maybe change the busyboard as a semephore rather than a lock?**
  - A:Use semephore maybe


### TODO
- [x] Functional simulator
  - [x] Modify functional simulator to generate resolved instructions
    - [x] Memory Access
    - [x] Branch
  - [x] Modify functional simulator to generate VLR
- [x] Timing simulator
  - [x] Backend
  - [x] Frontend
- [x] Fully Connected Layer Assembly
- [x] Conv Layer Assembly
- [ ] Optimization
- [ ] Measure and plot the performance of your design for all three functions (including the dot product from part1) by varying the model parameters (different configurations)
- [ ] report
- [ ] block diagram

### Report

https://www.overleaf.com/6474812394bgkjvbmvrgps









## Part 1 - Functional Simulator

### TODO

- [x] VMR should not affect execution, it should only affect WB and mem access

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
