# Dch-VM

Dch-VM is a Python Virtual Machine fast & secure, in this script Dch-VM is used for make a very simple encryption

## This Program

```python

program = [
    #OP.DATA,9,100,102, 108, 97, 103, 61, 110, 105, 103, 97, # 11 bytecodes
        
    OP.FUNC,"c",OP.ARG,OP.ARG,
    
    #COUNTER LOOP
    OP.CONST, 0, 
    OP.CONST, 0,
    OP.STORE,  
    #COUNTER LOOP
    
    # STORE ARGS
    OP.CONST, 4,    # LEN STR
    OP.STORE,       
    OP.CONST, 5,    # MEM PTR
    OP.STORE,  
    # STORE ARGS
    
    
    #CHECK LOOP PART
        #LOAD COUNTER
        OP.CONST, 0,
        OP.LOAD,   
        #LOAD COUNTER   
        
        #LOAD STR LEN
        OP.CONST, 4,
        OP.LOAD,  
        #LOAD STR LEN
        
        OP.CMP_E,
        OP.IF,"m",         
        OP.HALT,     
        OP.END_COND,"m",  
    #CHECK LOOP PART
    
    #LOAD STR PTR
    OP.CONST,5,
    OP.LOAD,
    #LOAD STR PTR
    
    #LOAD STR
    OP.LOAD,
    #LOAD STR

    # ENCRYPTION ALGO
        OP.CONST,42,
        OP.XOR,
        OP.CONST,33,
        OP.SUB,
        OP.CONST,2,
        OP.MUL,   
        OP.CONST,33,
        OP.ADD,
    # ENCRYPTION ALGO
    
    #LOAD STR PTR
    OP.CONST,5,
    OP.LOAD,
    #LOAD STR PTR
    
    #STORE STR
    OP.STORE,
    #STORE STR
    
    #LOAD MEM PTR
    OP.CONST, 5,    
    OP.LOAD,
    #LOAD MEM PTR
    
    #INCREAMENTE MEM PTR
    OP.CONST,1,
    OP.ADD,
    OP.CONST,5,
    OP.STORE,    
    #INCREAMENTE MEM PTR

    #LOAD COUNTER LOOP AND INCREAMENTE
    OP.CONST,0,
    OP.LOAD,
    OP.CONST,1,
    OP.ADD,
    OP.CONST,0,
    OP.STORE,
    #LOAD COUNTER LOOP AND INCREAMENTE    
    OP.JMP,15,         # Jump to the beginning of the loop  
    OP.END_FUNC,"c",
]
```