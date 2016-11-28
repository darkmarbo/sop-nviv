
import os
import sys


fp_pos=open(sys.argv[1]);
fp_out=open(sys.argv[2],"w");

for line in fp_pos:
    line = line[:-1]
    vec_line = line.split("\t");

    name = vec_line[0]
    fp_out.write("%s\t"%(name));

    con = vec_line[1];
    vec_con = con.split(' ');
    ii=0;
    for word_pos in vec_con:
        ii += 1;
        vec_wp = word_pos.split("/")
        word=vec_wp[0]
        if ii==1:
            fp_out.write("%s"%(word));
        else:
            fp_out.write(" %s"%(word));

    fp_out.write("\n");


fp_pos.close()
fp_out.close();

