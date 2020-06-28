import datetime

prop_converters={}

def get_string(input,clean=True,length=0,fill_char=''):
    if clean:
        input=input.strip()
        input=input.replace('\'',' ')
        input=input.replace('\\',' ')
    if length==0:
        return input
    
    res=input[:length]
    c=length-len(res)
    for i in range(c):
        res=fill_char+res
    return res

def get_real(input,digits=0,length=4):
    if digits==0:
        return int(input)
    else:
        return float(input)
    #TODO the following should be the right according to the coding guide, however, it sames that the file from NBIS already did what the follow code do
    input=input.strip()
    if input.find('.')!=-1:
        return float(input)
    
    c=max(length,digits)
    if c>len(input):
        for i in range(c-len(input)):
            input='0'+input
        input=input[:-digits]+'.'+input[-digits:]
        return float(input)
    
    return int(input)

def get_latlong(input):
    degree=float(input[:-6])    
    minute=float(input[-6:-4])    
    second=float(input[-4:])/100.0
    return degree+minute/60.0+second/3600.0

def get_year(input):
    return int(input)
    
def get_date(input,length=4):
    month=int(input[:-2])
    year_str=input[-2:]
    if int(year_str[0])<3:#tricky code here
        year=int('20'+year_str)
    else:
        year=int('19'+year_str)
    #print(str(year)+'/'+str(month))
    return datetime.datetime(year,month,1)

prop_converters['STATE_CODE_001']=lambda x:get_string(x,length=2)#TODO length should be 3
prop_converters['HIGHWAY_DISTRICT_002']=lambda x:get_string(x,length=2)
prop_converters['COUNTY_CODE_003']=lambda x:get_string(x,length=3)
prop_converters['PLACE_CODE_004']=lambda x:get_string(x,length=5)
prop_converters['RECORD_TYPE_005A']=lambda x:get_string(x,length=1,fill_char='1') #if no data provided, take 'on' as default
#TODO deal with 5B,5C,5E
prop_converters['ROUTE_PREFIX_005B']=lambda x:get_string(x,length=1,fill_char='1') 
prop_converters['SERVICE_LEVEL_005C']=lambda x:get_string(x,length=1,fill_char='1') 
prop_converters['ROUTE_NUMBER_005D']=lambda x:get_string(x,length=5,fill_char='')
prop_converters['DIRECTION_005E']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['FEATURES_DESC_006A']=lambda x:get_string(x)
prop_converters['FACILITY_CARRIED_007']=lambda x:get_string(x)
prop_converters['STRUCTURE_NUMBER_008']=lambda x:get_string(x,length=15,fill_char='0')
prop_converters['LOCATION_009']=lambda x:get_string(x)
prop_converters['MIN_VERT_CLR_010']=lambda x:get_real(x,digits=2,length=4)
prop_converters['KILOPOINT_011']=lambda x:get_real(x,digits=3,length=7)
#TODO convert the following to boolean
prop_converters['BASE_HWY_NETWORK_012']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['LRS_INV_ROUTE_013A']=lambda x:get_string(x,length=10)
prop_converters['SUBROUTE_NO_013B']=lambda x:get_string(x,length=2)
prop_converters['LAT_016']=lambda x:get_latlong(x)
prop_converters['LONG_017']=lambda x:-get_latlong(x) #fix latlong, WARNING this is not tested with enough cases
prop_converters['DETOUR_KILOS_019']=lambda x:get_real(x,length=3)
#TODO deal with item 20,21,22,26
prop_converters['TOLL_020']=lambda x:get_string(x,length=1,fill_char='1')
prop_converters['MAINTENANCE_021']=lambda x:get_string(x,length=2,fill_char='0')
prop_converters['OWNER_022']=lambda x:get_string(x,length=2,fill_char='0')
prop_converters['FUNCTIONAL_CLASS_026']=lambda x:get_string(x,length=2,fill_char='0')
prop_converters['YEAR_BUILT_027']=lambda x:get_year(x)
prop_converters['TRAFFIC_LANES_ON_028A']=lambda x:get_real(x,length=2)
prop_converters['TRAFFIC_LANES_UND_028B']=lambda x:get_real(x,length=2)
prop_converters['ADT_029']=lambda x:get_real(x,length=6)
prop_converters['YEAR_ADT_030']=lambda x:get_year(x)
prop_converters['DESIGN_LOAD_031']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['APPR_WIDTH_MT_032']=lambda x:get_real(x,digits=1,length=4)
prop_converters['MEDIAN_CODE_033']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['DEGREES_SKEW_034']=lambda x:get_real(x,length=2)
#TODO deal with item 35,36A/B/C/D,37,38
prop_converters['STRUCTURE_FLARED_035']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['RAILINGS_036A']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['TRANSITIONS_036B']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['APPR_RAIL_036C']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['APPR_RAIL_END_036D']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['HISTORY_037']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['NAVIGATION_038']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['NAV_VERT_CLR_MT_039']=lambda x:get_real(x,digits=1,length=4)
prop_converters['NAV_HORR_CLR_MT_040']=lambda x:get_real(x,digits=1,length=5)
#TODO deal with item 41,42,43,44
prop_converters['OPEN_CLOSED_POSTED_041']=lambda x:get_string(x,length=1,fill_char='A')
prop_converters['SERVICE_ON_042A']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['SERVICE_UND_042B']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['STRUCTURE_KIND_043A']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['STRUCTURE_TYPE_043B']=lambda x:get_string(x,length=2,fill_char='0')
prop_converters['APPR_KIND_044A']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['APPR_TYPE_044B']=lambda x:get_string(x,length=2,fill_char='0')
prop_converters['MAIN_UNIT_SPANS_045']=lambda x:get_real(x,length=3)
prop_converters['APPR_SPANS_046']=lambda x:get_real(x,length=4)
prop_converters['HORR_CLR_MT_047']=lambda x:get_real(x,digits=1,length=3)
prop_converters['MAX_SPAN_LEN_MT_048']=lambda x:get_real(x,digits=1,length=5)
prop_converters['STRUCTURE_LEN_MT_049']=lambda x:get_real(x,digits=1,length=6)
prop_converters['LEFT_CURB_MT_050A']=lambda x:get_real(x,digits=1,length=3)
prop_converters['RIGHT_CURB_MT_050B']=lambda x:get_real(x,digits=1,length=3)
prop_converters['ROADWAY_WIDTH_MT_051']=lambda x:get_real(x,digits=1,length=4)
prop_converters['DECK_WIDTH_MT_052']=lambda x:get_real(x,digits=1,length=4)
prop_converters['VERT_CLR_OVER_MT_053']=lambda x:get_real(x,digits=2,length=4)
prop_converters['VERT_CLR_UND_REF_054A']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['VERT_CLR_UND_054B']=lambda x:get_real(x,digits=2,length=4)
prop_converters['LAT_UND_REF_055A']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['LAT_UND_MT_055B']=lambda x:get_real(x,digits=1,length=3)
prop_converters['LEFT_LAT_UND_MT_056']=lambda x:get_real(x,digits=1,length=3)
#TODO deal with item 58-63,65
prop_converters['DECK_COND_058']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['SUPERSTRUCTURE_COND_059']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['SUBSTRUCTURE_COND_060']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['CHANNEL_COND_061']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['CULVERT_COND_062']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['OPR_RATING_METH_063']=lambda x:get_string(x,length=1,fill_char='5')
prop_converters['OPERATING_RATING_064']=lambda x:get_real(x,digits=1,length=3)
prop_converters['INV_RATING_METH_065']=lambda x:get_string(x,length=1,fill_char='5')
prop_converters['INVENTORY_RATING_066']=lambda x:get_real(x,digits=1,length=3)
#TODO deal with item 67-72,75
prop_converters['STRUCTURAL_EVAL_067']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['DECK_GEOMETRY_EVAL_068']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['UNDCLRENCE_EVAL_069']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['POSTING_EVAL_070']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['WATERWAY_EVAL_071']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['APPR_ROAD_EVAL_072']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['WORK_PROPOSED_075A']=lambda x:get_string(x,length=2,fill_char='3')
prop_converters['WORK_DONE_BY_075B']=lambda x:get_string(x,length=1,fill_char='1')
prop_converters['IMP_LEN_MT_076']=lambda x:get_real(x,digits=1,length=6)
prop_converters['DATE_OF_INSPECT_090']=lambda x:get_date(x,length=4)
prop_converters['INSPECT_FREQ_MONTHS_091']=lambda x:get_real(x,length=2)
#TODO deal with item 92A/B/C
prop_converters['FRACTURE_092A']=lambda x:get_string(x,length=3)
prop_converters['UNDWATER_LOOK_SEE_092B']=lambda x:get_string(x,length=3)
prop_converters['SPEC_INSPECT_092C']=lambda x:get_string(x,length=3)
prop_converters['FRACTURE_LAST_DATE_093A']=lambda x:get_date(x,length=4)
prop_converters['UNDWATER_LAST_DATE_093B']=lambda x:get_date(x,length=4)
prop_converters['SPEC_LAST_DATE_093C']=lambda x:get_date(x,length=4)
prop_converters['BRIDGE_IMP_COST_094']=lambda x:get_real(x,length=6)
prop_converters['ROADWAY_IMP_COST_095']=lambda x:get_real(x,length=6)
prop_converters['TOTAL_IMP_COST_096']=lambda x:get_real(x,length=6)
prop_converters['YEAR_OF_IMP_097']=lambda x:get_year(x)
prop_converters['OTHER_STATE_CODE_098A']=lambda x:get_string(x,length=2)#TODO length should be 3
prop_converters['OTHER_STATE_PCNT_098B']=lambda x:get_real(x,length=2)
prop_converters['OTHR_STATE_STRUC_NO_099']=lambda x:get_string(x,length=15,fill_char='0')
#TODO deal with item 100-105,107,108,110,111,112,113,
prop_converters['STRAHNET_HIGHWAY_100']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['PARALLEL_STRUCTURE_101']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['TRAFFIC_DIRECTION_102']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['TEMP_STRUCTURE_103']=lambda x:get_string(x,length=1)
prop_converters['HIGHWAY_SYSTEM_104']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['FEDERAL_LANDS_105']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['YEAR_RECONSTRUCTED_106']=lambda x:get_year(x)
prop_converters['DECK_STRUCTURE_TYPE_107']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['SURFACE_TYPE_108A']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['MEMBRANE_TYPE_108B']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['DECK_PROTECTION_108C']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['PERCENT_ADT_TRUCK_109']=lambda x:get_real(x,length=2)
prop_converters['NATIONAL_NETWORK_110']=lambda x:get_string(x,length=1,fill_char='0')
prop_converters['PIER_PROTECTION_111']=lambda x:get_string(x,length=1,fill_char='5')
prop_converters['BRIDGE_LEN_IND_112']=lambda x:get_string(x,length=1,fill_char='Y')
prop_converters['SCOUR_CRITICAL_113']=lambda x:get_string(x,length=1,fill_char='N')
prop_converters['FUTURE_ADT_114']=lambda x:get_real(x,length=6)
prop_converters['YEAR_OF_FUTURE_ADT_115']=lambda x:get_year(x)
prop_converters['MIN_NAV_CLR_MT_116']=lambda x:get_real(x,digits=1,length=4)#TODO the coding guide is inconsistent