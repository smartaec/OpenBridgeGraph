import csv
import datetime
from nbiHeaderMapper import *
from nbi_prop_converter import *
import sys
import os

append_rows=False
if len(sys.argv)<=1:
    print('please input NOAA climate file path.')
    exit()
else:
    file_path=sys.argv[1]

if len(sys.argv)>2:
    append_rows=sys.argv[2].lower()=='true'


root='./output/'
if not os.path.exists(root):
    os.makedirs(root)

def gen_prop(row,prop_name,format=True):
    val=row[prop_name]
    if len(val)>2 and val[0]=='\'' and val[-1]=='\'':
        val=val[1:-1]
    
    #replace \' in val with white space
    idx=val.find('\'')
    if idx!=-1:
        val=val[:idx]+' '+val[idx+1:]
    
    if len(val)==0:
        return ''
    
    if prop_name in prop_converters:
        converter=prop_converters[prop_name]
        res=converter(val)
        if isinstance(res,(int,float)):
            return str(res)
        elif isinstance(res,datetime.datetime):
            return '\''+res.strftime('%Y-%m-%d')+'\'' if format else res.strftime('%Y-%m-%d')
        elif isinstance(res,str):
            return '\''+res+'\'' if format else res
        else:
            return '\''+str(res)+'\'' if format else str(res)
    
    return '\''+val+'\'' if format else val

def gen_prop_post_script(label,prop_name,prop_type,is_node=True):
    leading_part='MATCH (n:'+label+')' if is_node else 'MATCH p=()-[n:'+label+']-()'
    if prop_type=='string':return '\n'
    if prop_type=='datetime':
        return leading_part+' WHERE EXISTS(n.'+prop_name+') WITH n,[x IN split(toString(n.'+prop_name+'),"-") | toInteger(x)] AS parts SET n.'+prop_name+'=datetime({day: parts[2], month: parts[1], year: parts[0]})\n'
    if prop_type=='int':
        conv_func='toInt'
        return leading_part+' WHERE EXISTS(n.'+prop_name+') SET n.'+prop_name+'='+conv_func+'(n.'+prop_name+')\n'
    elif prop_type=='float':
        conv_func='toFloat'
        return leading_part+' WHERE EXISTS(n.'+prop_name+') SET n.'+prop_name+'='+conv_func+'(n.'+prop_name+')\n'
    else:
        return '\n'

def gen_node_item(row,node_def,writer):
    if node_def.constraint:
        for k,v in node_def.constraint.items():
            if callable(v):
                if not v(row[k]):
                    return
            elif row[k]!=v:
                return
    
    item=[]
    id=''
    for prop in node_def.id_props:
        id+=gen_prop(row,prop,False)+'_'
    item.append(id[:-1])
    
    
    for k,v in sorted(node_def.props.items()):
        p=gen_prop(row,v,False)
        item.append(p)
    
    #TODO: take all default_props as string now, update it later
    if node_def.default_props:
        for k,v in sorted(node_def.default_props.items()):
            item.append(v)
    
    if len(id.rstrip('_'))==0:return #skip row with bad id
    writer.writerow(item)

def gen_edge_item(row,edge_def,writer):
    if edge_def.constraint:
        for k,v in edge_def.constraint.items():
            if callable(v):
                if not v(row[k]):
                    return
            elif row[k]!=v:
                return
    
    item=[]
    src_id=''
    for prop in edge_def.src_id_props:
        src_id+=gen_prop(row,prop,False)+'_'
    item.append(src_id[:-1])
    
    dst_id=''
    for prop in edge_def.dst_id_props:
        dst_id+=gen_prop(row,prop,False)+'_'
    item.append(dst_id[:-1])
    
    rel_str=edge_def.label
    if edge_def.props:
        for k,v in sorted(edge_def.props.items()):
            p=gen_prop(row,v,False)
            item.append(p)
    
    if len(src_id.rstrip('_'))==0 or len(dst_id.rstrip('_'))==0:return #skip row with bad id
    writer.writerow(item)
    
def gen_inventory_item(row,writters):
    for mapper in station_node_mappers:
        gen_node_item(row,mapper,writers[mapper.label])

    for mapper in station_edge_mappers:
        gen_edge_item(row,mapper,writers[mapper.rel_id])

def prepare(append_rows):
    script_file=open(root+'load_climate_data.script','w')
    post_file=open(root+'post_climate_data.script','w')
    
    writers={}
    file_mode='a+' if append_rows else 'w'
    #for node definitions
    for mapper in station_node_mappers:
        f=open(root+'climate_'+mapper.label+'.csv',file_mode,newline='')
        writer=csv.writer(f)
        header=['id']
        for k,v in sorted(mapper.props.items()):
            header.append(k)
            if not mapper.prop_types==None:post_file.write(gen_prop_post_script(mapper.label,k,mapper.prop_types[k]))
        
        if mapper.default_props:
            for k,v in sorted(mapper.default_props.items()):
                header.append(k)
        
        if not append_rows:writer.writerow(header)
        writers[mapper.label]=writer
        
        script_file.write('CREATE INDEX ON :'+mapper.label+'(id)\r\n')
        script_file.write('using periodic commit 500 LOAD CSV WITH HEADERS FROM "file:///climate_'+mapper.label+'.csv" AS row merge (n:'+mapper.label+'{id:row.id}) on match set n+=row on create set n=row;\r\n')
        
    #for edge definitions
    for mapper in station_edge_mappers:
        f=open(root+'climate_'+mapper.rel_id+'.csv',file_mode,newline='')
        writer=csv.writer(f)
        header=['src_id','dst_id']
        
        prop_map='{'
        if mapper.props:
            for k,v in sorted(mapper.props.items()):
                header.append(k)
                prop_map+=k+':row.'+k+','
                if not mapper.prop_types==None:post_file.write(gen_prop_post_script(mapper.label,k,mapper.prop_types[k],is_node=False))
        
        prop_map=prop_map.rstrip(',')+'}'
        
        if not append_rows:writer.writerow(header)
        writers[mapper.rel_id]=writer
        
        if len(prop_map)>2:
            script_file.write('using periodic commit 500 LOAD CSV WITH HEADERS FROM "file:///climate_'+mapper.rel_id+'.csv" AS row match (s:'+mapper.src_label+'{id:row.src_id}),(d:'+mapper.dst_label+'{id:row.dst_id}) merge (s)-[r:'+mapper.label+']->(d) on match set r+='+prop_map+' on create set r='+prop_map+';\r\n')
        else:
            script_file.write('using periodic commit 500 LOAD CSV WITH HEADERS FROM "file:///climate_'+mapper.rel_id+'.csv" AS row match (s:'+mapper.src_label+'{id:row.src_id}),(d:'+mapper.dst_label+'{id:row.dst_id}) merge (s)-[r:'+mapper.label+']->(d);\r\n')
    
    post_file.write('match (n:Station) set n.loc_point=point({longitude:n.longitude,latitude:n.latitude})')
    return writers

with open(file_path) as csv_file:
    writers=prepare(append_rows)
    
    csv_reader=csv.DictReader(csv_file,delimiter=',')
    line_count=0
    header=None
    for row in csv_reader:
        if line_count==0:
            header=row
        else:
            gen_inventory_item(row,writers)
        
        line_count+=1
        if (line_count%100)==0: print(str(line_count)+' rows processed...')
        
    print('file {'+file_path+'} converted.')
    print('copy all csv files in '+root+' folder to import folder in neo4j installation path, and exec scripts in load_nbi_data.script file one by one')
            