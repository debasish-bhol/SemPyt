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
    
    def ByteArrayToInt(self,array):
        return (array[0] << 24) + (array[1] << 16) + (array[2] << 8) + array[3]

    def __init__(self, filepath):
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
        self.rgb = []
        width = 0
        heigth = 0

        idats = bytearray()

        #smyčka která načte chunky které nás zajímají
        with open( filepath, mode="rb") as stream:
            if(stream.read(8) != b"\x89PNG\r\n\x1a\n"):
                raise PNGWrongHeaderError("Not a PNG!")

            while 1:
                length = self.ByteArrayToInt(stream.read(4))
                typ = stream.read(4)
                data = stream.read(length)
                crc = self.ByteArrayToInt(stream.read(4))

                if(zlib.crc32(typ+data)!=crc):
                    raise PNGWrongData("Data CRC does not match!")

                if(typ == b"IHDR"):
                    width = self.ByteArrayToInt(data[:4])
                    heigth = self.ByteArrayToInt(data[4:8])

                    if(data[8:] != b"\x08\x02\x00\x00\x00"):
                       raise PNGNotImplementedError("Not supported png type!")
                    
                if(typ == b"IDAT"):
                    idats+=data
                if(typ == b"IEND"):
                    break

        idats = zlib.decompress(idats)
       
         #následné zpracování rozbalených dat
        for i in range(heigth):
            line = []
            line_counter = i*width*3+i
            filtr = idats[line_counter]
            for j in range(width):
                column_counter = line_counter+j*3
                R = idats[column_counter+1]
                G = idats[column_counter+2]
                B = idats[column_counter+3]
                if(filtr==0):
                    line.append((R,G,B))
            self.rgb.append(line)

