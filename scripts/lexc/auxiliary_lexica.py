auxiliary_forms = [
    ('mpi',       'adjective',   '16',   'mp:mm',    'back',        '+comparative',        'COMPARATIVE_MPI_BACK'),
    ('mpi',       'adjective',   '16',   'mp:mm',    'front',    '+comparative',        'COMPARATIVE_MPI_FRONT'),
    ('in',        'adjective',    '36',   None,        'back',        '+superlative',        'SUPERLATIVE_IN_BACK'),
    ('in',        'adjective',    '36',   None,        'front',    '+superlative',        'SUPERLATIVE_IN_FRONT'),
    ('tu',        'adjective',    '1',    't:',        'back',        '+pass+part_past',    'PARTICIPLE_T|TU_BACK'),
    ('ty',        'adjective',    '1',    't:',        'front',    '+pass+part_past',    'PARTICIPLE_T|TU_FRONT'),
    ('tu',        'adjective',    '1',    't:n',        'back',        '+pass+part_past',    'PARTICIPLE_N|TU_BACK'),
    ('ty',        'adjective',    '1',    't:n',        'front',    '+pass+part_past',    'PARTICIPLE_N|TU_FRONT'),
    ('tu',        'adjective',    '1',    't:l',        'back',        '+pass+part_past',    'PARTICIPLE_L|TU_BACK'),
    ('ty',        'adjective',    '1',    't:l',        'front',    '+pass+part_past',    'PARTICIPLE_L|TU_FRONT'),
    ('tu',        'adjective',    '1',    't:r',        'back',        '+pass+part_past',    'PARTICIPLE_R|TU_BACK'),
    ('ty',        'adjective',    '1',    't:r',        'front',    '+pass+part_past',    'PARTICIPLE_R|TU_FRONT'),
    ('tu',        'adjective',    '1',    None,         'back',        '+pass+part_past',    'PARTICIPLE_S|TU_BACK'),
    ('ty',        'adjective',    '1',    None,         'front',    '+pass+part_past',    'PARTICIPLE_S|TU_FRONT'),
    ('tu',        'adjective',    '1',    't:d',        'back',        '+pass+part_past',    'PARTICIPLE_TU_BACK'),
    ('ty',        'adjective',    '1',    't:d',        'front',    '+pass+part_past',    'PARTICIPLE_TU_FRONT'),
    ('ut',        'adjective',    '47',   None,        'back',        '',                'PARTICIPLE_N|UT_BACK'),
    ('yt',        'adjective',    '47',   None,        'front',    '',                'PARTICIPLE_N|UT_FRONT'),
    ('a',         'adjective',    '10',   None,        'back',        '',                    'PARTICIPLE_V|A_BACK'),
    ('ä',         'adjective',    '10',   None,        'front',    '',                    'PARTICIPLE_V|A_FRONT'),
    ('a',         'noun|adjective',         '10',   None,        'back',        '',                    'PARTICIPLE_M|A_BACK'),
    ('ä',         'noun|adjective',         '10',   None,        'front',    '',                    'PARTICIPLE_M|A_FRONT'),
    ('maton',     'adjective',    '34',   'tt:t',      'back',        '+part_maton',        'PARTICIPLE_MATON_BACK'),
    ('mätön',     'adjective',    '34',   'tt:t',      'front',    '+part_maton',        'PARTICIPLE_MATON_FRONT'),
    ('minen',     'noun',         '38',   None,        'back',        '+inf4',                    'INFINITIVE_MINEN_BACK'),
    ('minen',     'noun',         '38',   None,        'front',    '+inf4',                    'INFINITIVE_MINEN_FRONT'),

    ('jä', 'noun', '12', '', 'front', '+deriv_agent', 'DERIV_AGENT_IJA_FRONT'),
    ('ja', 'noun', '12', '', 'back', '+deriv_agent', 'DERIV_AGENT_IJA_BACK'),
    ('jä', 'noun', '10', '', 'front', '+deriv_agent', 'DERIV_AGENT_AJA_FRONT'),
    ('ja', 'noun', '10', '', 'back', '+deriv_agent', 'DERIV_AGENT_AJA_BACK'),

    ('us',       'noun',    '39',   '',        'back',        '+deriv_action',        'DERIV_ACTION_US_BACK'),
    ('ys',       'noun',    '39',   '',        'front',        '+deriv_action',        'DERIV_ACTION_YS_FRONT'),
    ('nti', 'noun', '5', 'nt:nn', 'back', '+deriv_action', 'DERIV_ACTION_NTI_BACK'),
    ('nti', 'noun', '5', 'nt:nn', 'front', '+deriv_action', 'DERIV_ACTION_NTI_FRONT'),
    ('nta', 'noun', '9', 'nt:nn', 'back', '+deriv_action', 'DERIV_ACTION_NTA_BACK'),
    ('ntä', 'noun', '9', 'nt:nn', 'front', '+deriv_action', 'DERIV_ACTION_NTÄ_FRONT'),
    ('na', 'noun', '2', '', 'back', '+deriv_action', 'DERIV_ACTION_NA_BACK'),
    ('nä', 'noun', '2', '', 'front', '+deriv_action', 'DERIV_ACTION_NÄ_FRONT'),

    # No way I am handling gradation with these
    ('u', 'noun', '2', '', 'back', '+deriv_action+sg+nom', 'DERIV_ACTION_U_BACK'),
    ('y', 'noun', '2', '', 'front', '+deriv_action+sg+nom', 'DERIV_ACTION_Y_FRONT'),
    ('o', 'noun', '1', '', 'back', '+deriv_action+sg+nom', 'DERIV_ACTION_O_BACK'),
    ('o', 'noun', '1', '', 'front', '+deriv_action+sg+nom', 'DERIV_ACTION_Ö_FRONT'),

    # ('ton',     'adjective',    '34',   'tt:t',        'back',        '+deriv_ton',        'DERIV_TON_BACK'),
    # ('tön',     'adjective',    '34',   'tt:t',        'front',    '+deriv_ton',        'DERIV_TON_FRONT'),

    # TODO:
    #   * adjective + -sti
    #   * adjective + -uus/-yys
    #   * noun + -ton/-tön

]