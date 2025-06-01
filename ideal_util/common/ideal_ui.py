#!/usr/local/env Python3

import uuid
import os
from PIL import Image
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import streamlit as st

from gao_st.common import ideal_config, ideal_server

def setup_page(page_icon, page_title):
  
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        menu_items={
            "About": "IDEAL 5.x  ",
            "Get Help": "mailto:wangc1@gao.gov",
        },
    )
    image = Image.open("./assets/images/ideal_logo.png")
    #st.image(image, capt.n='Interactive Data Exploration and Analysis Lab (IDEAL)', width=400)
    st.image(image, width=300) 
    
            # st.logo(
            #     "./assets/images/ideal_logo_no_words.png", 
            #     link=None, 
            #     icon_image="./assets/images/ideal_logo_no_words.png"
            # )
    
    st.write(f"## {page_title} {page_icon}")

                
def upload_dataset(i=0):
    file = st.file_uploader(
        "Upload", 
        type=ideal_config.DATA_FORMATS, 
        accept_multiple_files=False, 
        key=f"upload_dataset_{i}",
        label_visibility="collapsed"
    )

    if file == None:
        file_name = None 
        df = pd.DataFrame()
    else:
        file_name = file.name
        file_ext = file_name.rsplit(".")[-1].lower()
        df, file_name = create_dataframe(file, file_name, file_ext, i)
        
    return df, file_name


def create_dataframe(file, file_name, i=0):
    file_ext = file_name.split(".")[-1].lower()
    if file_ext == "parquet":
        df = ideal_server.read_parquet_cache(file)
    elif file_ext in ["csv", "txt", "xlsx"]:
        columns = st.columns(3)
        with columns[0]:
            skiprows = st.number_input("Skip First Rows", min_value=0, step=1, key=f"skiprows_{i}")
        with columns[1]:   
            skip_last_rows = st.number_input("Skip Last Rows", min_value=0, step=1, key=f"skip_last_rows_{i}")
        with columns[2]:
            if file_ext in ["csv","txt"]:
                delimiter = st.text_input(f"Delimiter", value=",", key=f"delimiter_{i}")
                df = ideal_server.read_csv_cache(file, skiprows=skiprows, skipfooter=skip_last_rows, sep=delimiter)
            elif file_ext == "xlsx":
                xls = pd.ExcelFile(file)
                sheet = st.selectbox(
                    "Worksheet", 
                    xls.sheet_names, 
                    index = None if len(xls.sheet_names) > 1 else 0, 
                    key=f"worksheet_{i}"
                )

                if sheet == None:
                    df = pd.DataFrame()
                    file_name = None
                else:
                    df = ideal_server.read_excel_cache(file, sheet_name=sheet, skiprows=skiprows, skipfooter=skip_last_rows)
                    file_name = sheet + "_" + file_name
            else:
                raise Exception(f"The file format {file_format} is not supported.")
                
        # Excel worksheet headers can have mutiple lines, so flatten them
        columns = []
        for column in df.columns:
            if type(column) == str:
                column = column.replace("\n", "")
            columns.append(column)
            
        df.columns = columns                    
                
    return df, file_name
    

def select_dataset(input_folder, i=0, use_cache=True):
    
    file_list = get_file_names(input_folder)
    if len(file_list) == 0:
        st.info("No datasets in your space. Go to My Space -> Data Ingest to import data first.", icon=ideal_config.INFO_ICON)
        df = pd.DataFrame()
        file_name = None
    else:
        
        if st.button("Refresh", key=f"Refresh {i}"):
            file_list = get_file_names(input_folder)

        full_name = st.selectbox(
            f"dataset {i}", 
            file_list, 
            index=None, 
            placeholder=f"Select a dataset",  
            label_visibility="collapsed")
        if full_name == None:
            file_name = None
            df = pd.DataFrame()
        else:
            file_name = full_name.split(".", maxsplit=1)[0]
            file_ext = full_name.split(".", maxsplit=1)[1]
            df, file_name = create_dataframe(f"{input_folder}/{file_name}.{file_ext}", file_name, file_ext, i)       

    return df, file_name           
  
    
def get_file_names(folder):
    file_list = os.listdir(folder)
    file_list = [file for file in file_list if file.rsplit(".")[-1].lower() in ideal_config.DATA_FORMATS]
    file_list.sort()
    return file_list


def display_data(df, i, display_mode, random_only=False):
              
    if display_mode == "data_only":
        display_dataframe(df, i, random_only)  
    elif display_mode == "stats_only":
        display_stats(df)
    elif display_mode == "both":
        tabs = st.tabs([":sunny: Data Table", ":sunny: Summary Statistics"])
        with tabs[0]: 
            display_dataframe(df, i, random_only) 
        with tabs[1]:
            display_stats(df)
    else:
        pass
        
        
def display_dataframe(df, i=0, sample_size=1000):
    pd.set_option("styler.render.max_elements", ideal_config.MAX_CELLS)
    col1, col2 = st.columns((3,1))
    with col1:
        st.markdown(f"Rows: `{df.shape[0]}`    Columns: `{df.shape[1]}`")
    if df.shape[0] * df.shape[1] <= ideal_config.MAX_CELLS:
        st.dataframe(df, use_container_width=True) 
    elif sample_size != None:
        st.info(f"Number of cells exceeds {ideal_config.MAX_CELLS}. Only a random sample of {sample_size} records is shown.", icon="ℹ️")
        st.dataframe(df.sample(sample_size), use_container_width=True)
    else: 
        st.info(f"Number of cells exceeds {ideal_config.MAX_CELLS}. Full table display is turned off.", icon="ℹ️")
        col1, col2 = st.columns(2)
        with col1:
            display = st.selectbox("Filter", ["Top", "Bottom", "Random"], key=f"{i}_select")
        with col2:
            count = st.number_input("Rows", min_value=5, step=5,  max_value=100, key=f"{i}_input")

        if display == "Top":
            st.dataframe(df.head(count), use_container_width=True)
        elif display == "Bottom":
            st.dataframe(df.tail(count), use_container_width=True)                                            
        else:
            st.dataframe(df.sample(count), use_container_width=True)

               
def display_stats(df):
    
    column_type_dict = ideal_server.get_column_types(df)

    if len(column_type_dict["INT"]) > 0 or len(column_type_dict["FLOAT"]) > 0 :
        st.write("###### Numeric Columns")
        st.dataframe(get_df_stats_numeric(df), use_container_width=True)
        
    if len(column_type_dict["STRING"]) > 0 :
        st.write("###### String Columns")
        st.dataframe(get_df_stats_string(df), use_container_width=True)        
        
    if len(column_type_dict["BOOL"]) > 0 :
        st.write("###### Boolean Columns")
        st.dataframe(get_df_stats_bool(df), use_container_width=True)
        
    if len(column_type_dict["DATETIME"]) > 0: 
        st.write("###### Datetime Columns")
        st.dataframe(get_df_stats_datetime(df), use_container_width=True)


@st.cache_data
def get_df_stats_numeric(df):    
    return df.describe(include=[np.number]).T


@st.cache_data
def get_df_stats_string(df):    
    return df.describe(include=[object]).T


@st.cache_data
def get_df_stats_bool(df):    
    return df.describe(include=[bool]).T


@st.cache_data
def get_df_stats_datetime(df):    
    return df.describe(include=[np.datetime64]).T

        
def download_dataframe(df, file_name):
              
    columns = st.columns((3,1,1))
    with columns[0]:
        file_name = st.text_input("File Name", value=file_name) 
        if file_name.strip() == "":
            st.warning("Please enter file name." , icon="⚠️")
        else:
            file_name = "_".join(file_name.strip().split(" "))
    with columns[1]:
        file_format = st.selectbox("File Format", ideal_config.SAVE_DATA_FORMATS) 
        if file_format == "csv":
            mime_type = "text/csv"
        else:
            mime_type = "application/octet-stream" 
    with columns[2]:
        downloaded = st.download_button(
            label="Download",
            data=convert_df(df, file_format),
            file_name=f"{file_name}.{file_format}",
            mime=mime_type,
            type="primary"
#            on_click=convert_df, 
#            args=(df, file_format)
        )
        
    if downloaded:
        st.info("The dataset was downloaded successfully.", icon=ideal_config.INFO_ICON)
            
        
@st.cache_data
def convert_df(df, file_format):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    if file_format == "csv":
        return df.to_csv().encode('utf-8')
    elif file_format == "parquet":
        return df.to_parquet() 
    else:
        raise Exception(f"The file format {file_format} is not support.")


def download_as_excel(df_cover, df_params, df_data, file_name):
    
    downloaded = st.download_button(
        label="Download",
        data=ideal_server.to_excel_bytes(df_cover, df_params, df_data),
        file_name=f"{file_name}.xlsx",
        mime="application/octet-stream",
        type="primary"
#            on_click=convert_df, 
#            args=(df, file_format)
    )      
    if downloaded:
        st.info("The dataset was downloaded successfully.", icon=ideal_config.SUCCESS_ICON)
        
        
def show_details(df, key="default"):
    _df = df.copy()
    
    col1, col2 = st.columns((3,1))
    with col1:
        st.markdown(f"Rows: `{df.shape[0]}`    Columns: `{df.shape[1]}`")
        
    event = st.dataframe(
        _df,
        key="editor_" + key,
        on_select="rerun",
        selection_mode=["multi-row"],
        use_container_width=True
    )
    
    if st.button("Display Selected Rows", key="show_" + key):
        indexes = event.selection["rows"]
        if len(indexes) == 0:
            st.warning("Please select one or more rows.", icon=ideal_config.WARNING_ICON)
        else:
            details_dialog(_df.iloc[indexes])     

#@st.dialog("Show Row Details", width="large")
def details_dialog(df):
    st.table(df.T)

    