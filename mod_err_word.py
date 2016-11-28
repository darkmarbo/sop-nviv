# -*- coding: utf-8 -*-

import sys;
import os;
import re;
import traceback

'''
    Seikatsu01\A-I_\000040\__000024  Chính sách bảo hiểm y tế từ các công ty bảo hiểm y tế không xử lý việc điều trị y tế thôn thường.
    Seikatsu01\A-I_\000040\__000024 Chính_sách/N bảo_hiểm/N y_tế/N từ/E các/L công_ty/N bảo_hiểm_/N y_tế/N không/R xử_lí/V việc/N điều_trị/V y_tế/N thông_thường/A ./S1

'''

if(len(sys.argv))<4:
    print("usage %s file_line1 file_pos file_pos_out"%(sys.argv[0]));
    print("usage: %s 带序号的全部句子line1  词性标记后带序号的句子\
                输出新的pos文件"%(sys.argv[0]));
    sys.exit(0);

f_line1=sys.argv[1]
f_line2=sys.argv[2]
f_out=sys.argv[3]

### 记录 序号+line
map_num={};
### 记录 词性集
map_pos={};

fp_line1 = open(f_line1, 'r')
fp_line2 = open(f_line2, 'r')
fp_out = open(f_out, 'w')
fp_map_pos = open("map-vivn-pos-tagger-set.txt", 'r')

#### 读取 词性标注集合的 map 
for line in fp_map_pos:
    line = line[:-1]
    list_line = line.split('\t');
    if len(list_line)<2:
        print "ERROR:read line format error!"
        continue;
    pos     = list_line[0].strip();
    content = list_line[1].strip();
    if map_pos.has_key(pos):
        print("ERROR:map read redup line!")
        continue;
    else:
        map_pos[pos] = content;

#print("map_pos len=%d"%(len(map_pos.keys())));

#### 读取 原始序号和句子的 map 
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


#### 处理pos文件 修改错误的word为原始正确的结果 
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
        continue
    #### 原始句子 标点切分开 
    line_ori_punc = line_ori;
    line_ori_punc = line_ori_punc.replace("."," .");
    line_ori_punc = line_ori_punc.replace(","," ,");
    line_ori_punc = line_ori_punc.replace("?"," ?");
    line_ori_punc = line_ori_punc.replace("!"," !");
    line_ori_punc = line_ori_punc.replace(";"," ;");
    line_ori_punc = line_ori_punc.replace(" \""," \" ");
    line_ori_punc = line_ori_punc.replace("\" "," \" ");
    line_ori_punc = line_ori_punc.replace(" ("," ( ");
    line_ori_punc = line_ori_punc.replace(") "," ) ");
    line_ori_punc = line_ori_punc.replace(" ["," [ ");
    line_ori_punc = line_ori_punc.replace("] "," ] ");

    ### 输出 句子编号+原始句子 
    #fp_out.write("%s\t%s\n"%(num, line_ori));

    #### 每一个word/pos
    list_cont = content.split(' ')
        
    for word in list_cont:

        list_pos = word.split('/');

        #### 得到词和词性 
        www = list_pos[0]
        www = www.replace('_', ' ');

        pos = ""
        if len(list_pos)<2:
            print("ERROR:num=%d\tline=%s\n"%(ii, word));
        else:
            pos = list_pos[1]

        #### 词性错误 
        if not map_pos.has_key(pos):
            print("ERROR:pos-tagger error!num=%d\tword=%s\tpos=%s\n"%(ii, www, pos));

        #### 词错误  去原始文本中查找分词后的词  
        www_find = line_ori.find(www);
        if www_find<0:
            print("ERROR:word_segment error!num=%d\tline_ori=%s\terr_word=%s\t\n"%\
                        (ii, line_ori, www));

        fp_out.write("%s\t%s\n"%(www, pos))

fp_line1.close();
fp_line2.close();
fp_out.close();
fp_map_pos.close();

    





