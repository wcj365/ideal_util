#!/usr/bin/env python3

import pandas as pd    
import plotly.express as px
import streamlit as st

from gao_st.common import ideal_config, ideal_ui

CATEGORICAL = ["string", "object", "category"]
NUMERICAL = ["int64", "float64"]

def explore(df_in):
    df = df_in.copy()
    COL_TYPES = ["Numerical Columns", "Categorical Columns"]
    cols = st.columns(3)
    with cols[0]:
        col_type = st.selectbox("Column Type", COL_TYPES, placeholder="Select column type", label_visibility="collapsed")
        
    if col_type == COL_TYPES[0]:
        columns = df.select_dtypes(include=['number']).columns
    else:
        columns =  df.select_dtypes(exclude=['number']).columns

    with cols[1]:
        column = st.selectbox("Select a column", columns, index=None, placeholder="Select column", label_visibility="collapsed")

    if column != None:
        with cols[2]:
            if df[column].dtype in CATEGORICAL:
                convert = st.checkbox("Convert to Number") 
            elif df[column].dtype in NUMERICAL:
                convert = st.checkbox("Convert to Category")                 

        if convert:
            try:
                df = convert_column(df, column)                 
            except Exception as err:
                st.error(f"ERROR: {err}", icon=ideal_config.ERROR_ICON)  

        univariate_exploration(df, column)

            
def univariate_exploration(df, column): 
    
    if df[column].dtype in CATEGORICAL:   
        df_counts, fig_bar, fig_pie = value_counts(df, column)
        tabs = st.tabs(["🌼 Frequency Table", "🌼 Bar Chart", "🌼 Pie Chart"])
        with tabs[0]:
            st.markdown(f"Categories: `{df_counts.shape[0]}`")
            st.dataframe(df_counts, use_container_width=True)
        
        with tabs[1]:
            st.plotly_chart(
                fig_bar, 
                use_container_width=True, 
                theme="streamlit", 
                config=ideal_config.PLOTLY_CONFIG
            )  
            
        with tabs[2]:
            st.plotly_chart(
                fig_pie, 
                use_container_width=True, 
                theme="streamlit", 
                config=ideal_config.PLOTLY_CONFIG
            )  

    elif df[column].dtype in NUMERICAL:

        fig_hist, fig_box = summary_stats(df, column)

        tabs = st.tabs(["🌼 Summary Statistics", "🌼 Histogram", "🌼 Boxplot"])
        
        with tabs[0]:
            st.dataframe(df[column].describe(), use_container_width=True)

        with tabs[1]:
            st.plotly_chart(
                fig_hist, 
                use_container_width=True, 
                theme="streamlit", 
                config=ideal_config.PLOTLY_CONFIG
            )  
            
        with tabs[2]:
            st.plotly_chart(
                fig_box,    
                use_container_width=True, 
                theme="streamlit", 
                config=ideal_config.PLOTLY_CONFIG
            )    


@st.cache_data
def convert_column(df, column):
    if df[column].dtype in CATEGORICAL:
        df[column] =  pd.to_numeric(df[column])
    elif df[column].dtype in NUMERICAL:
        df[column] = df[column].astype("string")  
    return df


@st.cache_data
def value_counts(df, column):
    df_counts = df[column].value_counts(dropna=False)  

    fig_bar = px.bar(
        df_counts.reset_index(),
        x="count",
        y=column,
        color=column,
    )
    fig_bar.update_layout(showlegend=False)

    fig_pie = px.pie(
        df_counts.reset_index(),
        values="count",
        names=column,
        color=column,
        hole=0.25
    )
    fig_pie.update_traces(textposition="inside", textinfo='label+percent+value')
    fig_pie.update_layout(showlegend=False)

    return df_counts, fig_bar, fig_pie


@st.cache_data
def summary_stats(df, column):
                
    fig_hist = px.histogram(
        df,
        x=column,
    )

    fig_box = px.box(
        df,
        x=column,
    )

    return fig_hist, fig_box