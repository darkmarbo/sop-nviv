#coding=utf-8
#! python

import sys;
import os;
import re;
import traceback


if(len(sys.argv))<4:
    print("usage %s file_num file_seg-line file_out"%(sys.argv[0]));
    print("file1是序列号 file2是line 将两者合并 ");
    sys.exit(0);

f_line1=sys.argv[1]
f_line2=sys.argv[2]
f_out=sys.argv[3]

fp_line1 = open(f_line1, 'r')
fp_line2 = open(f_line2, 'r')
fp_out = open(f_out, 'w')

list_line1 = fp_line1.readlines()
list_line2 = fp_line2.readlines()

len_1 = len(list_line1);
len_2 = len(list_line2);
print("LOG:len_1=%d\tlen_2=%d\n"%(len_1,len_2));
if len_1 != len_2:
    print("ERROR:len_file1 != len_file2");
    sys.exit(0);


for ii in range(0,len_1):
    #print("process line_num ii=%d\nline2=%s"%(ii,list_line2[ii]));
    line_1 = list_line1[ii][:-1]
    line_2 = list_line2[ii][:-1]
        
    fp_out.write("%s\t%s\n"%(line_1, line_2))

fp_line1.close();
fp_line2.close();
fp_out.close();

    
