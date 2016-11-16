#!/bin/sh

if(($#<1));then
    echo "usage: $0 file_in "
    echo "usage: $0 输入为准备分词的文本(带序号) ***.line1"
    exit 0
fi

file_in=$1
if [ ! -f ${file_in} ];then
    echo "ERROR:${file_in} not is file!"
    exit 0
fi

### ./bin/spark-submit ~/vitk/target/vn.vitk-3.0.jar -i <input-file> -o <output-file>

dir_vnvi_jar=/home/szm/lang_8/vi-vn/pos-tag/vn.vitk.git/vn.vitk/target/vn.vitk-3.0.jar
dir_spark=/home/szm/lang_8/vi-vn/pos-tag/vn.vitk.git/spark-1.6.2-bin-hadoop2.6/bin


### 分词时 需要把dat/tok tag exp 拷贝到制定目录 
dir_dat_ws=/export/dat/tok

##### 提取序号+line
##awk '{if(NR%3==1){print $0}}' $1 > $2
##awk '{if(NR%3==2){print $0}}' $1 > $2 
 
### 删除掉 序号 num
awk -F"\t" '{print $1}' ${file_in} > ${file_in}.awk1
awk -F"\t" '{print $2}' ${file_in} > ${file_in}.awk2

### 分词 
${dir_spark}/spark-submit  --executor-memory 20G  --driver-memory 20G  --total-executor-cores 1  --executor-cores 1   ${dir_vnvi_jar} -i ${file_in}.awk2 -o ${file_in}_wordseg

### 分词结果 
cat ${file_in}_wordseg/part-00* >  ${file_in}.seg-tmp

### 添加序号到分词文件中 
python merge_num+line.py ${file_in}.awk1  ${file_in}.seg-tmp  ${file_in}.seg
rm -rf ${file_in}_wordseg ${file_in}.awk*  ${file_in}.seg-tmp  

### 词性标注

#${dir_spark}/spark-submit --executor-memory 20G  --driver-memory 20G  --total-executor-cores 1  --executor-cores 1 ${dir_vnvi_jar} -t tag -a tag -i ${1} -o ${1}.postagger




