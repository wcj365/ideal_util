#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

from gao_st.common import ideal_server, ideal_config
from gao_st.data_viz import viz_utils


def bar(df):
   
    column_types =ideal_server.get_column_types(df)

    x = st.sidebar.selectbox("X Axis", column_types["ALL"], index=None) 
    y = st.sidebar.selectbox("Y Axis", column_types["ALL"], index=None)  

    color, showlegend, orientation, title, height = viz_utils.common_params(column_types["ALL"], f"{x} vs {y}") 

    if x != None and y != None:  
        fig = create_bar(df, x, y, color, showlegend, orientation, title, height)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", config=ideal_config.PLOTLY_CONFIG) 
        

@st.cache_data
def create_bar(df, x, y, color=None, showlegend=True, orientation=None, title=None, height=None):

    fig = px.bar(
        df, 
        x=x,
        y=y,
        title=title if title != None else None,
        color=color if color != None else None
    )  
    
    fig.update_xaxes(categoryorder="total descending")
    fig.update_yaxes(categoryorder="total ascending")

    fig.update_layout(showlegend=showlegend)  

    if orientation != None:
        fig.update_layout(legend=dict(orientation=orientation))
    
    if height != None:
        fig.update_layout(height=height)

    return fig