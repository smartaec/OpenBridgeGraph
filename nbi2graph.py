import csv
import datetime
from nbiHeaderMapper import *
from neo4j_helper import *
from nbi_prop_converter import *
from set_place_name import *
import sys

force_init=False

if len(sys.argv)<=1:
    print('please input NBI file path.')
    exit()
else:
    file_paths=sys.argv[1:]

#file_path='MI15.txt'
#file_path='ALL15.txt'

# def gen_prop(row,prop_name,format=True):
    # val=row[prop_name]
    # if len(val)>2 and val[0]=='\'' and val[-1]=='\'':
        # return val if format else val[1:-1]
    
    # return '\''+val+'\'' if format else val

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

def gen_node_script(row,node_def):
    if node_def.constraint:
        for k,v in node_def.constraint.items():
            if callable(v):
                if not v(row[k]):
                    return ''
            elif row[k]!=v:
                return ''
    
    id=''
    for prop in node_def.id_props:
        id+=gen_prop(row,prop,False)+'_'
    #s=s[:-1]+'})'
    s='MERGE (p:'+node_def.label+'{id:\''+id[:-1]+'\'})'
    
    prop_map='{'
    for k,v in node_def.props.items():
        p=gen_prop(row,v)
        if isinstance(p,str) and len(p)==0:
            continue
        prop_map+=k+':'+p+','
    
    #TODO: take all default_props as string now, update it later
    if node_def.default_props:
        for k,v in node_def.default_props.items():
            prop_map+=k+':\''+v+'\','
    
    prop_map=prop_map+'id:\''+id[:-1]+'\'}'
    
    return s+' ON MATCH set p+='+prop_map+' ON CREATE set p='+prop_map

def gen_edge_script(row,edge_def):
    if edge_def.constraint:
        for k,v in edge_def.constraint.items():
            if callable(v):
                if not v(row[k]):
                    return ''
            elif row[k]!=v:
                return ''
    
    src_str='(s:'+edge_def.src_label+'{id:\''
    src_id=''
    for prop in edge_def.src_id_props:
        src_id+=gen_prop(row,prop,False)+'_'
    src_str+=src_id[:-1]+'\'})'
    
    dst_str='(d:'+edge_def.dst_label+'{id:\''
    dst_id=''
    for prop in edge_def.dst_id_props:
        dst_id+=gen_prop(row,prop,False)+'_'
    dst_str+=dst_id[:-1]+'\'})'
    
    rel_str=edge_def.label
    prop_map='{'
    if edge_def.props:
        for k,v in edge_def.props.items():
            p=gen_prop(row,v)
            if len(p)==0:
                continue
            prop_map+=k+':'+p+','
        prop_map=prop_map[:-1]
    prop_map+='}'
    
    #TODO check directional prop of edge_def later
    if len(prop_map)==1:
        return 'MATCH '+src_str+','+dst_str+' MERGE (s)-[:'+rel_str+']->(d)'
    else:
        return 'MATCH '+src_str+','+dst_str+' MERGE (s)-[r:'+rel_str+']->(d) ON MATCH SET r+='+prop_map+' ON CREATE SET r='+prop_map

def create_index():
    for mapper in node_mappers:
        script='CREATE INDEX ON :'+mapper.label+'(id)'
        execute_query(script)

def save_inventory_item(row):
    #print(row['STATE_CODE_001'])
    #script=gen_node_script(row,county_mapper)
    #execute_write(run_query,script)
    
    queries=[]
    for mapper in node_mappers:
        script=gen_node_script(row,mapper)
        #print(script)
        if len(script)>0:
            res=execute_query(script)
            #queries.append(script)
    
    #res=execute_queries(queries)
    
    queries=[]
    for mapper in edge_mappers:
        script=gen_edge_script(row,mapper)
        if len(script)>0:
            res=execute_query(script)
            #queries.append(script)
    
    #res=execute_queries(queries)

for file_path in file_paths:
    if force_init:
        init_states_counties()
        create_index()
    
    with open(file_path,encoding='utf-8') as csv_file:
        csv_reader=csv.DictReader(csv_file,delimiter=',')
        line_count=0
        header=None
        for row in csv_reader:
            if line_count==0:
                #print('column names are {'+','.join(row)+'}')
                header=row
            else:
                #if len(row['OTHER_STATE_CODE_098A'].strip())==0:continue
                save_inventory_item(row)
            
            line_count+=1
            #if line_count>100: break
        
            print('row '+str(line_count)+' processed.')
    
        print('file {'+file_path+'} converted.')