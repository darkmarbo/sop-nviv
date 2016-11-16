#coding=utf-8
#! python

import sys;
import os;
import re;
import traceback


dictMap = {}

charsetMap = {}

def loadCharset(dictPath):
    lineNum = 0
    
    for line in open(dictPath):
        try:
            new_line = line[:-1].decode('utf-8').strip()

            if not new_line:
                continue

            contents = new_line.split("\t")
            key = contents[0]

            charsetMap[key] = ""
        except Exception as e:
            print(e);
    print charsetMap
        

def handleDir(inputDir):
    if not os.path.exists(inputDir):
        print ('error')+"\t"+inputDir
        return

    files = os.listdir(inputDir)
    for f1 in files:
        if os.path.isdir(inputDir+"/"+f1):
            handleDir(inputDir+"/"+f1)
            continue

        if f1.endswith(".del") or f1.endswith(".ok"):
            continue
            
        handleFile(inputDir+'/'+f1);

        print "Complete file \t"+inputDir+"/"+f1+" ~"
        
    print "Complete dir \t"+inputDir+" !"

        
def handleFile(filePath):
    fr = open(filePath,'r+');

    fpw_OK = open(filePath+".ok", 'w')
    fpw_Del = open(filePath+".del", 'w')
    
    for line in fr.readlines():
        new_line = "";
        try:
            new_line = line[:-1].decode('utf-8').strip()
        except Exception as e:
            new_line="";
            print(e);

        if not new_line:
            last_ch=""
            continue

        last_ch = ""
        out_str = ""
        isMatch = False
        for ch in new_line:
            if (ch not in charsetMap) and (ch not in ' ?.!:;,-;()[]{}1234567890wjzFf"\''):
                out_str=last_ch+ch
                fpw_Del.write(out_str.encode('utf-8').strip()+"\n")
            if ch in charsetMap:
                isMatch = True
            else:
                isMatch = False
                
            last_ch=ch


    fpw_OK.close()
    fpw_Del.close()
    
    fr.close()


if __name__=='__main__':
    if len(sys.argv)!=3:
        print ('%s inputDir dictPath', sys.argv[0])
    else:
        loadCharset(sys.argv[2])
        handleDir(sys.argv[1])
        
        
