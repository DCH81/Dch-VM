import base64

class OP:
    HALT        = bytes([0x0])
    JMP         = bytes([0x1])
    CONST       = bytes([0x2])
    ADD         = bytes([0x3])
    SUB         = bytes([0x4])
    XOR         = bytes([0x5])
    LOAD        = bytes([0x6])
    STORE       = bytes([0x7])
    DATA        = bytes([0x8])
    IF          = bytes([0x10])
    FUNC        = bytes([0x11])
    END_FUNC    = bytes([0x12])
    END_COND    = bytes([0x13])
    RETURN      = bytes([0x14])
    CMP_G       = bytes([0x15])
    ARG         = bytes([0x16])  
    CMP_E       = bytes([0x17]) 
    MUL         = bytes([0x18])
    DIV         = bytes([0x18])
    
    DUMP_STACK  = bytes([0x51])
    DUMP_MEMORY = bytes([0x33])

class VirtualMachine:
    def __init__(self, program, verbose: bool = False):
        self.memory = []
        self.stack = []
        self.pc = 0
        self.verbose = verbose
        self.program = self.parse_program(program)
        
        self.funcs = {}
        self.olds_pc = []
        self.actual_funcs = []
        self.old_stacks = {}
        
        self.where_togo = None
        
        self.load()
        

    def get_old_pcs(self):
        pos = len(self.olds_pc) - 1
        old = self.olds_pc[pos]
        self.olds_pc.pop(pos)
        
        return old
    
    def load(self):
        while self.pc < len(self.program):
            opcode = self.get_b()
            if opcode == OP.FUNC:
                func_name = self.get_b()
                self.actual_funcs.append(func_name)
                self.old_stacks[self.get_f()] = self.stack
                self.stack.clear()
                self.funcs[func_name] = {}
                self.funcs[func_name]["pc"] = self.pc
                te = self.pc
                while te < len(self.program):
                    opcode = self.program[te]
                    te += 1
                    if opcode == OP.END_FUNC and self.program[te] == self.get_f():
                        te += 1
            elif opcode == OP.DATA:
                data_len = int(self.get_b())
                mem_add = int.from_bytes(self.get_b(), byteorder='big')
                for _ in range(data_len):
                    va = self.get_b()
                    try:
                        loaded_val = int(va)
                    except:
                        loaded_val = ord(va.decode())
                    self.store_memory(mem_add, loaded_val)
                    mem_add += 1
            elif opcode == OP.ARG:
                try:
                    self.funcs[self.get_f()]["args"] += 1
                except:
                    self.funcs[self.get_f()]["args"] = 1
        self.pc = 0
                
    def get_f(self):
        return self.actual_funcs[len(self.actual_funcs) - 1] 
    
    def get_b(self):
        res = self.program[self.pc]
        self.pc += 1 
        return res
    
    def get_s(self):
        l = len(self.stack) - 1
        val = self.stack[l]
        self.stack.pop(l)
        return val
    
    def add_s(self, val):
        try:
            try:
                val = int(val)
            except:
                val = int.from_bytes(val, byteorder='big')
        except:
            pass
        self.stack.append(int(val))
    
    def store_memory(self, pos, value):
        mem_len = len(self.memory) - 1
        pos = int(pos)
        if pos >= mem_len:
            toadd = pos - mem_len
            self.memory = self.memory + [0] * toadd
        self.memory[int(pos)] = int(value)
    
    def run(self):
        while self.pc < len(self.program):
            opcode = self.get_b()
            if self.verbose:
                print(f"[DEBUG] OP CODE : {opcode}")
            match opcode:
                case OP.HALT:
                    break
                case OP.RETURN:
                    d = self.get_s()
                    if len(self.olds_pc) != 0:
                        self.pc = int(self.get_old_pcs())
                        self.stack = self.old_stacks[self.get_f()]
                    self.actual_funcs.pop(len(self.actual_funcs) - 1)
                    self.add_s(d)
                case OP.FUNC:
                    func_name = self.get_b()
                    self.actual_funcs.append(func_name)
                    self.old_stacks[self.get_f()] = self.stack
                    self.stack.clear()
                    self.funcs[func_name] = {}
                    self.funcs[func_name]["op"] = self.pc
                    te = self.pc
                    while te < len(self.program):
                        opcode = self.program[te]
                        te += 1
                        if opcode == OP.END_FUNC and self.program[te] == self.get_f():
                            te += 1 
                            self.pc = int(te)
                case OP.END_FUNC:
                    self.get_b()
                    if len(self.olds_pc) != 0:
                        self.pc = int(self.get_old_pcs())
                        self.stack = self.old_stacks[self.get_f()]
                    self.actual_funcs.pop(len(self.actual_funcs) - 1)
                    break
                case OP.END_COND:
                    self.get_b()               
                case OP.JMP:
                    b = self.get_b()
                    try:
                        self.pc = int(b)
                    except:
                        self.pc = int.from_bytes(b, byteorder='big')
                case OP.CONST:
                    value = self.get_b()
                    self.add_s(value)
                case OP.ADD:
                    val1 = self.get_s()
                    val2 = self.get_s()
                    self.add_s(val2 + val1) 
                case OP.CMP_G:
                    val1 = self.get_s()
                    val2 = self.get_s()
                    self.add_s(int(val2 > val1)) 
                case OP.CMP_E:
                    val1 = self.get_s()
                    val2 = self.get_s()
                    self.add_s(int(val2 == val1)) 
                case OP.SUB:
                    val1 = self.get_s()
                    val2 = self.get_s()
                    self.add_s(val2 - val1) 
                case OP.MUL:
                    val1 = self.get_s()
                    val2 = self.get_s()
                    self.add_s(val2 * val1) 
                case OP.XOR:
                    val1 = self.get_s()
                    val2 = self.get_s()
                    self.add_s(val2 ^ val1) 
                case OP.LOAD:
                    mem_add = self.get_s() 
                    self.add_s(self.memory[int(mem_add)])
                case OP.STORE:
                    mem_add = self.get_s() 
                    value = self.get_s()
                    self.store_memory(mem_add, value)
                case OP.IF:
                    condition = int(self.get_s())
                    condition_name = self.get_b()
                    te = self.pc
                    end_pos = None
                    while te < len(self.program):
                        opcode = self.program[te]
                        te += 1
                        if opcode == OP.END_COND and self.program[te] == condition_name:
                            te += 1 
                            end_pos = te
                    if not condition:
                        self.pc = int(end_pos)
                case OP.DUMP_STACK:
                    self.dump_stack()          
                case OP.DUMP_MEMORY:
                    self.dump_memory()
                case OP.ARG:
                    pass
                case OP.DATA:
                    pass
                case _:
                    print("Unknown opcode:", opcode, f" INDEX : {self.pc}")
                    break
    
    def dump_stack(self):
        print(f"[STACK DUMP] : {self.stack}")
        return self.stack
    
    def dump_memory(self):
        print(f"[MEMORY DUMP] : {self.memory}")
        return self.memory
    
    def parse_program(self, program: str): 
        dec = base64.b64decode(program).decode()
        inverse = []
        for item in dec:
            if isinstance(item, str):
                for char in item:
                    inverse.append(bytes([ord(char)]))
            else:
                inverse.append(item)
        return inverse
    
    def run_function(self, function_name: str, *args):
        if function_name not in list(self.funcs.keys()):
            print(f"WARNING !! {function_name} DOES NOT EXIST !! WARNING")
            return
        self.pc = self.funcs[function_name]["pc"]
        self.actual_funcs.append(function_name)
        if "args" in self.funcs[function_name]:
            if self.funcs[function_name]["args"] != len(args):
                print(f"WARNING !! {function_name} EXPECTS {len(self.funcs[function_name]['args'])} ARGS, BUT RECEIVED {len(args)} !! WARNING")
                return
            self.stack = list(args)
        self.run()
        self.stack.clear()
        self.olds_pc.clear()
        self.old_stacks.clear()
