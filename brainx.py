#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        
        # data programu
        self.data = data
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        self.output = ""
        data_pointer = 0
        input_data_pointer = len(data)
        stack = list()        

        #hledání vstupních dat
        while (input_data_pointer > 0):
            input_data_pointer -= 1
            if(data[input_data_pointer] == '!'):
                input_data_pointer += 1
                break

        #hlavní loop
        while 1:        
            if(self.data[data_pointer] == '+'):
                self.memory[self.memory_pointer]=(self.memory[self.memory_pointer]+1)%256

            elif(self.data[data_pointer] == '-'):
                self.memory[self.memory_pointer]=(self.memory[self.memory_pointer]-1)%256

            elif(self.data[data_pointer] == '>'):
                self.memory_pointer += 1
                if(self.memory_pointer >= len(self.memory)):
                    self.memory.append(0)

            elif(self.data[data_pointer] == '<'):
                if(self.memory_pointer > 0):
                    self.memory_pointer -=1

            elif(self.data[data_pointer] == ']'):
                if(self.memory[self.memory_pointer] != 0):
                    data_pointer = stack[len(stack)-1]
                else:
                    stack.pop()

            elif(self.data[data_pointer] == '.'):
                self.output += chr(self.memory[self.memory_pointer])
                sys.stdout.write(chr(self.memory[self.memory_pointer]))
                sys.stdout.flush()

            elif(self.data[data_pointer] == ','):
                if((input_data_pointer > 0) and (input_data_pointer < len(data))):
                    self.memory[self.memory_pointer] = ord(data[input_data_pointer])
                    input_data_pointer += 1
                else:
                    self.memory[self.memory_pointer]=ord(sys.stdin.read(1))

            elif(self.data[data_pointer] == '['):
                if(self.memory[self.memory_pointer] != 0):
                    stack.append(data_pointer)
                else:
                    count=1

                    while(count > 0):
                        data_pointer += 1
                        if(self.data[data_pointer] == '['):
                            count += 1
                        elif(self.data[data_pointer] == ']'):
                            count -= 1
                        if(len(self.data) <= data_pointer):
                            break

            data_pointer += 1

            if(len(self.data) <= data_pointer):
                break

    def get_memory(self):
        return self.memory


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""
    
    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        



        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)
