# OpenBridgeGraph
This repo contains scripts for the paper entitled "OpenBridgeGraph: Integrating Open Government Data for Bridge Management".

Use the following data to reference this repo or the paper:  
Lin, J.-R.(2020), OpenBridgeGraph: Integrating Open Government Data for Bridge Management. in Proceedings of the 37th International Symposium on Automation and Robotics in Construction (ISARC 2020). (Submitted)

## Introduction
Due to limited funds, road authorities around the world are facing challenges related to bridge management and the escalating maintenance requirements of large infrastructure assets. Nowadays, many government organizations have published a variety of data to enable transparency, foster applications, and to satisfy legal obligations. Open governments data like bridge data, weather data would help to better assess the condition of bridges for maintenance purpose and allocation of funds. However, these data sets are fragmented in different systems or formats, and their value in bridge management are not fully explored. This paper proposes a graph-based bridge information modeling framework to integrate open government data for bridge management. The framework represents bridge inventory data as a labeled property graph model and extends the model with weather data. Implementation of the framework employs python scripts for data processing, and neo4j database for data management. The framework is demonstrated using data from national bridge inventory (NBI) and national oceanic and atmosphere administration (NOAA). The results show that the proposed framework can potentially facilitate the integration and retrieval of public government data, and effectively support and provide services to bridge management.

## Data used
1. download bridge inventory data from [the NBI website](https://www.fhwa.dot.gov/bridge/nbi.cfm)
2. download weather data from [the NOAA website](https://www.ncdc.noaa.gov/cdo-web/)
3. choose csv format when downloading data.

## How to load and integrate data
### Save one by one (obsoleted)
1. open cmd
2. run python nbi2graph.py MI11.txt MI12.txt MI13.txt MI14.txt MI15.txt MI16.txt
3. this takes quite a long time, and only deals with the NBI data

### Batch loading
1. open cmd
2. run python gen_state_county_csv.py
3. run python gen_nbi_csv_v2.py MI11.txt
4. run python gen_nbi_csv_v2.py MI12.txt true #append csv to previously generated
5. run python gen_nbi_csv_v2.py MI13.txt true #append csv to previously generated
6. run python gen_nbi_csv_v2.py MI14.txt true #append csv to previously generated
7. run python gen_nbi_csv_v2.py MI15.txt true #append csv to previously generated
8. run python gen_nbi_csv_v2.py MI16.txt true #append csv to previously generated
8. run python gen_nbi_csv_v2.py WI16.txt true #append csv to previously generated
9. run python gen_climate_csv.py MI_Climate.csv
10. run python del_nbi_csv_duplicate.py
11. copy all data in output folder to import folder of neo4j installation path
12. loading all csv files
12.1 exec scripts in load_state_county.script line by line
12.2 exec scripts in load_nbi_data.script line by line
12.3 exec scripts in post_nbi_data.script line by line
12.4 exec scripts in load_climate_data.script line by line
12.5 exec scripts in post_climate_data.script line by line
13. run python exec_import_script.py

## Exemplary queries
1. match p=(s:State{state_code:'26'})-[:LocateIn*..]-(b:Bridge)-[:Has]-(i:SpecialInspection) return p limit 50
2. match p=(s:State{state_code:'26'})-[:LocateIn*..]-(b:Bridge)-[:Has]-(i) WHERE 'Improvement' IN LABELS(i) OR 'SpecialInspection' IN LABELS(i) return p limit 50
3. match p=(im:Improvement)-[:Has]-(b:Bridge)-[:Has]-(s:SpecialInspection) return p limit 50
4. match p=(s:SpecialInspection)-[:Has]-(b:Bridge)-[:Carry]-(ro:Route)-[:Carry]-(b2:Bridge)-[:Has]-(s2:SpecialInspection) where s2.category=s.category return p limit 25
5. match p=(b:Bridge)-[r:Intersect|:Carry]-() return p limit 30
6. match p=(im:Improvement)-[:Has]-(b:Bridge)-[:Has]-(s:SpecialInspection) match q=(b)-[:Has]-(i:Inspection) return p,q limit 50
7. match p=(im:Improvement)-[:Has]-(b:Bridge)-[:Has]-(s:SpecialInspection) match q=(b)-[:Has]-(i:Inspection) where im.total_cost>100  return p,q limit 50
8. match p=(f:Feature)-[:Intersect]-(b1:Bridge)-[:LocateIn*1..2]-()-[:LocateIn*1..2]-(b2:Bridge)-[:Intersect]-(f:Feature) return p limit 30
9. match p=(s:State)<-[:LocateIn*..2]-(b:Bridge)-[:SameAs]-(b2:Bridge)-[:LocateIn*..2]->(s1:State) return p
10. match p=(b:Bridge)-[:Has]->(ins:SpecialInspection{category:'underwater inspection'}),q=(s:Station)-[:Has]->(o:Observation) where ins.date=o.date and o.precipitation>0 and exists(o.temperature) return b.structure_number,ins.date,o.temperature,o.precipitation,distance(b.loc_point,s.loc_point)/1000 as distance order by distance limit 5