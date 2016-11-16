#coding=utf-8
#! python

import sys;
import os;
import re;
import traceback


f_in=sys.argv[1]
fpw_Del = open(f_in+".del", 'w')

charsetMap = {}

for line in open(f_in):
    new_line = line[:-1].decode('utf-8').strip()

    if not new_line:
        continue

    contents = new_line.split("\t")
    key = contents[0]

    if not charsetMap.has_key(key):
        charsetMap[key] = 1
        

for key in charsetMap.keys():
    fpw_Del.write(key.encode('utf-8').strip()+"\n")

fpw_Del.close();
    
