class SqlQueries:
       

    data_clean_addrl = ("""
        DELETE 
        FROM dim_i94addrl_table
        WHERE addr_value = 'All Other Codes'
    """)

    data_clean_cntyl = ("""
        DELETE 
        FROM dim_i94cntyl_table
        WHERE (cnty_value LIKE '%No Country Code%' OR cnty_value LIKE '%Collapsed%' OR cnty_value LIKE '%INVALID%') 
    """)

    data_clean_prtl = ("""
        DELETE 
        FROM dim_i94prtl_table
        WHERE (prt_value LIKE '%No PORT Code%' OR prt_value LIKE '%Collapsed%') 
    """)

    data_clean_fact = ("""
        DELETE 
        FROM fact_immigration
        WHERE gender NOT IN ('M','F') 
    """)

    addrl_table_count_check = ("""
        SELECT count(*)  
        FROM dim_i94addrl_table
    """)

    cntyl_table_count_check = ("""
        SELECT count(*)  
        FROM dim_i94cntyl_table
    """)

    prtl_table_count_check = ("""
        SELECT count(*)  
        FROM dim_i94prtl_table
    """)

    model_table_count_check = ("""
        SELECT count(*)  
        FROM dim_i94model_table
    """)

    visal_table_count_check = ("""
        SELECT count(*)  
        FROM dim_i94visal_table
    """)

    fact_table_count_check = ("""
        SELECT count(*)  
        FROM fact_immigration
    """)

    demographics_table_count_check = ("""
        SELECT count(*)  
        FROM dim_demographics_table
    """)