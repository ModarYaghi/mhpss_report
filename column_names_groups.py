tt_passwords = {
    'TS_FC_meetingOutreachReferralFollowUpAdvocacy.xlsx': 'Ahmed02',
    'tt_psc_IJ_v04.xlsx': 'Israa006',
    'tt_psc_LA_v04.xlsx': 'Lama010',
    'tt_psc_MT_v04.xlsx': 'Mt011',
    'tt_psc_SA_v04.xlsx': 'Salwa003',
    'tt_psc_YQ-v04.xlsx': 'Yaqzan004',
    'tt_pt_HJ_v04.xlsx': 'Heba001',
    'tt_pt_HR_v04.xlsx': 'Hind002'
}

screening_columns = [
    'scspi',
    'rid',
    'firstname',
    'lastname',
    'sex',
    'age',
    'nat',
    'scloc',
    'sc1',
    'sc2',
    'scre',
    'srs',
    'srsorg',
    'mhpss',
    'trw',
    'outref',
    'tmh',
    'pei',
    'note'
]

screening_basic_columns = [
    'rid',
    'firstname',
    'lastname',
    'sc1',
    'sc2',
    'scre'
]

screening_date_columns = [
    'sc1',
    'sc2',
    'scre'
]

screening_to_service = [
    'mhpss',
    'trw',
    'outref',
    'tmh',
    'pei',
]

screening_basic_int_columns = [
    'scspi',
    'age'
]

screening_all_int_columns = [
    'scspi',
    'age',
    'sex',
    'mhpss',
    'trw',
    'outref',
    'tmh',
    'pei',
    'sert'
]

screening_numerical_variables = [
    'scspi',
    'sex',
    'age',
    'mhpss',
    'trw',
    'outref',
    'tmh',
    'pei',
    'sert'
]

intake_columns = [
    'ntspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'nt1',
    'nt2',
    'nt3',
    'ntre',
    'fom',
    'sod',
    'pts',
    'sts',
    'vsva',
    'vsvp',
    'hrd',
    'jrn',
    'wov',
    'stgbv',
    'lgbti',
    'other',
    'note'
]

intake_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'nt1',
    'nt2',
    'nt3',
    'ntre'
]

intake_date_columns = [
    'nt1',
    'nt2',
    'nt3',
    'ntre'
]

victimhood = [
    'fom',
    'sod',
    'pts',
    'sts',
    'vsva',
    'vsvp',
    'hrd',
    'jrn',
    'wov',
    'stgbv',
    'lgbti',
    'other'
]

intake_numerical_variables = [
    'ntspi',
    'fcid',
    'nt',
    'fom',
    'sod',
    'pts',
    'sts',
    'vsva',
    'vsvp',
    'hrd',
    'jrn',
    'wov',
    'stgbv',
    'lgbti',
    'other',
    'vict'
]

group_counseling_columns = [
    'gcspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptn',
    'gcindx',
    'gccls',
    'gc1',
    'gc2',
    'gc3',
    'gc4',
    'chin',
    'gc5',
    'gc6',
    'gc7',
    'gc8',
    'gc9',
    'gc10',
    'gct',
    'note'
]

group_counseling_date_columns = [
    'gc1',
    'gc2',
    'gc3',
    'gc4',
    'chin',
    'gc5',
    'gc6',
    'gc7',
    'gc8',
    'gc9',
    'gc10'
]

group_counseling_basic_date_columns = [
    'gc1',
    'gc2',
    'gc3',
    'gc4',
    'gc5',
    'gc6',
    'gc7',
    'gc8',
    'gc9',
    'gc10'
]

group_counseling_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'gc1',
    'gc2',
    'gc3',
    'gc4',
    'chin',
    'gc5',
    'gc6',
    'gc7',
    'gc8',
    'gc9',
    'gc10'
]

individual_counseling_columns = [
    'icspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptn',
    'ic1',
    'ic2',
    'ic3',
    'ic4',
    'ic5',
    'ic6',
    'ic7',
    'ic8',
    'ic9',
    'ic10',
    'ict',
    'note'
]

individual_counseling_date_columns = [
    'ic1',
    'ic2',
    'ic3',
    'ic4',
    'ic5',
    'ic6',
    'ic7',
    'ic8',
    'ic9',
    'ic10'
]

individual_counseling_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ic1',
    'ic2',
    'ic3',
    'ic4',
    'ic5',
    'ic6',
    'ic7',
    'ic8',
    'ic9',
    'ic10'
]

follow_up_columns = [
    'fuspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    '3m',
    '6m',
    '12m',
    'status',
    'closure_reason',
    'note'
]

follow_up_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    '3m',
    '6m',
    '12m'
]

follow_up_date_columns = [
    '3m',
    '6m',
    '12m'
]

follow_up_int_columns = [
    'fuspi',
    'fcid'
]

pei_columns = [
    'pespi',
    'rid',
    'fcid',
    'peloc',
    'firstname',
    'lastname',
    'pe1',
    'pe2',
    'pe3',
    'pet',
    'pef',
    'note'
]

pei_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'pe1',
    'pe2',
    'pe3',
    'pef'
]

pei_date_columns = [
    'pe1',
    'pe2',
    'pe3',
    'pef'
]

pei_int_columns = [
    'pespi',
    'fcid',
    'pet'
]

trw_columns = [
    'trspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'tr1',
    'tr2',
    'trt',
    'fac1',
    'fac2',
    'note'
]

trw_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'tr1',
    'tr2'
]

trw_date_columns = [
    'tr1',
    'tr2'
]

trw_int_columns = [
    'trspi',
    'fcid',
    'trt'
]

td_columns = [
    'tdspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'cslt',
    'csnt',
    'ld',
    'iu',
    'cw',
    'com',
    'adv',
    'is1',
    'is2',
    'is3',
    'tdt',
    'note'
]

td_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'cslt',
    'csnt',
    'ld',
    'iu',
    'cw',
    'com',
    'adv',
    'is1',
    'is2',
    'is3'
]

td_date_columns = [
    'cslt',
    'csnt',
    'is1',
    'is2',
    'is3'
]

td_date_p1_columns = [
    'cslt',
    'csnt'
]

td_date_p2_columns = [
    'is1',
    'is2',
    'is3'
]

td_int_columns = [
    'tdspi',
    'fcid',
    'tdt'
]

td_pathways = [
    'ld',
    'iu',
    'cw',
    'com',
    'adv'
]

cws_columns = [
    'cwspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'cw1',
    'cw2',
    'cwt',
    'note'
]

cws_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'cw1',
    'cw2'
]

cws_date_columns = [
    'cw1',
    'cw2'
]

cws_int_columns = [
    'cwspi',
    'fcid',
    'cwt'
]

aw_columns = [
    'awspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'sex',
    'age',
    'awloc',
    'awci',
    'aws',
    'note'
]

aw_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'awci',
    'aws'
]

aw_date_columns = [
    'awci',
    'aws'
]

aw_int_columns = [
    'awspi',
    'fcid',
    'age'
]

psfs_columns = [
    'pfspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'sex',
    'age',
    'nat',
    'psfs',
    'sco',
    'vic',
    'note'
]

psfs_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'psfs'
]

psfs_date_columns = [
    'psfs'
]

psfs_int_columns = [
    'pfspi',
    'fcid',
    'age'
]

ptnt_columns = [
    'ptntspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptnt1',
    'ptnt2',
    'ptntre',
    'ptntpsc',
    'note'
]

ptnt_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptnt1',
    'ptnt2',
    'ptntre'
]

ptnt_date_columns = [
    'ptnt1',
    'ptnt2',
    'ptntre'
]

ptnt_int_columns = [
    'ptntspi',
    'fcid',
]

ptgc_columns = [
    'ptgcspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptgcls',
    'ptgc1',
    'ptgc2',
    'ptgc3',
    'ptgc4',
    'ptgc5',
    'ptgc6',
    'ptgc7',
    'ptgc8',
    'ptgc9',
    'ptgc10',
    'ptgct',
    'ptgcst',
    'note'
]

ptgc_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptgc1',
    'ptgc2',
    'ptgc3',
    'ptgc4',
    'ptgc5',
    'ptgc6',
    'ptgc7',
    'ptgc8',
    'ptgc9',
    'ptgc10'
]

ptgc_date_columns = [
    'ptgc1',
    'ptgc2',
    'ptgc3',
    'ptgc4',
    'ptgc5',
    'ptgc6',
    'ptgc7',
    'ptgc8',
    'ptgc9',
    'ptgc10'
]

ptgc_int_columns = [
    'ptgcspi',
    'fcid',
    'ptgct'
]

ptic_columns = [
    'pticspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptic1',
    'ptic2',
    'ptic3',
    'ptic4',
    'ptic5',
    'ptic6',
    'ptic7',
    'ptic8',
    'ptic9',
    'ptic10',
    'ptict',
    'pticst',
    'note'
]

ptic_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'ptic1',
    'ptic2',
    'ptic3',
    'ptic4',
    'ptic5',
    'ptic6',
    'ptic7',
    'ptic8',
    'ptic9',
    'ptic10'
]

ptic_date_columns = [
    'ptic1',
    'ptic2',
    'ptic3',
    'ptic4',
    'ptic5',
    'ptic6',
    'ptic7',
    'ptic8',
    'ptic9',
    'ptic10'
]

ptic_int_columns = [
    'pticspi',
    'fcid',
    'ptict'
]

ptfua_columns = [
    'ptfuspi',
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'pt3m',
    'pt6m',
    'pt12m',
    'ptst',
    'pt_closure_reason',
    'note'
]

ptfua_basic_columns = [
    'rid',
    'fcid',
    'firstname',
    'lastname',
    'pt3m',
    'pt6m',
    'pt12m'
]

ptfua_date_columns = [
    'pt3m',
    'pt6m',
    'pt12m'
]

ptfua_int_columns = [
    'ptfuspi',
    'fcid'
]
