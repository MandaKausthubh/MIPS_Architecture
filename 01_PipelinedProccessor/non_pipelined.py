


pc=4194304
instruction_mem={}
data_mem={}
init=0

for i in range(101):
    data_mem[init+(4*i)]=0
data_mem[0]=24
data_mem[4]=2   #instructions to feed input for sorting
data_mem[8]=3


    


clock_cycles=0
"""mips_registers = {#for reference
    0: "$zero",   # Always 0
    1: "$at",     # Assembler temporary #4194304
    2: "$v0",     # Return value
    3: "$v1",     # Return value
    4: "$a0",     # Argument 0
    5: "$a1",     # Argument 1
    6: "$a2",     # Argument 2
    7: "$a3",     # Argument 3
    8: "$t0",     # Temporary 0
    9: "$t1",     # Temporary 1
    10: "$t2",    # Temporary 2
    11: "$t3",    # Temporary 3
    12: "$t4",    # Temporary 4
    13: "$t5",    # Temporary 5
    14: "$t6",    # Temporary 6
    15: "$t7",    # Temporary 7
    16: "$s0",    # Saved 0
    17: "$s1",    # Saved 1
    18: "$s2",    # Saved 2
    19: "$s3",    # Saved 3
    20: "$s4",    # Saved 4
    21: "$s5",    # Saved 5
    22: "$s6",    # Saved 6
    23: "$s7",    # Saved 7
    24: "$t8",    # Temporary 8
    25: "$t9",    # Temporary 9
    26: "$k0",    # Kernel 0
    27: "$k1",    # Kernel 1
    28: "$gp",    # Global pointer
    29: "$sp",    # Stack pointer
    30: "$fp",    # Frame pointer
    31: "$ra"     # Return address
}"""
mips_reg_file=[0]*32
mips_reg_file[9]=3 
mips_reg_file[10]=0     #instructions to feed input for sorting
mips_reg_file[11]=16

#mips_reg_file[11]=40 #instruction to feed input for factorial

rd=0
rs=0
rt=0
shamt=0
funct=0
initial_addr=4194304

input_file="Sorting_machine_code.txt" #name of whatever file to be read from replace here
with open(input_file,"r") as file:
    for line in file:
        instr=(line.strip())
        instruction_mem[initial_addr]=instr
        initial_addr=initial_addr+4

while(((pc-4194304)/4)<len(instruction_mem)):#use pc as control counter
    if(instruction_mem[pc][0:6]=="000000"):#r Type opcode is 0 (this line is IF stage),below lines decode the 32 bit instruction.ie ID stage
        rd=int(instruction_mem[pc][16:21],2)
        rs=int(instruction_mem[pc][6:11],2)
        rt=int(instruction_mem[pc][11:16],2)
        shamt=int(instruction_mem[pc][21:26],2)
        funct=int(instruction_mem[pc][26:32],2)#put all to some temp and then in wb  put to rd

        if(funct==32):#EX stage where we read funct field and decide arithmetic/logical operation on input and do it using ALU
            temp=mips_reg_file[rs]+mips_reg_file[rt]
        elif(funct==0):
            temp=mips_reg_file[rt]<<shamt
        elif(funct==2):
            temp ==mips_reg_file[rt]>>shamt
        elif(funct==34):
            temp=mips_reg_file[rs]-mips_reg_file[rt]
        elif(funct==36):
            temp=mips_reg_file[rs]&mips_reg_file[rt]
        elif(funct==37):
            temp=mips_reg_file[rs]|mips_reg_file[rt]
        elif(funct==38):
            temp=mips_reg_file[rs]^mips_reg_file[rt]
        elif(funct==39):
            temp=~(mips_reg_file[rs]|mips_reg_file[rt])
        elif(funct==42):
            if(mips_reg_file[rs]<mips_reg_file[rt]):
                temp=1
            else:
                temp=0
        mips_reg_file[rd]=temp#writeback phase
        clock_cycles=clock_cycles+5
    
    elif(instruction_mem[pc][0:6]=="100011"):# lw instruction
        rs=int(instruction_mem[pc][6:11],2)#ID(instruction decode phase),decode everything to decimal
        rt=int(instruction_mem[pc][11:16],2)
        imm=int(instruction_mem[pc][16:32],2)

        temp=mips_reg_file[rs]+imm#EX phase i.e add rs and imm
        #print(pc)
        #print("imm:",imm)
        #print("rs value",mips_reg_file[13])
        #print("bin",instruction_mem[pc][6:11])
        temp1=data_mem[temp]#MEM ,memory access phase
        mips_reg_file[rt]=temp1 #WB, that is writeback phase where the memory data is written back to register
        clock_cycles=clock_cycles+5

    elif(instruction_mem[pc][0:6]=="101011"):# sw instruction(IF  stage)
        rs=int(instruction_mem[pc][6:11],2)#ID(instruction decode phase),decode everything to decimal
        rt=int(instruction_mem[pc][11:16],2)
        imm=int(instruction_mem[pc][16:32],2)

        temp=mips_reg_file[rs]+imm#EX phase i.e add rs and imm
        data_mem[temp]=mips_reg_file[rt]#MEM ,memory access phase where we write to memory address given by ALU output and content is in register rt
        clock_cycles=clock_cycles+5
    
    elif(instruction_mem[pc][0:6]=="001000"):# addi instruction(IF  stage)
        rs=int(instruction_mem[pc][6:11],2)#ID(instruction decode phase),decode everything to decimal
        rt=int(instruction_mem[pc][11:16],2)
        imm=int(instruction_mem[pc][16:32],2)
        #print(pc)
        #print(instruction_mem[pc][16:32])

        temp=mips_reg_file[rs]+imm#EX phase i.e add rs and imm
        mips_reg_file[rt]=temp#WB ,write back phase where alu outptu is written back to register rt(in register file)
        clock_cycles=clock_cycles+5
    
    elif(instruction_mem[pc][0:6]=="000100"):# beq instruction(IF  stage)
        rs=int(instruction_mem[pc][6:11],2)#ID(instruction decode phase),decode everything to decimal
        rt=int(instruction_mem[pc][11:16],2)
        imm=int(instruction_mem[pc][16:32],2)
        branch=1#branch is set to 1 to indicate branching instruction
        zero=0#zero signal from ALU
        temp=pc+4+(imm*4)
        pcsrc=0#controls whether pc should change

        if(mips_reg_file[rs]==mips_reg_file[rt]):#EX phase i.e compare rs and rt
            zero=1
        if(zero and branch):
            pcsrc=1
        clock_cycles=clock_cycles+5
        if(pcsrc==1):
            pc=temp
            continue
        

    elif(instruction_mem[pc][0:6]=="000010"):# jump(j) instruction(IF  stage)
        jump=1#indicates that it is a jump signal
        #ID(instruction decode phase),decode jump adrress and convert it to 32 bit form  and then to decimal
        jump_addr="0000"+instruction_mem[pc][6:32]+"00"#concatenate 4 zeros as MSB and concatenate 2 zeros to LSBi.e left shift by 2 to get ddress in 32 bit form
        jump_addr=int(jump_addr,2)
        clock_cycles=clock_cycles+5
        if(jump==1):
            pc=jump_addr
            continue
    
    elif(instruction_mem[pc][0:6]=="011100"):#mul instruction(IF stage)
        rd=int(instruction_mem[pc][16:21],2)#decode the instruction to get rs,rt,rd(ID stage)
        rs=int(instruction_mem[pc][6:11],2)
        rt=int(instruction_mem[pc][11:16],2)
        temp23=mips_reg_file[rs]*mips_reg_file[rt]#EXE phase
        mips_reg_file[rd]=temp23#WB phase where ALU result written back to rd
        clock_cycles=clock_cycles+5
        
        
    
    pc=pc+4
print(data_mem)
print(mips_reg_file)
print(clock_cycles)
    

            
    

        












