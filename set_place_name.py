import csv
from neo4j_helper import *
from nbi_static_data import *

def init_states_counties():
    execute_query('CREATE INDEX ON :State(id)')
    execute_query('CREATE INDEX ON :State(state_code)')
    execute_query('CREATE INDEX ON :County(id)')
    execute_query('CREATE INDEX ON :County(state_code)')
    for k,v in state_codes.items():
        prop_code='state_code:\''+k[:-1]+'\''
        prop_id='id:\''+k[:-1]+'\''
        prop_name='name:\''+v+'\''
        script='MERGE (p:State{'+prop_id+'}) on MATCH set p+={'+prop_name+','+prop_id+'} ON CREATE SET p={'+prop_code+','+prop_name+','+prop_id+'}'
        execute_query(script)

    for k,v in county_codes.items():
        #if not (k[:2]=='26' or k[:2]=='39'): continue
        prop_state='state_code:\''+k[:2]+'\''
        prop_county='county_code:\''+k[-3:]+'\''
        prop_id='id:\''+k[:2]+'_'+k[-3:]+'\''
        prop_name='name:\''+v+'\''
        script='MERGE (p:County{'+prop_id+'}) on MATCH set p+={'+prop_name+','+prop_id+'} ON CREATE SET p={'+prop_state+','+prop_county+','+prop_name+','+prop_id+'}'
        #print(script)
        execute_query(script)
        
        script='MATCH (p:County{'+prop_state+'}),(s:State{'+prop_state+'}) MERGE (p)-[:LocateIn]-(s)'
        execute_query(script)

    print('updated...')

init_states_counties()