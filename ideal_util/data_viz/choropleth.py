#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

from gao_st.common import ideal_server, ideal_config
from gao_st.data_viz import viz_utils

SCOPE = ['world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america']

@st.cache_data
def create_choropleth(df, location, scope, color, title, height):
        
    fig = px.choropleth(
        df,
        title=title,
        locations=location,
        scope=scope,
        color=color,
        height=height
    )
   
    fig.update_layout(height=height)    

    return fig


def choropleth(df):   
    column_types =ideal_server.get_column_types(df)

    location = st.sidebar.selectbox("Location", column_types["STRING"], index=None) 
    scope = st.sidebar.selectbox("Scope", SCOPE, index=None) 
    color = st.sidebar.selectbox("Color", column_types["INT"] + column_types["FLOAT"], index=None) 
    title = f"Choropleth of {color}" 
    height = st.sidebar.number_input("Height (px)", min_value=100, max_value=None, value=800, step=10)

    if  location != None and scope != None and color != None:   
        fig = create_choropleth(df, location, scope, color, title, height)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", config=ideal_config.PLOTLY_CONFIG) 

               
