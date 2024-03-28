from machine.machine import VirtualMachine
import base64
class Client:
    def __init__(self, data: str) -> None:
        self.vm = VirtualMachine(program="EWMWFgIwAjAHAjQHAjUHAjAGAjQGFxBtABNtAjUGBgIqBQIhBAIyGAIhAwI1BgcCNQYCMQMCNQcCMAYCMQMCMAcBDxJj", verbose=False)
        mem_pos, string_len = self.create_string_memory(string=data)
        self.vm.run_function(b"c", mem_pos, string_len)     
        decoded_data = self.read_memory(mem_pos, string_len)
        self.res = ''.join(chr(x) for x in decoded_data)
        
    def create_string_memory(self, string: str):
        str_len = len(string)
        string_unit8 = [ord(i) for i in string]
        initial_mem_pos = len(self.vm.memory) + 26
        mem_pos = initial_mem_pos
        for char_code in string_unit8:
            self.vm.store_memory(mem_pos, char_code)
            mem_pos += 1
        return initial_mem_pos, str_len
    
    def read_memory(self, ptr, length):
        string_unit8 = []
        mem = ptr
        for _ in range(length):
            string_unit8.append(self.vm.memory[mem])
            mem += 1
        return string_unit8
    
    def get_result(self):
        return base64.b64encode(self.res.encode()).decode()

if __name__ == '__main__':
    value = Client(data='soloversus').get_result()
    print(f"[DEBUG] OUTPUT RESULT : {value}")