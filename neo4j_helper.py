from neo4j.v1 import GraphDatabase #neo4j==1.7.0

uri="bolt://localhost:7687"
driver=GraphDatabase.driver(uri, auth=("neo4j", "testneo4j"))

def execute_queries(scripts,message=None):
    with driver.session() as session:
        tx=session.begin_transaction()
        res=tx.run(';'.join(scripts))
        tx.commit()
        return res

def execute_query(script,message=None):
    with driver.session() as session:
        return session.run(script,message)

def execute_read(cypher_func,message):
    with driver.session() as session:
        return session.read_transaction(cypher_func,message)

def execute_write(cypher_func,message):
    with driver.session() as session:
        return session.write_transaction(cypher_func,message)

def run_query(tx,script):
    return tx.run(script)

def print_query(tx,name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(f) WHERE a.name = {name} RETURN f.name",name=name):
       print(record["f.name"])
    
    return ""

#execute_read(print_query,'Alice')