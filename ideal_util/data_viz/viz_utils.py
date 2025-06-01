#!/usr/bin/env python3

import streamlit as st


def common_params(color_columns, title):

    color = st.sidebar.selectbox(
        "Color by", 
        color_columns, 
        index=None
    )                                     

    if color != None:
        showlegend = st.sidebar.checkbox("Show Color Legend")  
    else:
        showlegend = False

    if showlegend:
        orientation = st.sidebar.selectbox("Legend Orientation", ["vertical", "horizontal"])
        orientation = "h" if orientation == "horizontal" else "v"
    else:
        orientation = None 

    title = st.sidebar.text_input("Title", value=title)    
    height = st.sidebar.number_input("Height (px)", min_value=100, max_value=None, value=800, step=10)

    return color, showlegend, orientation, title, height