#!/usr/local/env Python3

import io
import os
from datetime import datetime
from pytz import timezone
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import streamlit as st

from gao_st.common import ideal_config

        
@st.cache_data
def to_excel_bytes(df_cover, df_params, df_data):
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        if not df_cover.empty:
            df_cover.to_excel(writer, sheet_name="Cover Sheet", index=False)
        if not df_params.empty:
            df_params.to_excel(writer, sheet_name="Input Parameters", index=False)
        df_data.to_excel(writer, sheet_name="Output Data", index=False)
        
    return buffer

        
@st.cache_data
def to_excel_file(df_cover, df_params, df_data, input_folder, file_name):   
    with pd.ExcelWriter(f"{input_folder}/{file_name}.xlsx") as writer:
        if not df_cover.empty:
            df_cover.to_excel(writer, sheet_name="Cover Sheet", index=False)
        if not df_params.empty:
            df_params.to_excel(writer, sheet_name="Input Parameters", index=False)
        df_data.to_excel(writer, sheet_name="Output Data", index=False)


#@st.cache_data
def save_dataframe(df, file_format, input_folder, file_name):
    if file_format == "csv":
        to_csv(df, f"{input_folder}/{file_name}.csv", False)
    elif file_format == "xlsx":
        to_excel(df, f"{input_folder}/{file_name}.xlsx", False)    
    else:
        to_parquet(df, f"{input_folder}/{file_name}.parquet", preserve_index=False)
        

@st.cache_data
def read_csv_cache(file, skiprows, skipfooter, sep):
    return pd.read_csv(file, parse_dates=True, skiprows=skiprows, skipfooter=skipfooter, sep=sep)


def read_csv(file, skiprows, skipfooter, sep):
    return pd.read_csv(file, parse_dates=True, skiprows=skiprows, skipfooter=skipfooter, sep=sep)


@st.cache_data
def to_csv(df, file_path, preserve_index):
    return df.to_csv(file_path, index=preserve_index)


@st.cache_data
def read_excel_cache(file, sheet_name=0, skiprows=0, skipfooter=0):
    return pd.read_excel(file, parse_dates=True, sheet_name=sheet_name, skiprows=skiprows, skipfooter=skipfooter)


def read_excel(file, sheet_name, skiprows, skipfooter):
    return pd.read_excel(file, parse_dates=True, sheet_name=sheet_name, skiprows=skiprows, skipfooter=skipfooter)


@st.cache_data
def to_excel_old(df, file_path, preserve_index):
    return df.to_excel(file_path, index=preserve_index)

@st.cache_data
def to_excel(df, file_path, preserve_index):
    return df.to_excel(file_path, index=preserve_index)

@st.cache_data
def read_parquet_cache(file):
    table = pq.read_table(file)
    return table.to_pandas()


def read_parquet(file):
    table = pq.read_table(file)
    return table.to_pandas()


@st.cache_data
def to_parquet(df, file_path, preserve_index):
    table = pa.Table.from_pandas(df, preserve_index=preserve_index)
    pq.write_table(table, file_path)   
    

def get_us_eastern_datetime_string():
    return datetime.now().astimezone(timezone('US/Eastern')).strftime("%Y-%m-%d_%H:%M:%S")


def get_column_types(df):
    
    df_columns = df.dtypes.to_frame().reset_index()
    df_columns.columns = ["Column_Name", "Column_Type"]
    df_string_columns = df_columns[(df_columns["Column_Type"] == "object") | (df_columns["Column_Type"] == "category") ]
#        df_string_columns = df_columns[df_columns["Column_Type"].isin(["object", "category"])] WHY doe this not work?
    df_datetime_columns = df_columns[df_columns["Column_Type"] == 'datetime64[ns]']
    df_int_columns = df_columns[df_columns["Column_Type"] == 'int64'] 
    df_float_columns = df_columns[df_columns["Column_Type"] == 'float64']  
    df_bool_columns = df_columns[df_columns["Column_Type"] == 'bool'] 
    
    column_types = {} 
    column_types["ALL"] =  list(df_columns["Column_Name"])
    column_types["STRING"] = list(df_string_columns["Column_Name"])
    column_types["DATETIME"] = list(df_datetime_columns["Column_Name"])
    column_types["INT"] = list(df_int_columns["Column_Name"])
    column_types["FLOAT"] = list(df_float_columns["Column_Name"])
    column_types["BOOL"] = list(df_bool_columns["Column_Name"])
      
    return column_types


def get_num_cat_columns(df):
    column_types = get_column_types(df)
    num_cols = column_types["INT"] + column_types["FLOAT"]
    cat_cols = list(set(column_types["ALL"]) - set(num_cols))
    return num_cols, cat_cols


def add_file_info(df, folder):
    df["Created (US/Eastern)"] = df["File Name"].apply(
        lambda x: datetime.fromtimestamp(os.path.getctime(f"{folder}/{x}")).astimezone(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M")
    )
    df["Size (KB)"] = df["File Name"].apply(lambda x: round(os.stat(f"{folder}/{x}").st_size / 1024))
    return df

