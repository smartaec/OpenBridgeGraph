class NodeMapperDef:
    def __init__(self,label,id_props,props,default_props=None,constraint=None,prop_types=None):
        self.label=label #node label
        self.id_props=id_props #original props to generate id
        self.props=props #map from original props to node props
        self.default_props=default_props #set some default props when create node
        self.constraint=constraint #constraint on original props to generate this node
        self.prop_types=prop_types

class EdgeMapperDef:
    def __init__(self,label,src_label,src_id_props,dst_label,dst_id_props,props=None,directional=True,constraint=None,rel_id=None,prop_types=None):
        self.label=label #relation label
        self.src_label=src_label #source node label
        self.src_id_props=src_id_props #original props to generate source node id
        self.dst_label=dst_label #destination nodel label
        self.dst_id_props=dst_id_props #original props to generate destination node id
        self.props=props #map from original props to relation props
        self.directional=directional #is relation directional or not
        self.constraint=constraint #constraint on original props to generate this relation
        self.rel_id=rel_id if not rel_id==None else label
        self.prop_types=prop_types

node_mappers=[]
edge_mappers=[]

state_mapper=NodeMapperDef(
    label='State',
    id_props=['STATE_CODE_001'],
    props={'state_code':'STATE_CODE_001'},
    prop_types={'state_code':'string'})
node_mappers.append(state_mapper)

county_mapper=NodeMapperDef(
    label='County',
    id_props=['STATE_CODE_001','COUNTY_CODE_003'],
    props={'state_code':'STATE_CODE_001','county_code':'COUNTY_CODE_003'},
    prop_types={'state_code':'string','county_code':'string'})
node_mappers.append(county_mapper)

county_in_state=EdgeMapperDef(
    label='LocateIn',
    src_label='County',
    src_id_props=county_mapper.id_props,
    dst_label='State',
    dst_id_props=state_mapper.id_props,
    props=None,rel_id='County_LocateIn_State')
edge_mappers.append(county_in_state)

bridge_mapper=NodeMapperDef(
    label='Bridge',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008'],
    props={
        'state_code':'STATE_CODE_001',
        'county_code':'COUNTY_CODE_003',
        'structure_number':'STRUCTURE_NUMBER_008',
        'location':'LOCATION_009',
        'latitude':'LAT_016',
        'longitude':'LONG_017',
        'detour_length':'DETOUR_KILOS_019',
        'toll_status':'TOLL_020',
        'year_built':'YEAR_BUILT_027',
        'approach_roadway_width':'APPR_WIDTH_MT_032',
        'median_type':'MEDIAN_CODE_033',
        'skew_angle':'DEGREES_SKEW_034',
        'railing_safety_acceptable':'RAILINGS_036A',
        'transition_safety_acceptable':'TRANSITIONS_036B',
        'guardrail_safety_acceptable':'APPR_RAIL_036C',
        'guardrail_end_safety_acceptable':'APPR_RAIL_END_036D',
        'is_flared':'STRUCTURE_FLARED_035',
        'historical_significance':'HISTORY_037',
        'material_kind':'STRUCTURE_KIND_043A',
        'structure_type':'STRUCTURE_TYPE_043B',
        'span_count':'MAIN_UNIT_SPANS_045',
        'maximum_span_length':'MAX_SPAN_LEN_MT_048',
        'structure_length':'STRUCTURE_LEN_MT_049',
        'left_curb_sidewalk_width':'LEFT_CURB_MT_050A',
        'right_curb_sidewalk_width':'RIGHT_CURB_MT_050B',
        'roadway_width':'ROADWAY_WIDTH_MT_051',
        'deck_width':'DECK_WIDTH_MT_052',
        'minimum_vertical_clearance_over':'VERT_CLR_OVER_MT_053',
        'minimum_vertical_under_clearance':'VERT_CLR_UND_054B',
        'minimum_vertical_under_clearance_reference':'VERT_CLR_UND_REF_054A',
        'left_minimum_lateral_under_clearance':'LEFT_LAT_UND_MT_056',
        'right_minimum_lateral_under_clearance':'LAT_UND_MT_055B',
        'right_minimum_lateral_under_clearance_reference':'LAT_UND_REF_055A',
        'border_state':'OTHER_STATE_CODE_098A',
        'border_structure_number':'OTHR_STATE_STRUC_NO_099',
        'has_temporary_structure':'TEMP_STRUCTURE_103',
        'year_reconstructed':'YEAR_RECONSTRUCTED_106',
        'deck_structure_type':'DECK_STRUCTURE_TYPE_107',
        'wearing_surface_type':'SURFACE_TYPE_108A',
        'membrane_type':'MEMBRANE_TYPE_108B',
        'deck_protection_type':'DECK_PROTECTION_108C',
        'meet_nbis_bridge_length':'BRIDGE_LEN_IND_112',
        'is_scour_critical':'SCOUR_CRITICAL_113',
        
        'designed_live_load':'DESIGN_LOAD_031',
        'approach_span_count':'APPR_SPANS_046',
        'approach_span_material_kind':'APPR_KIND_044A',
        'approach_span_structure_type':'APPR_TYPE_044B',
        'minimum_vertical_clearance':'MIN_VERT_CLR_010',
        'total_horizontal_clearance':'HORR_CLR_MT_047',
        'functional_classification':'FUNCTIONAL_CLASS_026',
        'is_STRAHNET_highway':'STRAHNET_HIGHWAY_100',
        'is_in_highway_system':'HIGHWAY_SYSTEM_104',
        'federal_land_type':'FEDERAL_LANDS_105',
        'is_national_network_for_trucks':'NATIONAL_NETWORK_110',
    },
    prop_types={
        'state_code':'string',
        'county_code':'string',
        'structure_number':'string',
        'location':'string',
        'latitude':'float',
        'longitude':'float',
        'detour_length':'float',
        'toll_status':'string',
        'year_built':'int',
        'approach_roadway_width':'float',
        'median_type':'string',
        'skew_angle':'float',
        'railing_safety_acceptable':'string',
        'transition_safety_acceptable':'string',
        'guardrail_safety_acceptable':'string',
        'guardrail_end_safety_acceptable':'string',
        'is_flared':'string',
        'historical_significance':'string',
        'material_kind':'string',
        'structure_type':'string',
        'span_count':'int',
        'maximum_span_length':'float',
        'structure_length':'float',
        'left_curb_sidewalk_width':'float',
        'right_curb_sidewalk_width':'float',
        'roadway_width':'float',
        'deck_width':'float',
        'minimum_vertical_clearance_over':'float',
        'minimum_vertical_under_clearance':'float',
        'minimum_vertical_under_clearance_reference':'float',
        'left_minimum_lateral_under_clearance':'float',
        'right_minimum_lateral_under_clearance':'float',
        'right_minimum_lateral_under_clearance_reference':'float',
        'border_state':'string',
        'border_structure_number':'string',
        'has_temporary_structure':'string',
        'year_reconstructed':'int',
        'deck_structure_type':'string',
        'wearing_surface_type':'string',
        'membrane_type':'string',
        'deck_protection_type':'string',
        'meet_nbis_bridge_length':'string',
        'is_scour_critical':'string',
        
        'designed_live_load':'float',
        'approach_span_count':'int',
        'approach_span_material_kind':'string',
        'approach_span_structure_type':'string',
        'minimum_vertical_clearance':'float',
        'total_horizontal_clearance':'float',
        'functional_classification':'string',
        'is_STRAHNET_highway':'string',
        'is_in_highway_system':'string',
        'federal_land_type':'string',
        'is_national_network_for_trucks':'string',
    })
node_mappers.append(bridge_mapper)

bridge_in_county=EdgeMapperDef(
    label='LocateIn',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='County',
    dst_id_props=county_mapper.id_props,
    props=None,rel_id='Bridge_LocateIn_County')
edge_mappers.append(bridge_in_county)

agency_mapper=NodeMapperDef(
    label='Agency',
    id_props=['STATE_CODE_001','MAINTENANCE_021'],
    props={
        'agency_code':'MAINTENANCE_021',
        'state_code':'STATE_CODE_001',
    },
    prop_types={
        'agency_code':'string',
        'state_code':'string',
    })
node_mappers.append(agency_mapper)

bridge_owned_by=EdgeMapperDef(
    label='OwnedBy',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Agency',
    dst_id_props=agency_mapper.id_props,
    props=None,rel_id='Bride_OwnedBy_Agency')
edge_mappers.append(bridge_owned_by)

agency_within=EdgeMapperDef(
    label='Within',
    src_label='Agency',
    src_id_props=agency_mapper.id_props,
    dst_label='State',
    dst_id_props=state_mapper.id_props,
    props=None,rel_id='Agency_Within_State')
edge_mappers.append(agency_within)

#percent here should be 100-OTHER_STATE_PCNT_098B, currently just do not set the prop and update the prop with other state bridge record
state_responsible_for=EdgeMapperDef(
    label='ResponsibleFor',
    src_label='State',
    src_id_props=state_mapper.id_props,
    dst_label='Bridge',
    dst_id_props=bridge_mapper.id_props, #props={'percent':'OTHER_STATE_PCNT_098B'}
    rel_id='State_ResponsibleFor_Bridge'
    )
edge_mappers.append(state_responsible_for)

other_state_responsible_for=EdgeMapperDef(
    label='ResponsibleFor',
    src_label='State',
    src_id_props=['OTHER_STATE_CODE_098A'],
    dst_label='Bridge',
    dst_id_props=bridge_mapper.id_props,
    props={'percent':'OTHER_STATE_PCNT_098B'},
    prop_types={'percent':'float'},
    rel_id='OtherState_ResponsibleFor_Bridge')
edge_mappers.append(other_state_responsible_for)

bridge_same_as=EdgeMapperDef(
    label='SameAs',
    src_label='Bridge',
    src_id_props=['OTHER_STATE_CODE_098A','OTHR_STATE_STRUC_NO_099'],
    dst_label='Bridge',
    dst_id_props=bridge_mapper.id_props,
    rel_id='Bridge_SameAs_Bridge')
edge_mappers.append(bridge_same_as)

route_mapper=NodeMapperDef(
    label='Route',
    id_props=['ROUTE_PREFIX_005B','ROUTE_NUMBER_005D'],
    props={
        'signing_prefix':'ROUTE_PREFIX_005B',
        'number':'ROUTE_NUMBER_005D',
    },
    prop_types={
        'signing_prefix':'string',
        'number':'string',
    })
node_mappers.append(route_mapper)

bridge_carray_route=EdgeMapperDef(
    label='Carry',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Route',
    dst_id_props=route_mapper.id_props,
    props={
        'facility':'FACILITY_CARRIED_007',
        'designated_service_level':'SERVICE_LEVEL_005C',
        'directional_suffix':'DIRECTION_005E',
        'kilometer_point':'KILOPOINT_011',
        'lanes_on_count':'TRAFFIC_LANES_ON_028A',
        'lanes_under_count':'TRAFFIC_LANES_UND_028B',
        'service_type_on':'SERVICE_ON_042A',
        'service_type_under':'SERVICE_UND_042B',
    },
    prop_types={
        'facility':'string',
        'designated_service_level':'string',
        'directional_suffix':'string',
        'kilometer_point':'string',
        'lanes_on_count':'int',
        'lanes_under_count':'int',
        'service_type_on':'string',
        'service_type_under':'string',
    },
    constraint={'RECORD_TYPE_005A':'1'},
    rel_id='Bridge_Carry_Route')
edge_mappers.append(bridge_carray_route)

feature_mapper=NodeMapperDef(
    label='Feature',
    id_props=['FEATURES_DESC_006A'],
    props={
        'name':'FEATURES_DESC_006A',
    },
    prop_types={
        'name':'string',
    })
node_mappers.append(feature_mapper)

bridge_intersect_feature=EdgeMapperDef(
    label='Intersect',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Feature',
    dst_id_props=feature_mapper.id_props,
    rel_id='Bridge_Intersect_Feature')
edge_mappers.append(bridge_intersect_feature)

improvement_mapper=NodeMapperDef(
    label='Improvement',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008','WORK_PROPOSED_075A','YEAR_OF_IMP_097'],
    props={
        'work_type':'WORK_PROPOSED_075A',
        'done_by':'WORK_DONE_BY_075B',
        'length':'IMP_LEN_MT_076',
        'bridge_cost':'BRIDGE_IMP_COST_094',
        'roadway_cost':'ROADWAY_IMP_COST_095',
        'total_cost':'TOTAL_IMP_COST_096',
        'year_cost_estimated':'YEAR_OF_IMP_097',
    },
    prop_types={
        'work_type':'string',
        'done_by':'string',
        'length':'float',
        'bridge_cost':'float',
        'roadway_cost':'float',
        'total_cost':'float',
        'year_cost_estimated':'int',
    },
    constraint={'WORK_PROPOSED_075A':lambda x:len(x)>0})
node_mappers.append(improvement_mapper)

bridge_has_improvement=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Improvement',
    dst_id_props=improvement_mapper.id_props,
    props={'year':'YEAR_OF_IMP_097'},
    prop_types={'year':'int'},
    constraint={'WORK_PROPOSED_075A':lambda x:len(x)>0},
    rel_id='Bridge_Has_Improvement')
edge_mappers.append(bridge_has_improvement)

traffic_mapper=NodeMapperDef(
    label='Traffic',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008','YEAR_ADT_030','YEAR_OF_FUTURE_ADT_115'],
    props={
        'control_level':'OPEN_CLOSED_POSTED_041',
        'average_daily_traffic':'ADT_029',
        'year_ADT':'YEAR_ADT_030',
        'direction':'TRAFFIC_DIRECTION_102',
        'average_daily_truck_percent':'PERCENT_ADT_TRUCK_109',
        'future_ADT':'FUTURE_ADT_114',
        'year_future_ADT':'YEAR_OF_FUTURE_ADT_115',
    },
    prop_types={
        'control_level':'string',
        'average_daily_traffic':'float',
        'year_ADT':'string',
        'direction':'string',
        'average_daily_truck_percent':'float',
        'future_ADT':'float',
        'year_future_ADT':'string',
    })
node_mappers.append(traffic_mapper)

bridge_has_traffic=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Traffic',
    dst_id_props=traffic_mapper.id_props,
    rel_id='Bridge_Has_Traffic')
edge_mappers.append(bridge_has_traffic)

navigation_mapper=NodeMapperDef(
    label='Navigation',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008'],
    props={
        'is_controlled':'NAVIGATION_038',
        'vertical_clearance':'NAV_VERT_CLR_MT_039',
        'horizontal_clearance':'NAV_HORR_CLR_MT_040',
        'pier_abutment_protection':'PIER_PROTECTION_111',
        'minimum_vertical_clearance_for_vertical_lift_bridge':'MIN_NAV_CLR_MT_116',
    },
    prop_types={
        'is_controlled':'string',
        'vertical_clearance':'float',
        'horizontal_clearance':'float',
        'pier_abutment_protection':'string',
        'minimum_vertical_clearance_for_vertical_lift_bridge':'float',
    },
    constraint={'NAVIGATION_038':lambda x: x!='N'})
node_mappers.append(navigation_mapper)

bridge_has_navigation=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Navigation',
    dst_id_props=navigation_mapper.id_props,
    constraint={'NAVIGATION_038':lambda x: x!='N'},
    rel_id='Bridge_Has_Navigation')
edge_mappers.append(bridge_has_navigation)


inspection_mapper=NodeMapperDef(
    label='Inspection',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008','DATE_OF_INSPECT_090'],
    props={
        'date':'DATE_OF_INSPECT_090',
        'designated_frequency':'INSPECT_FREQ_MONTHS_091',
        'deck_condition_rating':'DECK_COND_058',
        'superstructure_condition_rating':'SUPERSTRUCTURE_COND_059',
        'substructure_condition_rating':'SUBSTRUCTURE_COND_060',
        'channel_condition_rating':'CHANNEL_COND_061',
        'culvert_rating':'CULVERT_COND_062',
        'operating_rating_method':'OPR_RATING_METH_063',
        'operating_rating':'OPERATING_RATING_064',
        'inventory_rating_method':'INV_RATING_METH_065',
        'inventory_rating':'INVENTORY_RATING_066',
        # 'structural_evaluation_appraisal_rating':'STRUCTURAL_EVAL_067',
        # 'deck_geometry_appraisal_rating':'DECK_GEOMETRY_EVAL_068',
        # 'under_vertical_horizontal_clearance_appraisal_rating':'UNDCLRENCE_EVAL_069',
        # 'posting_appraisal_rating':'POSTING_EVAL_070',
        # 'waterway_adquacy_appraisal_rating':'WATERWAY_EVAL_071',
        # 'approach_roadway_alignment_appraisal_rating':'APPR_ROAD_EVAL_072','structural_evaluation':'STRUCTURAL_EVAL_067',
        'deck_geometry_evaluation':'DECK_GEOMETRY_EVAL_068',
        'clearance_evaluation':'UNDCLRENCE_EVAL_069',
        'posting_evaluation':'POSTING_EVAL_070',
        'waterway_adquacy_evaluation':'WATERWAY_EVAL_071',
        'approach_roadway_evaluation':'APPR_ROAD_EVAL_072',
    },
    prop_types={
        'date':'datetime',
        'designated_frequency':'int',
        'deck_condition_rating':'int',
        'superstructure_condition_rating':'int',
        'substructure_condition_rating':'int',
        'channel_condition_rating':'int',
        'culvert_rating':'int',
        'operating_rating_method':'string',
        'operating_rating':'int',
        'inventory_rating_method':'string',
        'inventory_rating':'int',
        # 'structural_evaluation_appraisal_rating':'int',
        # 'deck_geometry_appraisal_rating':'int',
        # 'under_vertical_horizontal_clearance_appraisal_rating':'int',
        # 'posting_appraisal_rating':'int',
        # 'waterway_adquacy_appraisal_rating':'int',
        # 'approach_roadway_alignment_appraisal_rating':'int','structural_evaluation':'float',
        'deck_geometry_evaluation':'float',
        'clearance_evaluation':'float',
        'posting_evaluation':'float',
        'waterway_adquacy_evaluation':'float',
        'approach_roadway_evaluation':'float',
    },
    constraint={'DATE_OF_INSPECT_090':lambda x:len(x)>0})
node_mappers.append(inspection_mapper)

bridge_has_inspection=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='Inspection',
    dst_id_props=inspection_mapper.id_props,
    constraint={'DATE_OF_INSPECT_090':lambda x:len(x)>0},
    rel_id='Bridge_Has_Inspection')
edge_mappers.append(bridge_has_inspection)


#TODO it seems no need to create three EdgeMapperDefs here, for now we just use the same rel_id for outputting edges in the same csv
spec_inspection_mapper_1=NodeMapperDef(
    label='SpecialInspection',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008','FRACTURE_092A','UNDWATER_LOOK_SEE_092B','SPEC_INSPECT_092C'],
    props={'date':'FRACTURE_LAST_DATE_093A','designated_frequency':'FRACTURE_092A'},
    default_props={'category':'fracture critical details'},
    constraint={'FRACTURE_092A':lambda x:not x.startswith('N')})
node_mappers.append(spec_inspection_mapper_1)
bridge_has_special_1=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='SpecialInspection',
    dst_id_props=spec_inspection_mapper_1.id_props,
    constraint={'FRACTURE_092A':lambda x:not x.startswith('N')},
    rel_id='Bridge_Has_SpecialInspection'#_Fracture'
    )
edge_mappers.append(bridge_has_special_1)

spec_inspection_mapper_2=NodeMapperDef(
    label='SpecialInspection',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008','FRACTURE_092A','UNDWATER_LOOK_SEE_092B','SPEC_INSPECT_092C'],
    props={'date':'UNDWATER_LAST_DATE_093B','designated_frequency':'UNDWATER_LOOK_SEE_092B'},
    prop_types={'date':'datetime','designated_frequency':'int'},
    default_props={'category':'underwater inspection'},
    constraint={'UNDWATER_LOOK_SEE_092B':lambda x:not x.startswith('N')})
node_mappers.append(spec_inspection_mapper_2)
bridge_has_special_2=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='SpecialInspection',
    dst_id_props=spec_inspection_mapper_2.id_props,
    constraint={'UNDWATER_LOOK_SEE_092B':lambda x:not x.startswith('N')},
    rel_id='Bridge_Has_SpecialInspection'#_Underwater'
    )
edge_mappers.append(bridge_has_special_2)

spec_inspection_mapper_3=NodeMapperDef(
    label='SpecialInspection',
    id_props=['STATE_CODE_001','STRUCTURE_NUMBER_008','FRACTURE_092A','UNDWATER_LOOK_SEE_092B','SPEC_INSPECT_092C'],
    props={'date':'SPEC_LAST_DATE_093C','designated_frequency':'SPEC_INSPECT_092C'},
    prop_types={'date':'datetime','designated_frequency':'int'},
    default_props={'category':'other special inspection'},
    constraint={'SPEC_INSPECT_092C':lambda x:not x.startswith('N')})
node_mappers.append(spec_inspection_mapper_3)
bridge_has_special_3=EdgeMapperDef(
    label='Has',
    src_label='Bridge',
    src_id_props=bridge_mapper.id_props,
    dst_label='SpecialInspection',
    dst_id_props=spec_inspection_mapper_3.id_props,
    constraint={'SPEC_INSPECT_092C':lambda x:not x.startswith('N')},
    rel_id='Bridge_Has_SpecialInspection')
edge_mappers.append(bridge_has_special_3)

#===========================
# THE FOLLOWING IS FOR PROCESSING CLIMATE DATA FROM noaa.gov
#===========================
station_node_mappers=[]
station_edge_mappers=[]

station_mapper=NodeMapperDef(
    label='Station',
    id_props=['STATION'],
    props={
        'name':'NAME',
        'latitude':'LATITUDE',
        'longitude':'LONGITUDE',
        'elevation':'ELEVATION'
    },
    prop_types={
        'name':'string',
        'latitude':'float',
        'longitude':'float',
        'elevation':'float'
    })
station_node_mappers.append(station_mapper)

observation_mapper=NodeMapperDef(
    label='Observation',
    id_props=['STATION','DATE'],
    props={
        'date':'DATE',
        'average_wind_speed':'AWND',
        'precipitation':'PRCP',
        'days_multiday_percipitation':'DAPR',
        'multiday_percipitation':'MDPR',
        'peak_gust_time':'PGTM',
        'daily_percent_sunshine':'PSUN',
        'total_sunshine':'TSUN',
        'snow_depth':'SNWD',
        'snowfall':'SNOW',
        'temperature':'TOBS',
        'average_temperature':'TAVG'
    },
    prop_types={
        'date':'datetime',
        'average_wind_speed':'float',
        'precipitation':'float',
        'days_multiday_percipitation':'int',
        'multiday_percipitation':'float',
        'peak_gust_time':'float',
        'daily_percent_sunshine':'int',
        'total_sunshine':'int',
        'snow_depth':'int',
        'snowfall':'int',
        'temperature':'float',
        'average_temperature':'float'
    })
station_node_mappers.append(observation_mapper)

station_has_observation=EdgeMapperDef(
    label='Has',
    src_label='Station',
    src_id_props=station_mapper.id_props,
    dst_label='Observation',
    dst_id_props=observation_mapper.id_props,
    rel_id='Station_Has_Observation')
station_edge_mappers.append(station_has_observation)