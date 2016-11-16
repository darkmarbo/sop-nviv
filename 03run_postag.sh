#!/bin/sh

if(($#<1));then
    echo "usage: $0 file_in "
    echo "usage: $0 输入为人工校验后的分词结果文本(带序号) ***.line1.seg"
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

 
### 删除掉 序号 num
awk -F"\t" '{print $1}' ${file_in} > ${file_in}.awk1
awk -F"\t" '{print $2}' ${file_in} > ${file_in}.awk2


### 词性标注
rm -rf ${file_in}_postagger
${dir_spark}/spark-submit --executor-memory 20G  --driver-memory 20G  --total-executor-cores 1  --executor-cores 1 ${dir_vnvi_jar} -t tag -a tag -i ${file_in}.awk2 -o ${file_in}_postagger

#### 词性标注结果 
cat ${file_in}_postagger/part-00* >  ${file_in}.pos-tmp

### 处理 词性标注结果中的 标点和CC
sed 's/\/\./\/S1/g;s/\/?/\/S1/g;s/\/!/\/S1/g;s/\/,/\/S2/g;s/\/;/\/S2/g;s/\/:/\/S2/g;s/\/——/\/S2/g;s/\/"/\/S2/g;s/\/\[/\/S3/g;s/\/\]/\/S3/g;s/\/(/\/S3/g;s/\/)/\/S3/g;s/\/CC/\/C/g' ${file_in}.pos-tmp > ${file_in}.pos-tmp.sed


#### 添加序号到分词文件中 
python merge_num+line.py ${file_in}.awk1  ${file_in}.pos-tmp.sed  ${file_in}.pos

### 删除中间结果 
rm -rf ${file_in}_postagger ${file_in}.awk*  ${file_in}.pos-tm*  




###### 分词 
###${dir_spark}/spark-submit  --executor-memory 20G  --driver-memory 20G  --total-executor-cores 1  --executor-cores 1   ${dir_vnvi_jar} -i ${file_in}.awk2 -o ${file_in}_wordseg

