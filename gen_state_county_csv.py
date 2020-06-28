import csv
import os
from nbi_static_data import *

root='./output/'
if not os.path.exists(root):
    os.makedirs(root)

with open(root+'states.csv','w',newline='') as state_csv:
    writer=csv.writer(state_csv)
    header=['id','code','name']
    writer.writerow(header)
    
    for k,v in state_codes.items():
        id=k[:-1]
        state_code=k[:-1]
        name=v
        writer.writerow([id,state_code,name])

with open(root+'counties.csv','w',newline='') as county_csv:
    writer=csv.writer(county_csv)
    header=['id','code','name']
    writer.writerow(header)
    for k,v in county_codes.items():
        state=k[0:2]
        code=k[-3:]
        id=k[0:2]+'_'+k[-3:]
        name=v
        writer.writerow([id,code,name])

with open(root+'county_in_state.csv','w',newline='') as county_in_csv:
    writer=csv.writer(county_in_csv)
    header=['county_id','state_id']
    writer.writerow(header)
    for k,v in county_codes.items():
        state=k[0:2]
        id=k[0:2]+'_'+k[-3:]
        writer.writerow([id,state])

with open(root+'load_state_county.script','w') as file:
    file.write('using periodic commit 500 LOAD CSV WITH HEADERS FROM "file:///states.csv" AS row merge (n:State{id:row.id}) on match set n+=row on create set n=row;\r\n')
    file.write('using periodic commit 500 LOAD CSV WITH HEADERS FROM "file:///counties.csv" AS row merge (n:County{id:row.id}) on match set n+=row on create set n=row;\r\n')
    file.write('using periodic commit 500 LOAD CSV WITH HEADERS FROM "file:///county_in_state.csv" AS row match (c:County{id:row.county_id}),(s:State{id:row.state_id}) merge (c)-[:LocateIn]->(s);\r\n')
print('generated...')