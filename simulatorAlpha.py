#rei thao

import argparse
from bitstring import BitArray
import sys

'''b=BitArray(bin=imm) #imm is the binary value you wish to change to decimal

immediate=b.int
'''

Valid_R_Instruction = {
    "100000" : "add",
    "100010" : "sub",
}

Valid_I_Instruction = {
    "001000" : "addi"
}

Control_Signals = {
    "RegDst" : 0,         
    "ALUSrc" : 0,         
    "MemtoReg" : 0,
    "RegWrite" : 0,
    "MemRead" : 0,
    "MemWrite" : 0,
    "branch" : 0,
    "ALUOp1" : 0,
    "ALUOp2" : 0,       
    "Zero bit from ALU" : 0
}

Registers = {
    "Clock" : 65540,
    0 : 0,
    1 : 0,
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    7 : 0
}

def convert_Control(line): #assigns control
    combined_control = ''
    register = ''
    opcode = line[:6]
    rs = line[6:11]
    rt = line[11:16]
    rd = line[16:21]
    shamt = line[21:26]
    funct = line[26:]
    immediate = line[16:]

    if opcode == "000000":  # R-type (add, sub)
        Control_Signals["RegDst"] = 1
        Control_Signals["ALUSrc"] = 0
        Control_Signals["RegWrite"] = 1

        if funct == "100000":  # 'add' funct code
            Control_Signals["ALUOp1"] = 1
            Control_Signals["ALUOp2"] = 0
            Registers[int(rd,2)] = Registers[int(rs,2)] + Registers[int(rt,2)] #stores add result in register

        elif funct == "100010":  # 'sub' funct code

            Control_Signals["ALUOp1"] = 1  
            Control_Signals["ALUOp2"] = 0  
            Registers[int(rd,2)] = Registers[int(rs,2)] - Registers[int(rt,2)] #stores sub result in register

    elif opcode == "001000":  # I-type (addi)
        Control_Signals["RegDst"] = 0  
        Control_Signals["ALUSrc"] = 1  
        Control_Signals["RegWrite"] = 1
        Control_Signals["ALUOp1"] = 0  
        Control_Signals["ALUOp2"] = 0
        Registers[int(rt,2)] = Registers[int(rs,2)] + BitArray(bin=immediate).int #stores addi result in register
    
    for value in Control_Signals.values():
        combined_control += str(value)
    for value in Registers.values():
        register += str(value) + '|'
    return combined_control, register.strip('|') #returns register and control text lines

def parseInput(input_file, control, registers):
    output_file = open(control, 'w')
    register_file = open(registers, 'w')
    default_register = ''

    for value in Registers.values():
        if value == 65540:
            value -= 4
        default_register += str(value) + '|'
    register_file.write(default_register.strip('|') + '\n')

    
    with open(input_file, "r") as bin_file:
        for line in bin_file:
            instruction_counter = 0
            instruction = line.strip()
            
            converted_control,_ = convert_Control(instruction)
            _,converted_registers = convert_Control(instruction)

            output_file.write(converted_control + '\n')
            Registers["Clock"] += 4
            register_file.write(converted_registers + '\n')

            if instruction_counter == 100:
                print("Exiting.")
                sys.exit()

            instruction_counter += 1

    output_file.close   
    register_file.close 

    
def main():
    parser = argparse.ArgumentParser(description = 'Enter a text file to translate.')
    parser.add_argument("--program", type = str, help = 'Program File')
    args = parser.parse_args()

    if args.program is None: args.program = 'alpha.bin'

    output_control = open("out_control.txt", "w")
    output_control.close()
    output_control = "out_control.txt"

    output_registers = open("out_registers.txt", "w")
    output_registers.close()
    output_registers = "out_registers.txt"

    parseInput(args.program,output_control,output_registers)

if __name__ == "__main__":
    main()