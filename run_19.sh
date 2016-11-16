#!/bin/sh

if(($#<2));then
	echo "usage:$0 num file"
	echo "num=1|2|3|4 分别表示预处理、分词、词性、检查"
	exit 0
fi

num=$1
file_in=${2}

### 判断文件是否上传成功 
if [ ! -f ${file_in} ];then
	echo "szm_LOG:${file_in} 文件未上传成功 "
	exit 0
fi

name_file=`basename ${file_in}`
out_dir=`dirname ${file_in}`

dir_sh=vn.vitk.git/vn.vitk_run

#sleep 100000
cd /home/yanfa/shaozhiming/tools/vivn_postag

	echo "in:num=${num}   file=${file_in}" > 1.log
	echo "in:num=${num}   file=${file_in}" 
	echo "file_name=${name_file}  out_dir=${out_dir}" >> 1.log
	echo "file_name=${name_file}  out_dir=${out_dir}"
	
	cp -r ${file_in} ./
	if((${num}==1));then
		echo "开始进行 错误字符处理 ......"
	elif((${num}==2));then
		echo "开始进行 越南语分词 ......"
	elif((${num}==3));then
		echo "开始进行 越南语词性标注 ......"

		mv ${name_file} ${dir_sh} 
		cd ${dir_sh} && ./03run_postag.sh ${name_file}  && cd -

		mv ${dir_sh}/${name_file}  ./
		mv ${dir_sh}/${name_file}.pos ${out_dir}
	elif((${num}==4));then
		echo "开始进行 格式转换和检查 ......"

		mv ${name_file} ${dir_sh} 
		cd ${dir_sh} && ./04run_format.sh ${name_file}  && cd -

		mv ${dir_sh}/${name_file}  ./
		mv ${dir_sh}/${name_file}* ${out_dir}
	fi
	

	##cp 1.log ${out_dir} 




cd -

