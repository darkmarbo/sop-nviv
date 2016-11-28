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

ch_punc=['.','?','!',',',';',':','——','\'','"','[',']','(',')','’','“','”'];

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

#### 处理每一行  
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

    ### 输出 句子编号+原始句子 
    fp_out.write("%s\t%s\n"%(num, line_ori));

    #### 原始句子行  标点符合分开 前后都加空格  然后删除连续两个空格 
    line_ori_find=line_ori;
    for ch in ch_punc:
        line_ori_find = line_ori_find.replace(ch," %s "%(ch));

    line_ori_find = line_ori_find.replace("   "," ");
    line_ori_find = line_ori_find.replace("  "," ");
    line_ori_find = line_ori_find.strip();
    vec_word_ori = line_ori_find.split(" ");

    n_vec_ori = len(vec_word_ori);  ### 原始句子的词数 
    
    #print("%s\n%s"%(line_ori, line_ori_find));


    #### 每一个word/pos
    list_cont = content.split(' ')
        
    jj_st = 0;  ### 从 line_ori_find 的 jj_st 开始查找 
    jj_end = 0;  ###    line_ori_find 的 jj_end 结束  
    len_1 = len(line_ori_find);  ### 原始句子长度 
    len_2 = 0;  ### 分词结果 累计长度和 
    len_diff = 4;   ### 从jj_st到现在相差多少  
    N_list_cont = len(list_cont);
    n_list_cont = 0;  ### 第几个 www 
    for word in list_cont:

        n_list_cont += 1;
        list_pos = word.split('/');

        #### 得到词和词性 
        www = list_pos[0]
        www = www.replace('_', ' ');

        ### 把 www  左右两侧的空格也加上来  全词匹配  
        www = www.strip();
        if n_list_cont != 1:
            www = " %s"%(www)
        if n_list_cont != N_list_cont:
            www = "%s "%(www)

        pos = ""
        if len(list_pos)<2:
            print("ERROR:num=%d\tline=%s\n"%(ii, word));
        else:
            pos = list_pos[1]

        #### 词性错误 
        if not map_pos.has_key(pos):
            print("ERROR:pos-tagger error!num=%d\tword=%s\tpos=%s\n"%(ii, www, pos));

        len_www = len(www);  ### 当前词的长度 
        jj_end = jj_st + len_www + len_diff;
        if jj_end > len_1:
            jj_end = len_1;
            
        #### 查找 www  从jj_st索引  到jj_end(不包含)
        ##### 词错误  去原始文本中查找分词后的词  
        #if ii == 392:
        #    print "%s"%(line_ori)
        #    print "www=%s==="%(www)
        idx = line_ori_find.find(www, jj_st, jj_end); 
        if idx < 0:
            len_diff += len_www + 4;
            print("ERROR:word_segment error!num=%d\tline_ori=%s\terr_word=%s\t\n"%\
                        (ii, line_ori, www));
        else:
            jj_st = idx + len_www -2;
            len_diff = 4;
        


        fp_out.write("%s\t%s\n"%(www, pos))

fp_line1.close();
fp_line2.close();
fp_out.close();
fp_map_pos.close();

    





