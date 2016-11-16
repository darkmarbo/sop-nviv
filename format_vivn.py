# -*- coding: utf-8 -*-

import sys;
import os;
import re;
import traceback


if(len(sys.argv))<4:
    print("usage %s file_line1 file_pos file_out"%(sys.argv[0]));
    print("usage: %s 带序号的全部句子line1  词性标记后带序号的句子\
                输出格式结果"%(sys.argv[0]));
    sys.exit(0);

f_line1=sys.argv[1]
f_line2=sys.argv[2]
f_out=sys.argv[3]

### 记录 序号+line
map_num={};

fp_line1 = open(f_line1, 'r')
fp_line2 = open(f_line2, 'r')
fp_out = open(f_out, 'w')


#### 读取 map 
for line in fp_line1:
    line = line[:-1]
    list_line = line.split('\t');
    if len(list_line)<2:
        print "ERROR:read line format error!"
        continue;
    num     = list_line[0].strip();
    content = list_line[1].strip();
    if map_num.has_key(num):
        print("ERROR:map read redup line!")
        continue;
    else:
        map_num[num] = content;

#print("map_num len=%d"%(len(map_num.keys())));

ii=0
for line in fp_line2:

    ii += 1;

    line = line[:-1]
    list_line = line.split('\t');
    if len(list_line)<2:
        print "ERROR:read line format error!"
        continue;

    num     = list_line[0].strip();
    content = list_line[1].strip();

    ### 通过num 在map中查找到原始句子 
    line_ori=""
    if map_num.has_key(num):
        line_ori = map_num[num];
    else:
        print("ERROR:not found %s in map_num!"%(num));

    ### 输出 句子编号+原始句子 
    fp_out.write("%s\t%s\n"%(num, line_ori));

    #### 每一个word/pos
    list_cont = content.split(' ')
        
    for word in list_cont:
        list_pos = word.split('/');
        if len(list_pos)<2:
            print("ERROR:num=%d\tline=%s\n"%(ii, word));
            continue;

        www=list_pos[0]
        www = www.replace('_', ' ');
        pos=list_pos[1]
        fp_out.write("%s\t%s\n"%(www, pos))

fp_line1.close();
fp_line2.close();
fp_out.close();

    
