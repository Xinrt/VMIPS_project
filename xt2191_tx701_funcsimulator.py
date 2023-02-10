import os
import argparse
import copy
import string
import re


class IMEM(object):
    def __init__(self, iodir):
        self.size = pow(2, 16)  # Can hold a maximum of 2^16 instructions.
        self.filepath = os.path.abspath(os.path.join(iodir, "Code.asm"))
        self.instructions:list[str] = []

        try:
            with open(self.filepath, 'r') as insf:
                self.instructions = [ins.split('#')[0].strip() for ins in insf.readlines() if not (ins.startswith('#') or ins.strip() == '')]
            print("IMEM - Instructions loaded from file:", self.filepath)
            # print("IMEM - Instructions:", self.instructions)
        except:
            print("IMEM - ERROR: Couldn't open file in path:", self.filepath)

    def Read(self, idx: int):  # Use this to read from IMEM.
        if idx < self.size:
            return self.instructions[idx]
        else:
            print("IMEM - ERROR: Invalid memory access at index: ", idx, " with memory size: ", self.size)


class DMEM(object):
    # Word addressible - each address contains 32 bits.
    # one address -> one instruction
    def __init__(self, name, iodir, addressLen):
        self.name = name
        self.size = pow(2, addressLen)  # sdmem: 2^13, vdmem:2^17 lines
        self.min_value = -pow(2, 31)
        self.max_value = pow(2, 31) - 1
        self.ipfilepath = os.path.abspath(os.path.join(iodir, name + ".txt"))
        self.opfilepath = os.path.abspath(os.path.join(iodir, name + "OP.txt"))
        self.data = []  # self.data is an int array

        try:
            with open(self.ipfilepath, 'r') as ipf:
                self.data = [int(line.strip()) for line in ipf.readlines()]
            print(self.name, "- Data loaded from file:", self.ipfilepath)
            # print(self.name, "- Data:", self.data)
            self.data.extend([0x0 for i in range(self.size - len(self.data))])
        except:
            print(self.name, "- ERROR: Couldn't open input file in path:", self.ipfilepath)

    def Read(self, idx: int) -> int:  # Use this to read from DMEM.
        """"For vector data memory, notice that the return value of Read is an int"""
        assert isinstance(idx, int), f"In DMEM read: idx expected an int, but got {type(idx).__name__}"
        assert (0 <= idx and idx < self.size), f"In DMEM read: idx must smaller than {self.size}, but got {idx}"

        return self.data[idx]

    def Write(self, idx: int, val: int):  # Use this to write into DMEM.
        """"For vector data memory, notice to pass val as an int"""
        assert isinstance(idx, int), f"In DMEM write: idx expected an int, but got {type(idx).__name__}"
        assert isinstance(val, int), f"In DMEM write: val expected an int, but got {type(val).__name__}"
        assert (0 <= idx and idx < self.size), f"In DMEM write: idx must smaller than {self.size}, but got {idx}"
        assert (self.min_value <= val and val <= self.max_value), f"In DMEM write: val must between {self.min_value} and {self.max_value}, but got {val}"

        self.data[idx] = val
        return

    def dump(self):
        try:
            with open(self.opfilepath, 'w') as opf:
                lines = [str(data) + '\n' for data in self.data]
                opf.writelines(lines)
            print(self.name, "- Dumped data into output file in path:", self.opfilepath)
        except:
            print(self.name, "- ERROR: Couldn't open output file in path:", self.opfilepath)


class RegisterFile(object):
    def __init__(self, name, count, length=1, size=32):
        self.name = name
        self.reg_count = count
        self.vec_length = length  # Number of 32 bit words in a register.
        self.reg_bits = size
        self.min_value = -pow(2, self.reg_bits - 1)
        self.max_value = pow(2, self.reg_bits - 1) - 1
        self.registers = [[0x0 for e in range(self.vec_length)] for r in
                          range(self.reg_count)]  # list of lists of integers

    def Read(self, idx: int) -> list(int):
        """"For scalar register, notice that the return value of Read is a list"""
        assert isinstance(idx, int), f"In RF read: idx expected an int, but got {type(idx).__name__}"
        assert (0 <= idx and idx < self.reg_count), f"In RF read: idx must smaller than {self.reg_count}, but got {idx}"

        return copy.deepcopy(self.registers[idx])

    def Write(self, idx: int, val: list(int)):
        """"For scalar register, notice to pass val as a list"""
        assert isinstance(val, list), f"In RF write: val expected a list, but got {type(val).__name__}"
        assert (0 <= idx and idx < self.reg_count), f"In RF write: idx must smaller than {self.reg_count}, but got {idx}"
        if self.vec_length == 1: # scalar RF
            assert (len(val) == 1), f"In RF write: scalar val expected to have only one element, but got {len(val)}"
        else: # vector RF
            assert (len(val) == 64), f"In RF write: vector val expected to have exact 64 element, but got {len(val)}"
        self.registers[idx] = copy.deepcopy(val)
        return

    def dump(self, iodir):
        opfilepath = os.path.abspath(os.path.join(iodir, self.name + ".txt"))
        try:
            with open(opfilepath, 'w') as opf:
                row_format = "{:<13}" * self.vec_length
                lines = [row_format.format(*[str(i) for i in range(self.vec_length)]) + "\n",
                         '-' * (self.vec_length * 13) + "\n"]
                lines += [row_format.format(*[str(val) for val in data]) + "\n" for data in self.registers]
                opf.writelines(lines)
            print(self.name, "- Dumped data into output file in path:", opfilepath)
        except:
            print(self.name, "- ERROR: Couldn't open output file in path:", opfilepath)


class Core():
    def __init__(self, imem:IMEM, sdmem, vdmem):
        self.IMEM = imem
        self.SDMEM = sdmem
        self.VDMEM = vdmem

        self.RFs = {"SRF": RegisterFile("SRF", 8),
                    "VRF": RegisterFile("VRF", 8, 64)}

        self.SRF = self.RFs["SRF"]
        self.VRF = self.RFs["VRF"]

        self.PC = 0
        self.VLR = 64
        self.VMR = [1 for i in range(64)]

    def parseInstr(instrStr: str):
        instrList = instrStr.split(' ')
        return instrList

    # def RF_READ(rf_str: str, idx: int, RFs: dict(RegisterFile)):
    #     re_match = re.match("(\w{2})(\d)", rf_str)
    #     if re_match[0] == "VR":
    #         # read on Vector Reg
    #         return RFs["VRF"].Read(idx)
    #     elif re_match[0] == "SR":
    #         # read on Scalar Reg
    #         return RFs["SRF"].Read(idx)

    # def RF_WRITE(rf_str: str, idx: int, val: list(int), RFs: dict(RegisterFile)):
    #     re_match = re.match("(\w{2})(\d)", rf_str)
    #     if re_match[0] == "VR":
    #         # write on Vector Reg
    #         RFs["VRF"].Write(idx, val)
    #     elif re_match[0] == "SR":
    #         # write on Scalar Reg
    #         RFs["SRF"].Write(idx, val)

    def run(self):
        while (True):
            instr = self.parseInstr(self.IMEM.Read(self.PC))
            op = instr[0]

            # Vector Operations
            if re.match("(ADD|SUB|MUL|DIV)\w{2}", op):
                rd = int(instr[1][2])
                rs1 = int(instr[2][2])
                rs2 = int(instr[3][2])

                # copy the value of rd into temporary list, remain the length=64
                temp_list = self.VRF.Read(rd)
                match op:
                    case "ADDVV":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]+self.VRF.Read(rs2)[i]
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "SUBVV":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]-self.VRF.Read(rs2)[i]
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "ADDVS":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]+self.SRF.Read(rs2)
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "SUBVS":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]-self.SRF.Read(rs2)
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "MULVV":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]*self.VRF.Read(rs2)[i]
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "DIVVV":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]//self.VRF.Read(rs2)[i]
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "MULVS":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]*self.SRF.Read(rs2)
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case "DIVVS":
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VRF.Read(rs1)[i]//self.SRF.Read(rs2)
                        self.VRF.Write(rd, temp_list)
                        # pass
                    case _ :
                        print("Core run - ERROR: Vector Operations invalid operation ", op)
            # Vector Mask Register Operations
            elif re.match("(S\w{2}(VV|VS))|CVM|POP", op):
                rs1 = int(instr[1][2])
                rs2 = int(instr[2][2])
                vr1 = self.VRF.Read(rs1)
                match op:
                    case "SEQVV":
                        vr2 = self.VRF.Read(rs2)
                        for idx in range(64):
                            if vr1[idx] == vr2[idx]:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SNEVV":
                        vr2 = self.VRF.Read(rs2)
                        for idx in range(64):
                            if vr1[idx] != vr2[idx]:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SGTVV":
                        vr2 = self.VRF.Read(rs2)
                        for idx in range(64):
                            if vr1[idx] > vr2[idx]:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SLTVV":
                        vr2 = self.VRF.Read(rs2)
                        for idx in range(64):
                            if vr1[idx] < vr2[idx]:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SGEVV":
                        vr2 = self.VRF.Read(rs2)
                        for idx in range(64):
                            if vr1[idx] >= vr2[idx]:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SLEVV":
                        vr2 = self.VRF.Read(rs2)
                        for idx in range(64):
                            if vr1[idx] <= vr2[idx]:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SEQVS":
                        scalar = self.SRF.Read(rs2)[0]
                        for idx in range(64):
                            if vr1[idx] == scalar:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SNEVS":
                        scalar = self.SRF.Read(rs2)[0]
                        for idx in range(64):
                            if vr1[idx] != scalar:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SGTVS":
                        scalar = self.SRF.Read(rs2)[0]
                        for idx in range(64):
                            if vr1[idx] > scalar:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SLTVS":
                        scalar = self.SRF.Read(rs2)[0]
                        for idx in range(64):
                            if vr1[idx] < scalar:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SGEVS":
                        scalar = self.SRF.Read(rs2)[0]
                        for idx in range(64):
                            if vr1[idx] >= scalar:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case "SLEVS":
                        scalar = self.SRF.Read(rs2)[0]
                        for idx in range(64):
                            if vr1[idx] <= scalar:
                                self.VMR[idx] = 1
                            else:
                                self.VMR[idx] = 0
                    case _ :
                        print("Core run - ERROR: Vector Mask Operations invalid operation ", op)
            elif op == "CVM":
                self.VMR = [1 for i in range(64)]
            elif op == "POP":
                rs = int(instr[1][2])
                self.SRF.Write(rs, [self.VMR.count(1)])
            # Vector Length Register Operations
            elif op == "MTCL" or op == "MFCL":
                rs = int(instr[1][2])
                if op == "MTCL":
                    sr = self.SRF.Read(rs)[0]
                    assert (0 <= sr and sr < 64), f"In MTCL: val must between 0 and 63, but got {sr}"
                    self.VLR = sr
                elif op == "MFCL":
                    self.SRF.Write([self.VLR])
                else:
                    print("Core run - ERROR: Vector Length Mask Operations invalid operation ", op)
            # Memory Access Operations 
            elif op == "LV" or op == "SV":
                rs1 = int(instr[1][2])
                rs2 = int(instr[2][2])
                address0 = self.SRF.Read(rs2)[0]
                
                if op == "LV":
                    temp_list = [0x0 for i in range(64)]
                    # sdmem: 2^13, vdmem:2^17 
                    # assert (0 <= address and address < pow(2, 13)), f"In LV: index must between 0 and 2^13, but got {address}"
                    for i in range(self.VLR):
                        # starting address: 
                        if self.VMR[i] == 1:
                            temp_list[i] = self.VDMEM.Read(address0+i)
                    self.VRF.Write(rs1, temp_list)
                    # pass
                elif op == "SV":
                    for i in range(self.VLR):
                        if self.VMR[i] == 1:
                            self.VDMEM.Write(address0+i, self.VRF.Read(rs1)[i])
                    # pass
                else:
                    print("Core run - ERROR: Memory Access Operations LV/SV invalid operation ", op)
            elif re.match("((LV|SV)\w{1,2})", op):
                rs1 = int(instr[1][2])
                rs2 = int(instr[2][2])
                rs3 = int(instr[3][2])
                address0 = self.SRF.Read(rs2)[0]
                temp_list = [0x0 for i in range(64)]
                match op:
                    case "LVWS":
                        stride = self.SRF.Read(rs3)[0]
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VDMEM.Read(address0+i*stride)
                        self.VRF.Write(rs1, temp_list)
                        # pass
                    case "SVWS":
                        stride = self.SRF.Read(rs3)[0]
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                self.VDMEM.Write(address0+i*stride, self.VRF.Read(rs1)[i])
                        # pass
                    case "LVI":
                        offset = self.VRF.Read(rs3)
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                temp_list[i] = self.VDMEM.Read(address0+offset[i])
                        self.VRF.Write(rs1, temp_list)
                        # pass
                    case "SVI":
                        offset = self.VRF.Read(rs3)
                        for i in range(self.VLR):
                            if self.VMR[i] == 1:
                                self.VDMEM.Write(address0+offset[i], self.VRF.Read(rs1)[i])
                        # pass
                    case _ :
                        print("Core run - ERROR: Memory Access Operations invalid operation ", op)
            elif op == "LS" or op == "SS":
                rs1 = int(instr[1][2])
                rs2 = int(instr[2][2])
                imm = int(instr[3])
                address0 = self.SRF.Read(rs2)[0]
                
                if op == "LS":
                    temp_list = [0x0]
                    temp_list[0] = self.SDMEM.Read(address0+imm)
                    self.SRF.Write(rs1, temp_list)
                    # pass
                elif op == "SS":
                    value = self.SRF.Read(rs1)[0]
                    self.SDMEM.Write(address0+imm, value)
                    # pass
                else:
                    print("Core run - ERROR: Memory Access Operations LS/SS invalid operation ", op)
            # Scalar Operations
            elif op == "ADD" or op == "SUB" or op == "AND" or op == "OR" or op == "XOR" or op == "SLL" or op == "SRL" or op == "SRA":
                rd = int(instr[1][2])
                rs1 = int(instr[2][2])
                rs2 = int(instr[3][2])
                match op:
                    case "ADD":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] + self.SRF.Read(rs2)[0]])
                    case "SUB":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] - self.SRF.Read(rs2)[0]])
                    case "AND":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] & self.SRF.Read(rs2)[0]])
                    case "OR":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] | self.SRF.Read(rs2)[0]])
                    case "XOR":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] ^ self.SRF.Read(rs2)[0]])
                    case "SLL":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] << self.SRF.Read(rs2)[0]])
                    case "SRL":
                        self.SRF.Write(rd, [(self.SRF.Read(rs1)[0] % 0x100000000) >> self.SRF.Read(rs2)[0]])
                    case "SRA":
                        self.SRF.Write(rd, [self.SRF.Read(rs1)[0] >> self.SRF.Read(rs2)[0]])
                    case _ :
                        print("Core run - ERROR: Scalar Operations invalid operation ", op)
            # Control
            elif re.match("B\w{2}", op):
                rs1 = int(instr[1][2])
                rs2 = int(instr[2][2])
                imm = int(instr[3])
                assert (-(2 ** 20) <= imm and imm <= (2 ** 20)), f"In Control: imm must between {-(2 ** 20)} and {(2 ** 20)}, but got {imm}"
                match op:
                    case "BEQ":
                        if self.SRF.Read(rs1)[0] == self.SRF.Read(rs2)[0]:
                            self.PC += imm - 1
                    case "BNE":
                        if self.SRF.Read(rs1)[0] != self.SRF.Read(rs2)[0]:
                            self.PC += imm - 1
                    case "BGT":
                        if self.SRF.Read(rs1)[0] > self.SRF.Read(rs2)[0]:
                            self.PC += imm - 1
                    case "BLT":
                        if self.SRF.Read(rs1)[0] < self.SRF.Read(rs2)[0]:
                            self.PC += imm - 1
                    case "BGE":
                        if self.SRF.Read(rs1)[0] >= self.SRF.Read(rs2)[0]:
                            self.PC += imm - 1  
                    case "BLE":
                        if self.SRF.Read(rs1)[0] <= self.SRF.Read(rs2)[0]:
                            self.PC += imm - 1
                    case _ :
                        print("Core run - ERROR: Control Operations invalid operation ", op)
            # Halt
            elif op == "HALT":
                return
            else:
                print("Core - ERROR: Operation invalid ", op)

            self.PC = self.PC + 1

    def dumpregs(self, iodir):
        for rf in self.RFs.values():
            rf.dump(iodir)


if __name__ == "__main__":
    # parse arguments for input file location
    parser = argparse.ArgumentParser(description='Vector Core Performance Model')
    parser.add_argument('--iodir', default="", type=str,
                        help='Path to the folder containing the input files - instructions and data.')
    args = parser.parse_args()

    iodir = os.path.abspath(args.iodir)
    print("IO Directory:", iodir)

    # Parse IMEM
    imem = IMEM(iodir)
    # Parse SMEM
    sdmem = DMEM("SDMEM", iodir, 13)  # 32 KB is 2^15 bytes = 2^13 K 32-bit words.
    # Parse VMEM
    vdmem = DMEM("VDMEM", iodir, 17)  # 512 KB is 2^19 bytes = 2^17 K 32-bit words.

    # Create Vector Core
    vcore = Core(imem, sdmem, vdmem)

    # Run Core
    vcore.run()
    vcore.dumpregs(iodir)

    sdmem.dump()
    vdmem.dump()

    # THE END
