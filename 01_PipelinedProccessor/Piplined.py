

# How this works:

# 1. Build Object Called 'Stage'. This has a constructor, a method called Execute Stage.
# 2. Implement Queue and Its functioning.
# 3. General Setup for MIPS Operations.

RegFile = [0] * 32
RegChanged = [-1] * 32
RegForward = [None] * 32
Memory = [0] * 1000

mips_i_Type = {}

PC = 0



class Stages:

    def __init__(self, Type, instruction, n, res):
        self.Type = Type
        self.instruction = instruction
        self.index = n
        self.results = res

    def ExecuteStage(self):
        
        if(self.Type == "F"):
            # We first execute a the Fetch Stage: Which fetches the actual instruction. This stage doesn't have dependamcies
            # Here we just focus on Getting the actual instruction (Which is provided in the constructor).
            print("Fetching Instruction: ", self.instruction)
            
            # Implementation without forwarding:      ###
            # 1. Fetch the dependancies if any.

            if(self.instruction[:6] == "000000"):
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)
                RegChanged[rs] = max(rs, RegChanged[rs])

                if(RegChanged[rt] == -1 or RegChanged[rd] == -1):
                    return self
                
                else:
                    nextStage = Stages("D", self.instruction, self.index, [RegFile[rd], RegFile[rt], rs])
                    return nextStage

            if(self.instruction[:6] in mips_i_Type):
                    rt = int(self.instruction[11:16], 2)
                    #rd = int(self.instruction[16:21], 2)

                    rs = int(self.instruction[6:11], 2)
                    RegChanged[rs] = max(rs, RegChanged[rs])
                    
                    if(RegChanged[rt] == -1):
                        return self
                    
                    else:
                        nextStage = Stages("D", self.instruction, self.index, [])
                        return nextStage
            
            else:
                return Stages("D", self.instruction, self.index, [])
 
        
        elif(self.Type == "D"):
            # We are now working on the decode stage of the Instruction.
            print("Decoding Instruction: ", self.instruction)
            if(self.instruction[:6] == "000000"):
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)
                return Stages("E", self.instruction, self.index, [RegFile[rt], RegFile[rd]])
                
            if(self.instruction[:6] in mips_i_Type):
                rt = int(self.instruction[11:16], 2)
                rs = int(self.instruction[6:11], 2)
                immidiet = int(self.instruction[16:], 2)
                if(RegChanged[rt] == -1):
                    return self
                else:
                    nextStage = Stages("D", self.instruction, self.index, [RegFile[rt], immidiet])
                    return nextStage
            else:
                return Stages("D", self.instruction, self.index, [])


            # return Stages("E", self.instruction, self.index, [])
            # Add the conditions for stalling to execute forwarding.  
        
        elif(self.Type == "E"):
            print("Executing instruction: ", self.instruction)
            # When implementing Forwarding.                          ###
            # Now we have the execute stage:

            if(self.instruction[:6] == "000000"):
                Val_at_rt = self.results[0]
                Val_at_rd = self.results[1]
                res = 0
                funct = self.instruction[26:]
                if(funct == "100000"):
                    res = Val_at_rt + Val_at_rd
                elif(funct == "100010"):
                    res = Val_at_rt - Val_at_rd
                elif(funct == "011000"):
                    res = Val_at_rd * Val_at_rt
                elif(funct == "100100"):
                    res = Val_at_rt & Val_at_rd
                else:
                    print("Wrong Execute Stage Found!!")
                    res = 0
                return Stages("M", self.instruction, self.index, [res])


            if(self.instruction[:6] in mips_i_Type):
                    value_at_rt = self.results[0]
                    immd = self.results[1]
                    res = 0
                    if(mips_i_Type[self.instruction[:6]] == "addu"):
                        res = value_at_rt + immd
                    elif(mips_i_Type[self.instruction[:6]] == "subu"):
                        res = value_at_rt - immd
                    elif(mips_i_Type[self.instruction[:6]] == "multu"):
                        res = value_at_rt * immd

                    return Stages("M", self.instruction, self.index, [res])
                    
            else:
                return Stages("D", self.instruction, self.index, [])
            # return Stages("M", self.instruction, self.index, [])

        elif(self.Type == "M"):
            # Memory Write Back only happens at lw and stor word.
            rs = int(self.instruction[6:11], 2)
            rt = int(self.instruction[11:16], 2)

            print("Memory Stage for: ", self.instruction)

            if(self.instruction[:6] == ""):           ## Fill OpCode for lw
                print("Memory Read from location:", self.results[0])
                RegFile[rs] = Memory[self.results[0]]

            elif(self.instruction[:6] ==''):
                print("Writing to Memory in location", self.results[0])
                Memory[self.results[0]] = RegFile[rs]      ## Check This!!
                
                #pass
            #return Stages("W", self.instruction, self.index, [])
        
        elif(self.Type == "W"):
            print("Register Write Back: ", self.instruction)
            if(True):
                pass
            # return Stages("", self.instruction, self.index, [])






class StagesWithForwarding:

    def __init__(self, Type, instruction, n, res):
        self.Type = Type
        self.instruction = instruction
        self.index = n
        self.results = res

    def ExecuteStage(self):
        
        if(self.Type == "F"):
            # We first execute a the Fetch Stage: Which fetches the actual instruction. This stage doesn't have dependamcies
            # Here we just focus on Getting the actual instruction (Which is provided in the constructor).
            print("Fetching Instruction: ", self.instruction)
            
            # Implementation without forwarding:      ###
            # 1. Fetch the dependancies if any.

            if(self.instruction[:6] == "000000"):
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)
                RegChanged[rs] = max(rs, RegChanged[rs])
                return StagesWithForwarding("D", self.instruction, self.index, [])

            if(self.instruction[:6] in mips_i_Type):
                    rt = int(self.instruction[11:16], 2)
                    rs = int(self.instruction[6:11], 2)
                    RegChanged[rs] = max(rs, RegChanged[rs])
                    return StagesWithForwarding("D", self.instruction, self.index, [])
            else:
                return Stages("D", self.instruction, self.index, [])
 
        
        elif(self.Type == "D"):

            # We are now working on the decode stage of the Instruction.
            print("Decoding Instruction: ", self.instruction)
            if(self.instruction[:6] == "000000"):
                rt = int(self.instruction[11:16], 2)
                rd = int(self.instruction[16:21], 2)
                rs = int(self.instruction[6:11], 2)

                value_at_rt = 0
                Val_at_rd = 0
                
                if(RegChanged[rs] != -1 and RegForward[rs] == ):

                return Stages("E", self.instruction, self.index, [RegFile[rt], RegFile[rd]])
                
            if(self.instruction[:6] in mips_i_Type):
                rt = int(self.instruction[11:16], 2)
                rs = int(self.instruction[6:11], 2)
                immidiet = int(self.instruction[16:], 2)
                if(RegChanged[rt] == -1):
                    return self
                else:
                    nextStage = Stages("D", self.instruction, self.index, [RegFile[rt], immidiet])
                    return nextStage
            else:
                return Stages("D", self.instruction, self.index, [])


            # return Stages("E", self.instruction, self.index, [])
            # Add the conditions for stalling to execute forwarding.  
        
        elif(self.Type == "E"):
            print("Executing instruction: ", self.instruction)
            # When implementing Forwarding.                          ###
            # Now we have the execute stage:

            if(self.instruction[:6] == "000000"):
                Val_at_rt = self.results[0]
                Val_at_rd = self.results[1]
                res = 0
                funct = self.instruction[26:]
                if(funct == "100000"):
                    res = Val_at_rt + Val_at_rd
                elif(funct == "100010"):
                    res = Val_at_rt - Val_at_rd
                elif(funct == "011000"):
                    res = Val_at_rd * Val_at_rt
                elif(funct == "100100"):
                    res = Val_at_rt & Val_at_rd
                else:
                    print("Wrong Execute Stage Found!!")
                    res = 0
                return Stages("M", self.instruction, self.index, [res])


            if(self.instruction[:6] in mips_i_Type):
                    value_at_rt = self.results[0]
                    immd = self.results[1]
                    res = 0
                    if(mips_i_Type[self.instruction[:6]] == "addu"):
                        res = value_at_rt + immd
                    elif(mips_i_Type[self.instruction[:6]] == "subu"):
                        res = value_at_rt - immd
                    elif(mips_i_Type[self.instruction[:6]] == "multu"):
                        res = value_at_rt * immd

                    return Stages("M", self.instruction, self.index, [res])
                    
            else:
                return Stages("D", self.instruction, self.index, [])
            # return Stages("M", self.instruction, self.index, [])

        elif(self.Type == "M"):
            # Memory Write Back only happens at lw and stor word.
            rs = int(self.instruction[6:11], 2)
            rt = int(self.instruction[11:16], 2)

            print("Memory Stage for: ", self.instruction)

            if(self.instruction[:6] == ""):           ## Fill OpCode for lw
                print("Memory Read from location:", self.results[0])
                RegFile[rs] = Memory[self.results[0]]

            elif(self.instruction[:6] ==''):
                print("Writing to Memory in location", self.results[0])
                Memory[self.results[0]] = RegFile[rs]      ## Check This!!
                
                #pass
            #return Stages("W", self.instruction, self.index, [])
        
        elif(self.Type == "W"):
            print("Register Write Back: ", self.instruction)
            if(True):
                pass
            # return Stages("", self.instruction, self.index, [])














Lines = []

with open('a.txt', 'r') as Assembly:
    Lines = Assembly.readline()

QueueOfInstructions = []

# Read and implement Queue Method:

# 1. First Insert the first "F" stage instruction into the Queue. ->[0:]->
QueueOfInstructions.insert(0, Stages("F", Lines[int(PC/4)][0:32], PC/4, []))
PC += 4

# 2. After every execution ensure you pop the command.

while(len(QueueOfInstructions) == 0):

    i = 1
    for S in QueueOfInstructions:
        if S.Type == "F" and i % 2 != 0:
            QueueOfInstructions.insert(0, S.execute())
            i *= 2

        if S.Type == "D" and i % 3 != 0:
            QueueOfInstructions.insert(0, S.execute())
            i *= 3

        if S.Type == "E" and i % 5 != 0:
            QueueOfInstructions.insert(0, S.execute())
            i *= 5

        if S.Type == "M" and i % 7 != 0:
            QueueOfInstructions.insert(0, S.execute())
            i *= 7

        if S.Type == "W" and i % 8 != 0:
            i *= 11

        if i == 2*3*5*7*11:
            break

    if(i % 2 != 0 and PC/4 < len(Lines)):
        QueueOfInstructions.insert(0, Stages("F", Lines[int(PC/4)][0:32], PC/4 ,[]))































