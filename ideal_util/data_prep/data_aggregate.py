#!/usr/bin/env python3

import pandas as pd
import streamlit as st

from ideal_util.common import ideal_config, ideal_ui, ideal_server


def aggregate(df):  

    df_agg = pd.DataFrame()      
    
    column_type_dict = ideal_server.get_column_types(df)
    group_by_options = column_type_dict["ALL"]
#    group_by_options = column_type_dict["STRING"] + column_type_dict["BOOL"] + column_type_dict["DATETIME"]
    group_by_options.sort()
    numeric_options = column_type_dict["INT"] + column_type_dict["FLOAT"]
    numeric_options.sort()
    
    group_by_fields = st.multiselect("Group By Columns", group_by_options)
    
    select_list = [] 
    
    if len(group_by_fields) > 0:
     
        columns = st.columns((1,3,1))
        with columns[0]:
            st.text("Aggregate Function")
        with columns[1]:
            st.text("Aggregate Columns")
        with columns[2]:
            st.text("Compute %")
            
        func_fields_dict = {}
        
        for func in ideal_config.AGG_FUNCTIONS:

            with columns[0]:
                st.selectbox(
                    "display for {func}", 
                    [func],
                    index=0,
                    label_visibility="collapsed"
                )
                
            if func == "count":
                agg_column_options = list(set(column_type_dict["ALL"]) - set(group_by_fields))
            else:
                agg_column_options = numeric_options 
                
            agg_column_options.sort()

            with columns[1]:
                fields = st.multiselect(
                    f"Columns for {func}",
                    agg_column_options,
                    label_visibility="collapsed"
                )
                
            with columns[2]:
                compute = st.selectbox(
                    f"Compute % {func}",
                    ["No", "Yes"],
                    label_visibility="collapsed"
                )                

            if len(fields) > 0:
                func_fields_dict[func] = (fields, compute)
                
        if func_fields_dict != {}:       
            df_agg =  aggregate_cache(df, group_by_fields, func_fields_dict)

    return df_agg
    
    
@st.cache_data
def aggregate_cache(df, group_columns, func_fields_dict):
    
    df_list = []     
    for agg_func, (agg_columns, compute) in func_fields_dict.items():
        df_agg = df.groupby(group_columns)[agg_columns].agg(agg_func)
        df_agg.columns = [f"{column}_{agg_func}" for column in agg_columns]
        if compute == "Yes":
            for column in agg_columns:
                df_agg[f"{column}_{agg_func}_%"] = 100 * df_agg[f"{column}_{agg_func}"] / df_agg[f"{column}_{agg_func}"].sum()
        df_list.append(df_agg)
    df = pd.concat(df_list, axis=1).reset_index()
    return df    


