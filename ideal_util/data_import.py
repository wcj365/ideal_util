#!/usr/bin/env python3

import os
import pandas as pd  
import streamlit as st

from ideal_util.common import ideal_config, ideal_ui, ideal_server, file_uploader

# get the directory of the current script
script_dir = os.path.dirname(__file__)
example_file = f"{script_dir}/example_data/Wealth_vs_Health.xlsx"


def load_data():

    OPTIONS = [
        "Upload Data File",
        "Use Example Data"
    ]

    option = st.radio("Select an option", OPTIONS, index=0, horizontal=True, label_visibility="collapsed")

    if option == OPTIONS[0]:
        try:
            file, file_name = file_uploader.upload(["txt", "csv", "xlsx", "parquet"])
            if file is None:
                df = pd.DataFrame()
                file_name = None
            else:
                df, file_name = ideal_ui.create_dataframe(file, file_name)
        except Exception as err:
            print(err)
            st.error(err, icon=ideal_config.ERROR_ICON)
            df = pd.DataFrame()
            file_name = None
    else:
        df = ideal_server.read_excel_cache(example_file)
        file_name = example_file.split("/")[-1]  
        st.markdown(f"**{file_name}** - Wealth and health indicators for all countries from 2005 to 2024 (Source: The World Bank).")     

    if not df.empty:
        ideal_ui.display_dataframe(df)

    return df, file_name