#!/bin/sh

### 提供原始文本 147:258行 

if(($#<1));then
    echo "usage: $0 file_pos "
    exit 0
fi

### 输入 词性标注矫正后的文本  带序号
f_pos=$1

### 原始文本 num+line 集合 
f_ori=vi_seikatsu.all.line1
### 输出格式化后的结果 
f_out=${f_pos}.format
### 输出包含错误的pos
f_err=${f_pos}.error
rm -rf ${f_err} 

if [ ! -f ${f_pos} ];then
    echo "ERROR:not found file ${f_pos}!"  
    echo "ERROR:not found file ${f_pos}!" > ${f_err} 
    exit 0
fi

### 转换格式 
python format_vivn.py ${f_ori} ${f_pos} ${f_out} > ${f_err}




