#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zlib

class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""
    pass


class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
    pass

class PNGWrongData(Exception):
    """Výjimka oznamující, že nesouhlasí kontrolní součet v datech."""
    pass

class PngReader():
    """Třída pro práci s PNG-obrázky."""
    
    def byteArrayToInt(self,array):
        return (array[0] << 24) + (array[1] << 16) + (array[2] << 8) + array[3]

    def paeth(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        elif pb <= pc:
            return b
        else:
            return c

    def __init__(self, filepath):
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = []
        self.width = 0
        self.heigth = 0

        idats = bytearray()

        #smyčka která načte chunky které nás zajímají
        with open( filepath, mode = "rb") as stream:
            if(stream.read(8) != b"\x89PNG\r\n\x1a\n"):
                raise PNGWrongHeaderError("Not a PNG!")

            while 1:
                length = self.byteArrayToInt(stream.read(4))
                typ = stream.read(4)
                data = stream.read(length)
                crc = self.byteArrayToInt(stream.read(4))

                if(zlib.crc32(typ+data)!=crc):
                    raise PNGWrongData("Data CRC does not match!")

                if(typ == b"IHDR"):
                    self.width = self.byteArrayToInt(data[:4])
                    self.heigth = self.byteArrayToInt(data[4:8])

                    if(data[8:] != b"\x08\x02\x00\x00\x00"):
                       raise PNGNotImplementedError("Not supported png type!")
                    
                if(typ == b"IDAT"):
                    idats += data

                if(typ == b"IEND"):
                    break

                

        idats = zlib.decompress(idats)
       
         #následné zpracování rozbalených dat
        for i in range(self.heigth):
            line = []
            line_counter = i * self.width * 3 + i
            filtr = idats[line_counter]
            for j in range(self.width):
                column_counter = line_counter + j * 3
                R = idats[column_counter + 1]
                G = idats[column_counter + 2]
                B = idats[column_counter + 3]

                #aplikování filtrů
                if(filtr == 0):
                    pass

                elif(filtr == 1):
                    if(j > 0):
                        R = (R + line[j - 1][0]) % 256
                        G = (G + line[j - 1][1]) % 256
                        B = (B + line[j - 1][2]) % 256
                 
                elif(filtr == 2):
                    if(i > 0):
                        R = (R + self.rgb[i - 1][j][0]) % 256
                        G = (G + self.rgb[i - 1][j][1]) % 256
                        B = (B + self.rgb[i - 1][j][2]) % 256
  
                elif(filtr == 3):
                    Ra = Ga = Ba = 0
                    Rb = Gb = Bb = 0
                    if(j > 0):
                        R = (R + line[j - 1][0]) % 256
                        G = (G + line[j - 1][1]) % 256
                        B = (B + line[j - 1][2]) % 256
                    if(i > 0):
                        Rb = self.rgb[i - 1][j][0]
                        Gb = self.rgb[i - 1][j][1]
                        Bb = self.rgb[i - 1][j][2]

                    R = (R + (Ra + Rb) // 2) % 256
                    G = (G + (Ga + Gb) // 2) % 256
                    B = (B + (Ba + Bb) // 2) % 256

                elif(filtr == 4):
                    Ra = Ga = Ba = 0
                    Rb = Gb = Bb = 0
                    Rc = Gc = Bc = 0
                    if(j > 0):
                        Ra = line[j - 1][0]
                        Ga = line[j - 1][1]
                        Ba = line[j - 1][2]
                    if(i > 0):
                        Rb = self.rgb[i - 1][j][0]
                        Gb = self.rgb[i - 1][j][1]
                        Bb = self.rgb[i - 1][j][2]
                    if((i > 0) and (j > 0)):
                        Rc = self.rgb[i - 1][j - 1][0]
                        Gc = self.rgb[i - 1][j - 1][1]
                        Bc = self.rgb[i - 1][j - 1][2]

                    R = (R + self.paeth(Ra, Rb, Rc)) % 256
                    G = (G + self.paeth(Ga, Gb, Gc)) % 256
                    B = (B + self.paeth(Ba, Bb, Bc)) % 256

                else:
                    raise PNGNotImplementedError("Not supported png filtr!")

                line.append((R,G,B))
            self.rgb.append(line)
