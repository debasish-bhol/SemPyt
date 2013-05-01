#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import image_png
import os.path

class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory = b'\x00', memory_pointer = 0):
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
                self.memory[self.memory_pointer] = (self.memory[self.memory_pointer] + 1) % 256

            elif(self.data[data_pointer] == '-'):
                self.memory[self.memory_pointer] = (self.memory[self.memory_pointer] - 1) % 256

            elif(self.data[data_pointer] == '>'):
                self.memory_pointer += 1
                if(self.memory_pointer >= len(self.memory)):
                    self.memory.append(0)

            elif(self.data[data_pointer] == '<'):
                if(self.memory_pointer > 0):
                    self.memory_pointer -= 1

            elif(self.data[data_pointer] == ']'):
                if(self.memory[self.memory_pointer] != 0):
                    data_pointer = stack[len(stack) - 1]
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
                    count = 1

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

    #nextPixel vždy vrátí další pixel k rozkódování
    def nextPixel(self):
        self.pointer += self.direction
        if(len(self.rgb) > self.line):
            if((len(self.rgb[self.line]) > self.pointer) and (self.pointer > -1)):
                return self.rgb[self.line][self.pointer]
            else:
                return False
        else:
            return False

    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""

        if not os.path.isfile(filename):
            print("File or path does not exist!")
            return

        image = image_png.PngReader(filename)

        self.rgb = image.rgb
        self.pointer = -1
        self.line = 0
        self.direction = 1

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = []

        value = self.nextPixel()

        #smyčka rozkodovávající data
        while(value):
            if value == (255,0,0):
                self.data.append(">")
            elif value == (128,0,0):
                self.data.append("<")
            elif value == (0,255,0):
                self.data.append("+")
            elif value == (0,128,0):
                self.data.append("-")
            elif value == (0,0,255):
                self.data.append(".")
            elif value == (0,0,128):
                self.data.append(",")
            elif value == (255,255,0):
                self.data.append("[")
            elif value == (128,128,0):
                self.data.append("]")
            elif value == (0,255,255):
                if(self.direction == 1):
                    self.line += 1
                self.direction -= 1
            elif value == (0,128,128):
                if(self.direction == -1):
                    self.line += 1
                self.direction += 1
            value = self.nextPixel()

        self.data = "".join(self.data)

        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)

class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""

    #nextComannd vždy vrátí další příkaz
    def nextComannd(self):
        self.pointer += self.direction
        if(len(self.rgb) > self.line):
            if((len(self.rgb[self.line]) > self.pointer) and (self.pointer > -1)):
                pixel = self.rgb[self.line][self.pointer]
                return ((-2 * pixel[0] + 3 * pixel[1] + pixel[2]) % 11) + 1
            else:
                return False
        else:
            return False

    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        if not os.path.isfile(filename):
            print("File or path does not exist!")
            return

        image = image_png.PngReader(filename)

        self.rgb = image.rgb
        self.pointer = -1
        self.line = 0
        self.direction = 1

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = []

        value = self.nextComannd()

        #smyčka rozkodovávající data
        while(value):
            if value == 1:
                self.data.append(">")
            elif value == 2:
                self.data.append("<")
            elif value == 3:
                self.data.append("+")
            elif value == 4:
                self.data.append("-")
            elif value == 5:
                self.data.append(".")
            elif value == 6:
                self.data.append(",")
            elif value == 7:
                self.data.append("[")
            elif value == 8:
                self.data.append("]")
            elif value == 9:
                if(self.direction == 1):
                    self.line += 1
                self.direction -= 1
            elif value == 10:
                if(self.direction == -1):
                    self.line += 1
                self.direction += 1
            value = self.nextComannd()

        self.data = "".join(self.data)

        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)
