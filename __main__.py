#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import brainx
import os.path

parser = ArgumentParser(description = "Help to BrainFuck, BranLoller and BrainCopter interpretr", epilog = "epilog")
parser.add_argument('--version', action = 'version', version='1.0')
parser.add_argument('file', help = "Path to .png file or Brainfuck code which will be executed")
parser.add_argument('-l', action = 'store_true', help = "BrainLoller program")
parser.add_argument('-c', action = 'store_true', help = "BrainCopter program")
args = parser.parse_args()

if(args.c):
    brainx.BrainCopter(args.file)

elif(args.l):
    brainx.BrainLoller(args.file)

else:
    if not os.path.isfile(args.file):
        brainx.BrainFuck(args.file)
    else:
        with open( args.file, encoding = 'ascii' ) as stream:
            brainx.BrainFuck(stream.read())
