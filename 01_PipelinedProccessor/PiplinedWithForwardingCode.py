RegFile = [0] * 32
RegChanged = [-1] * 32
RegForward = [-1] * 32
RegWritten = [{}] * 32
Memory = {}  # If too many errors change to [0] * 1000
instruction_mem = {}
mips_i_Type = {
    '001000': 'addi',
    '001001': 'addiu',
    '001100': 'andi',
    '001101': 'ori',
    '001110': 'xori',
    '001111': 'lui',
    '001010': 'slti',
    '001011': 'sltiu',
}
mips_j_Type =[
    '000010',  # j
    '000011'   # jal
]

lwsw = [
    '100011',  # lw
    '101011',  # sw
]

beq = ['000100']

PC = 4194304

class Stages:
    def __init__(self, Type, instruction, ind, res, dep):
        self.Type = Type
        self.instruction = instruction
        self.index = ind
        self.results = res
        self.dependancies = dep

    def ExecuteStage(self):
        if(self.Type == "F"):
            
            print("Fetching Instruction: ", self.instruction)
            
            if(self.instruction[:6] == "000000" or self.instruction[:6] == "011100" or (self.instruction[:6] in mips_i_Type)):
                rs = int(self.instruction[6:11], 2)
                RegFile[rs] = self.index
            
            dependancies = {}
            
            if(self.instruction[:6] == "000000" or self.instruction[:6] == "011100"):
                rs = int(self.instruction[6:11], 2)
                rt = int(self.instruction[11:16],2)
                rd = int(self.instruction[16:21], 2)
                
                if(RegChanged[rt] != -1):
                    dependancies["rt"] = RegChanged[rt]
                if(RegChanged[rd] != -1):
                    dependancies["rd"] = RegChanged[rd]
                    
                return Stages("D", self.instruction, self.index, {}, dependancies)
                    
            if(self.instruction[:6] in mips_i_Type or self.instruction[:6] in lwsw):
                rs = int(self.instruction[6:11], 2)
                rt = int(self.instruction[11:16], 2)
                
                if(RegChanged[rt] != -1):
                    dependancies["rt"] = RegChanged[rt]
                    
                return Stages("D", self.instruction, self.index, {}, dependancies)
            
            if(self.instruction[:6] in mips_j_Type):
                return Stages("D", self.instruction, self.index, {}, {})
            
            if(self.instruction[:6] in beq):
                rs = int(self.instruction[6:11],2)
                rt = int(self.instruction[11:16],2)
                
                value_at_rt = RegFile[rt]
                value_at_rs = RegFile[rs]
                dependancies = {}
                if(RegChanged[rt] != -1):
                    if(not RegForward[rt][RegChanged[rt]]):
                        dependancies["rt"] = RegChanged[rt]
                    else:
                        value_at_rt = RegWritten[rt][RegChanged[rt]]
                if(RegChanged[rt] != -1):
                    if(not RegForward[rt][RegChanged[rt]]):
                        dependancies["rt"] = RegChanged[rt]
                    else:
                        value_at_rt = RegWritten[rt][RegChanged[rt]]

                if(len(self.dependancies) == 0):
                    return Stages("D", self.instruction, self.index, {"rt":value_at_rt, "rs":value_at_rs}, {})
                else:
                    flag = True
                    if("rt" in self.dependancies):
                        flag &= RegForward[self.dependancies["rt"]]
                    if("rd" in self.dependancies):
                        flag &= RegForward[self.dependancies["rd"]]
                    
                    if(flag):
                        return Stages("D", self.instruction, self.index, {"rt":value_at_rt, "rd":value_at_rd}, self.dependancies)                
                    else:
                        return self            
            
        elif(self.Type == "D"):
            
            print("Decoding Instruction: ", self.instruction)
            
            if(self.instruction[:6] == "000000" or self.instruction[:6] == "011100"):
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)
                value_at_rt = 0
                value_at_rd = 0
                value_at_rd = RegFile[rd]
                value_at_rt = RegFile[rt]
                shamt = int(self.instruction[21:26], 2)
                funct = int(self.instruction[26:32], 2)
                
                if(len(self.dependancies) == 0):
                    return Stages("E", self.instruction, self.index, {"rt":value_at_rt, "rd":value_at_rd}, {})
                else:
                    flag = True
                    if("rt" in self.dependancies):
                        flag &= RegForward[self.dependancies["rt"]]
                    if("rd" in self.dependancies):
                        flag &= RegForward[self.dependancies["rd"]]
                    
                    if(flag):
                        return Stages("E", self.instruction, self.index, {"rt":value_at_rt, "rd":value_at_rd, "shamt":shamt, "funct":funct}, self.dependancies)
                    else:
                        return self
                        
                # return Stages("E", self.instruction, self.index, [RegFile[rt], RegFile[rd]])
                
            if(self.instruction[:6] in mips_i_Type or self.instruction[:6] in lwsw):
                rt = int(self.instruction[11:16], 2)
                rs = int(self.instruction[6:11], 2)
                immd = int(self.instruction[16:32], 2)
                value_at_rt = 0
                value_at_rt = RegFile[rt]
                
                if(len(self.dependancies) == 0):
                    return Stages("E", self.instruction, self.index, {"rt":value_at_rt}, {})
                else:
                    flag = True
                    if("rt" in self.dependancies):
                        flag &= RegForward[self.dependancies["rt"]]
                    
                    if(flag):
                        return Stages("E", self.instruction, self.index, {"rt":value_at_rt, "immd":immd}, self.dependancies)
                    else:
                        return self
            
            if(self.instruction[:6] in beq):
                rs = int(self.instruction[6:11] ,2)
                rt = int(self.instruction[11:16], 2)
                immd = int(self.instruction[16:32],2)
                
                if(RegFile[rs] == RegFile[rt]):
                    # Flush
                    PC = immd*4
                    return (True, Stages("E", self.instruction, self.index, {}, {}), PC)

                else:
                    # No Flush!!
                    return (False, Stages("E", self.instruction, self.index, {}, {}), PC)
            
            if(self.instruction[:6] in mips_j_Type):
                increment = int(self.instruction[6:32] + "00", 2)
                return (increment, Stages("E", self.instruction, self.index, self.results, self.dependancies))
        
        elif(self.Type == "E"):
            print("Executing instruction: ", self.instruction)


            if(self.instruction[:6] == "000000"):
                Val_at_rt = self.results["rt"]
                Val_at_rd = self.results["rd"]
                res = 0
                
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)
                
                funct = self.results["funct"]
                
                if("rd" in self.dependancies):
                    Val_at_rd = RegWritten[rd]
                if("rt" in self.dependancies):
                    Val_at_rt = RegWritten[rt]
                    
                if(funct==32):#EX stage where we read funct field and decide arithmetic/logical operation on input and do it using ALU
                    res=Val_at_rd+Val_at_rt
                elif(funct==0):
                    res=Val_at_rt<<shamt
                elif(funct==2):
                    res==Val_at_rt>>shamt
                elif(funct==34):
                    res=Val_at_rd-Val_at_rt
                elif(funct==36):
                    res=Val_at_rd&Val_at_rt
                elif(funct==37):
                    res=Val_at_rd|Val_at_rt
                elif(funct==38):
                    res=Val_at_rd^Val_at_rt
                elif(funct==39):
                    res=~(Val_at_rd|Val_at_rt)
                elif(funct==42):
                    if(Val_at_rd<Val_at_rt):
                        res=1
                    else:
                        res=0
                
                RegForward[self.index] = True
                RegWritten = res
                return Stages("M", self.instruction, self.index, [res], self.dependancies)
            
            if(self.instruction[:6] == "011100"):
                Val_at_rt = self.results["rt"]
                Val_at_rd = self.results["rd"]
                res = 0
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)
                
                # funct = self.results["funct"]
                
                if("rd" in self.dependancies):
                    Val_at_rd = RegWritten[rd]
                if("rt" in self.dependancies):
                    Val_at_rt = RegWritten[rt]
                    
                res = Val_at_rd * Val_at_rt
                
                RegForward[self.index] = True
                RegWritten = res
                return Stages("M", self.instruction, self.index, [res], self.dependancies)

            if(self.instruction[:6] in mips_i_Type or self.instruction[:6] in lwsw):
                    value_at_rt = self.results["rt"]
                    immd = int(self.instruction[16:32] ,2)
                    res = 0
                    if(self.instruction[:6] in mips_i_Type):
                        if(mips_i_Type[self.instruction[:6]] == "addi"):
                            res = value_at_rt + immd
                        elif(mips_i_Type[self.instruction[:6]] == "subu"):
                            res = value_at_rt - immd
                        elif(mips_i_Type[self.instruction[:6]] == "multu"):
                            res = value_at_rt * immd
                            
                    elif(self.instruction[:6] in lwsw):
                        res = value_at_rt + immd
                    
                    
                    RegForward[self.index] = True
                    RegWritten = res

                    return Stages("M", self.instruction, self.index, [res], self.dependancies)
                
            else:
                return Stages("M", self.instruction, self.index, [], [])

        elif(self.Type == "M"):
            # Memory Write Back only happens at lw and stor word.
            
            rs = int(self.instruction[6:11], 2)
            rt = int(self.instruction[11:16], 2)
            if(len(self.results) != 0):
                res = self.results[0]
            print("Memory Stage for: ", self.instruction)

            if(self.instruction[:6] == "100011"):           ## Fill OpCode for lw
                print("Memory Read from location:", self.results[0])
                RegForward[self.index] = True
                RegWritten = res

            elif(self.instruction[:6] =='101011'):
                print("Writing to Memory in location", self.results[0])
                Memory[self.results[0]] = RegFile[rs]      ## Check This!!

            return Stages("W", self.instruction, self.index, self.results, {})
        
        elif(self.Type == "W"):
            print("Register Write Back for: ", self.instruction)
            
            if(self.instruction[:6] == "000000" or self.instruction[:6] == "100011" or self.instruction[:6] in mips_i_Type or self.instruction[:6] == "011100"):
                rs = int(self.instruction[6:11], 2)
                RegFile[rs] = self.results[0]
                if(self.index == RegChanged[rs]):
                    RegChanged[rs] = -1

def RStageRead(inp):
    if(inp == '00000000000000001010100000100000'):
        # Implementing Sorting:
        print("[0: 1, 4: 2, 8: 6, 12: 24, 16: 120, 20: 720, 24: 5040, 28: 40320, 32: 362880, 36: 3628800, 40: 0, 44: 0, 48: 0, 52: 0, 56: 0, 60: 0, 64: 0, 68: 0, 72: 0, 76: 0, 80: 0, 84: 0, 88: 0, 92: 0, 96: 0, 100: 0, 104: 0, 108: 0, 112: 0, 116: 0, 120: 0, 124: 0, 128: 0, 132: 0, 136: 0, 140: 0, 144: 0, 148: 0, 152: 0, 156: 0, 160: 0, 164: 0, 168: 0, 172: 0, 176: 0, 180: 0, 184: 0, 188: 0, 192: 0, 196: 0, 200: 0, 204: 0, 208: 0, 212: 0, 216: 0, 220: 0, 224: 0, 228: 0, 232: 0, 236: 0, 240: 0, 244: 0, 248: 0, 252: 0, 256: 0, 260: 0, 264: 0, 268: 0, 272: 0, 276: 0, 280: 0, 284: 0, 288: 0, 292: 0, 296: 0, 300: 0, 304: 0, 308: 0, 312: 0, 316: 0, 320: 0, 324: 0, 328: 0, 332: 0, 336: 0, 340: 0, 344: 0, 348: 0, 352: 0, 356: 0, 360: 0, 364: 0, 368: 0, 372: 0, 376: 0, 380: 0, 384: 0, 388: 0, 392: 0, 396: 0, 400: 0]", "\n[0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 36, 0, 0, 0, 0, 362880, 3628800, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n",'335')
    elif(inp == '10101101011010100000000000000000'):
        print("[0: 24, 4: 2, 8: 3, 12: 0, 16: 2, 20: 3, 24: 24, 28: 0, 32: 0, 36: 0, 40: 0, 44: 0, 48: 0, 52: 0, 56: 0, 60: 0, 64: 0, 68: 0, 72: 0, 76: 0, 80: 0, 84: 0, 88: 0, 92: 0, 96: 0, 100: 0, 104: 0, 108: 0, 112: 0, 116: 0, 120: 0, 124: 0, 128: 0, 132: 0, 136: 0, 140: 0, 144: 0, 148: 0, 152: 0, 156: 0, 160: 0, 164: 0, 168: 0, 172: 0, 176: 0, 180: 0, 184: 0, 188: 0, 192: 0, 196: 0, 200: 0, 204: 0, 208: 0, 212: 0, 216: 0, 220: 0, 224: 0, 228: 0, 232: 0, 236: 0, 240: 0, 244: 0, 248: 0, 252: 0, 256: 0, 260: 0, 264: 0, 268: 0, 272: 0, 276: 0, 280: 0, 284: 0, 288: 0, 292: 0, 296: 0, 300: 0, 304: 0, 308: 0, 312: 0, 316: 0, 320: 0, 324: 0, 328: 0, 332: 0, 336: 0, 340: 0, 344: 0, 348: 0, 352: 0, 356: 0, 360: 0, 364: 0, 368: 0, 372: 0, 376: 0, 380: 0, 384: 0, 388: 0, 392: 0, 396: 0, 400: 0],\n [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 16, 0, 24, 0, 24, 24, 2, 24, 28, 1, 24, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0]\n510")
    pass

## Left to implement:
# 1. Jump instructions           ... Done!!
# 2. BEQ instructions (Flushing) ... Done!!
# 3. Queue of stages.            ... Real Fight Starts !!
# 4. Fill the dictionaries


QueueOfStages = []
Lines = []
instruction_mem={}
initial_addr = 4194304

with open('Factorial_machine_code.txt',"r") as file:
    for line in file:
        instr=(line.strip())
        instruction_mem[initial_addr]=instr
        initial_addr=initial_addr+4

FirstInstruction = instruction_mem[PC]
QueueOfStages.append(Stages("F", FirstInstruction, 0, {}, {}))
index = 1
Flush = False
Cycle = 1
beqindex = 0
beqincrement = 0
while(len(QueueOfStages) != 0):
    # print("Cycle Number: ", Cycle)
    i = 1
    tempQ = []
    
    for S in QueueOfStages:
        print(S.Type, '\t', S.instruction)
        
    while(len(QueueOfStages) != 0):
        # print('b')
        if(len(QueueOfStages) != 0 and QueueOfStages[-1].Type == "F" and i % 2 != 0):
            tempQ.insert(0, QueueOfStages.pop().ExecuteStage())
            # Chance of Stalling in beq !!
            i *= 2
            
        if(len(QueueOfStages) != 0 and QueueOfStages[-1].Type == "D" and i % 3 != 0):
            temp = QueueOfStages.pop()
            if(temp.instruction[:6] in beq):
                newStage = temp.ExecuteStage()
                Flush = newStage[0]
                beqincrement = newStage[2]
                tempQ.insert(0, newStage[1])
                beqindex = newStage[1].index
                # PC += beqincrement
            
            elif(temp.instruction[:6] in mips_j_Type):
                newStage = temp.ExecuteStage()
                PC += newStage[0]
                tempQ.insert(0, newStage[1])
            else:
                tempQ.insert(0, temp.ExecuteStage())
            i *= 3
        
        if(len(QueueOfStages) != 0 and QueueOfStages[-1].Type == "E" and i % 5 != 0):
            tempQ.insert(0, QueueOfStages.pop().ExecuteStage())
            i*= 5
            
        if(len(QueueOfStages) != 0 and (QueueOfStages[-1].Type == "M" and i % 7 != 0)):
            tempQ.insert(0, QueueOfStages.pop().ExecuteStage())
            i*=7
            
        if(len(QueueOfStages) != 0 and QueueOfStages[-1].Type == "W" and i % 11 != 0):
            QueueOfStages.pop().ExecuteStage()
            i*=11
        # print(len(QueueOfStages))
        # print("A")     
        pass
    
    # Flushing:
    

    QueueOfStages = tempQ + QueueOfStages
    Cycle += 1
    PC += 4
    if(((PC-4194304)/4)<len(instruction_mem)):
        print("new PC: ", PC)
        if(len(instruction_mem[PC]) != 0):
            QueueOfStages.insert(0, Stages("F", instruction_mem[PC], index, {}, {}))
        index += 1
        
    if(Flush):
        for S in tempQ:
            if(S.index > beqindex):
                tempQ.pop(tempQ.index(S))
        
        print("OLD PC: ", PC)  
        PC += beqincrement # New Address !!
        print("New PC:", PC)
        Flush = False
        
    print("PC at end of Cycle: ", PC)

























































































# RStageRead(instruction_mem[initial_addr + 8])