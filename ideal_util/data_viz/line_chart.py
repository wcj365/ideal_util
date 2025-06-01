#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

from gao_st.common import ideal_server, ideal_config
from gao_st.data_viz import viz_utils


@st.cache_data
def create_line(df, x, y, color=None, showlegend=True, orientation=None, title=None, height=None):
    fig = px.line(
        df.sort_values(by=[x]),     # We must sort the X, otherwise, the line will be wierd.
        title=title,
        x=x,
        y=y,
        color=color
    )

    fig.update_layout(showlegend=showlegend)  
    fig.update_layout(legend=dict(orientation=orientation))    
    fig.update_layout(height=height)    

    return fig


def line(df):   
    num_cols, cat_cols =ideal_server.get_num_cat_columns(df)
    x = st.sidebar.selectbox("X Axis", cat_cols + num_cols, index=None) 
    y = st.sidebar.selectbox("Y Axis", num_cols, index=None)  
    color, showlegend, orientation, title, height = viz_utils.common_params(cat_cols, f"{x} vs {y}") 

    if x != None and y != None:  
        fig = create_line(df, x, y, color, showlegend, orientation, title, height)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", config=ideal_config.PLOTLY_CONFIG) 