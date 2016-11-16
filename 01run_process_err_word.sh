#!/bin/sh

if(($#<1));then
    echo "usage: $0 file_in"
    echo "处理客户提供的原始数据 替换掉错误字符"
    echo "同时生成 line1 第一行"
    exit 0
fi

file_in=$1
file_in_bak=${file_in}.bak
file_map=map-vivn-charset-err-ok.txt

rm -rf ${file_in_bak} && cp ${file_in}  ${file_in_bak}

cat  ${file_map} | while read line
do
    err=${line%#*}
    ok=${line#*#}
    echo ${err}
    echo ${ok}
    sed -i "s/$err/$ok/g" ${file_in} 
done


### 提取序号+line
### 后面用到的 line1
awk '{if(NR%3==1){print $0}}' ${file_in} > ${file_in}.line1
#awk '{if(NR%3==2){print $0}}' ${file_in} > ${file_in}.line2 



#### 提取出错误字符
#grep -n " ̀" all.line2.seg  > all.line2.seg.grep.err 


