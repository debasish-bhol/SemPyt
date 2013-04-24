#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        
        # data programu
        self.data = data
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        data_pointer = 0
        stack = list()
        
        while 1:        #hlavní loop
            print(self.memory_pointer)
            if(self.data[data_pointer]=='+'):
                self.memory[self.memory_pointer]=(self.memory[self.memory_pointer]+1)%256

            if(self.data[data_pointer]=='-'):
                self.memory[self.memory_pointer]=(self.memory[self.memory_pointer]-1)%256

            if(self.data[data_pointer]=='>'):
                self.memory_pointer+=1
                print(self.memory_pointer>=len(self.memory))
                if(self.memory_pointer>=len(self.memory)):
                    self.memory.append(0)

            if(self.data[data_pointer]=='<'):
                self.memory_pointer-=1

            if(self.data[data_pointer]=='['):
                stack.append(data_pointer)

            if(self.data[data_pointer]==']'):
                if(len(stack)>0):
                    if(self.memory[self.memory_pointer]!=0):
                        data_pointer=stack[len(stack)-1]
                    else:
                         stack.pop()

            data_pointer+=1

            if(len(self.data)<=data_pointer):
                break
                        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ""
    
    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
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

