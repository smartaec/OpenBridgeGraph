import csv
import os
from nbi_static_data import *

root='./output/'
if not os.path.exists(root):
    pass

for subdirs,di,files in os.walk(root):
    for file in files:
        if not file.endswith('.csv'):continue
        lines_seen=set()
        header=''
        for line in open(root+file,'r'):
            if len(header)==0:
                header=line
                continue
            if not line in lines_seen:lines_seen.add(line)
        with open(root+file,'w') as writer:
            writer.write(header)
            for line in lines_seen:
                writer.write(line)
        print('processed: '+file)

print('finished...')