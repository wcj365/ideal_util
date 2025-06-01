#!/usr/bin/env python3

import uuid
from datetime import datetime
from pytz import timezone
import re
import pandas as pd
import streamlit as st

from ideal_util.common import ideal_config


STRING_OPERATORS = [
    "Includes", 
    "Excludes",
    "Contains",
#    "Starts with",
#    "Ends with"
]

COMPARISON_OPERATORS =  ["=", ">", "<", ">=", "<="] 

RANKING_OPERATORS = ["top", "bottom"]


def filter(df_src, filter_key=0, default_columns=[], required_columns=[]): 
#     if default_columns == None:
#         default = list(df.columns)
#     elif default_columns == []:
#         if required_columns == []:
#             default =list(df.columns)
#         else:
#             default = required_columns
#     else:
#         default = default_columns
        
#     selected_columns = st.multiselect("Select Columns for Display", list(df.columns), default=default)
    
#     if len(set(required_columns).intersection(set(selected_columns))) < len(required_columns):
#         st.error(f"The following columns are required: {required_columns}", icon=error_icon)
#         return pd.DataFrame()
    df = df_src.copy()
    df_columns = df.dtypes.to_frame().reset_index()
    df_columns.columns = ["column_name", "column_type"]
    df_columns["column_name"] = df_columns["column_name"].astype(str)
    type_dict = dict(zip(df_columns['column_name'], df_columns['column_type']))
    field_list = df_columns["column_name"].tolist()
    field_list.sort()

    def add_field():
        st.session_state.explorer_fields_size += 1

    if "explorer_fields_size" not in st.session_state:
        st.session_state.explorer_fields_size = 0
        st.session_state.explorer_fields = []
    elif st.session_state.explorer_fields_size > 0:
        columns = st.columns((2,1,3))
        with columns[0]:
            st.text("Filter By")
        with columns[1]:
            st.text("Operator")
        with columns[2]:
            st.text("Value")

    for i in range(st.session_state.explorer_fields_size):
            
        columns = st.columns((2,1,3))
        with columns[0]:
            field_name = st.selectbox(
                f"Column {i}", 
                field_list, 
                index=None,
                label_visibility="collapsed",
    #            key=f"filter_{filter_key}"
            )
            
        if field_name == None:
            pass
        elif type_dict[field_name] == "bool":
            df = boolean_filter(df, columns, field_name, i)
        elif type_dict[field_name] in ["object", "category"]:
            df = string_filter(df, columns, field_name, i)
        elif type_dict[field_name] in ["int64", "float64"]:
            df = numeric_filter(df, columns, field_name, i)
        elif type_dict[field_name] == "datetime64[ns]":
            df = date_filter(df, columns, field_name, i)
        else:    ## not possible
            st.error(f"Error occured: the data type {type_dict[field_name]} is not supported.", icon=ideal_config.ERROR_ICON)
    
    st.button("➕ Add Filter", on_click=add_field, key=uuid.uuid4().hex) 
               
    return df    
#    return df[selected_columns]
                                                                      
        
def boolean_filter(df, columns, field_name, i):

    with columns[1]:
        operator = st.selectbox(
            f"Operator {i}", 
            ["Equals"],
            index=0,
            label_visibility="collapsed",
            disabled=True
        )  
        
    with columns[2]:             
        field_value  = st.selectbox(      
            f"Values {i}",
            [True, False],
            label_visibility="collapsed"
        ) 
        
    return df[df[field_name] == field_value]

def string_filter(df, columns, field_name, i):
    
    with columns[1]:
        operator = st.selectbox(
            f"Operator {i}", 
            STRING_OPERATORS,
            label_visibility="collapsed"
        ) 

    with columns[2]:
       
        value_options = list(df[field_name].unique())
#        value_options.sort()   error when there is missing value
        
        if operator in ["Includes", "Excludes"]:
            field_value  = st.multiselect(
                f"Values {i}", 
                value_options, 
                label_visibility="collapsed"
            )
            if len(field_value) > 0:
                df = category_filter_cached(df, field_name, operator, field_value)
        else:
            field_value  = st.text_input(
                f"Values {i}", 
                label_visibility="collapsed"
            )
            if field_value != None and field_value.strip() != "":
                df = text_filter_cached(df, field_name, operator, field_value)
                
    return df


@st.cache_data
def category_filter_cached(df, field_name, operator, field_value):
    
    if operator == "Includes":
        query = f'`{field_name}` in {field_value}'
    else:
        query = f'`{field_name}` not in {field_value}'

    df.query(query, inplace=True)
                
    return df


@st.cache_data
def text_filter_cached(df, field_name, operator, field_value):
    
    df = df[df[field_name].str.contains(field_value)]   
    df = df[df[field_name].str.contains(field_value)]
                
    return df


def numeric_filter(df, columns, field_name, i):
             
    COMPARE_OPERATORS =  ["==", ">", "<", ">=", "<="] 
    RANK_OPERATORS = ["top", "bottom"]
    
    with columns[1]:
        operator = st.selectbox(
            f"Operator {i}", 
            COMPARE_OPERATORS + RANK_OPERATORS,
            label_visibility="collapsed"
        ) 
        
    if operator in COMPARE_OPERATORS:
        with columns[2]:                 
            field_value  = st.number_input(
                f"Values {i}", 
                label_visibility="collapsed"
            )
        df = compare_filter_cached(df, field_name, operator, field_value)     
    else:            
        with columns[2]:                 
            field_value  = st.number_input(
                f"Values {i}", 
                min_value= 1, step=1, value=10,
                label_visibility="collapsed"
            )
        df = rank_filter_cached(df, field_name, operator, field_value)

    return df              


@st.cache_data
def compare_filter_cached(df, field_name, operator, field_value):
    
    query = f"`{field_name}` {operator} {field_value}"
    print(query)
    
    df.query(query, inplace=True) 
    
     
    
    return df


@st.cache_data
def rank_filter_cached(df, field_name, operator, field_value):

    if operator == "top":
        df = df.sort_values(by=f'{field_name}', ascending=False).head(field_value)   
    else:
        df = df.sort_values(by=f'{field_name}', ascending=True).head(field_value)
    
    return df


def date_filter(df, columns, field_name, i):
        
    DATE_OPERATORS =  ["==", ">", "<", ">=", "<="] 
    
    with columns[1]:
        operator = st.selectbox(
            f"Operator {i}", 
            DATE_OPERATORS,
            label_visibility="collapsed"
        ) 

    with columns[2]:                 
        field_value  = st.date_input(
            f"Values {i}", 
            format="YYYY-MM-DD",
            label_visibility="collapsed"
        )

    if field_value != None:
        df = date_filter_cached(df, field_name, operator, field_value)
                
    return df


@st.cache_data
def date_filter_cached(df, field_name, operator, field_value):
    
    df[f'_DATE_{field_name}'] = df[field_name].dt.normalize()
    date_filter = pd.to_datetime(field_value).date()
    query = f"_DATE_{field_name} {operator} '{date_filter}'"
    df.query(query, inplace=True) 
    
    return df
