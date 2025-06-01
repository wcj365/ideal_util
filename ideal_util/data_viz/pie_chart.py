#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

from ideal_util.common import ideal_server, ideal_config
from ideal_util.data_viz import viz_utils


def pie(df):
    
    num_cols, cat_cols =ideal_server.get_num_cat_columns(df)

    names = st.sidebar.selectbox("Group Column", cat_cols, index=None) 
    values = st.sidebar.selectbox("Value Column", num_cols, index=None) 

    hole = st.sidebar.number_input("Donut Hole Percent", min_value=0, max_value=100, step=1, value=25)
    hole = hole / 100

    textinfo = st.sidebar.multiselect("Display Text", ["percent", "value", "label"], default=["percent","value", "label"])     

    textposition = st.sidebar.selectbox("Text Position", ["inside", "outside"])
  
    color, showlegend, orientation, title, height = viz_utils.common_params(cat_cols, f"{values} by {names}") 

    if names != None and values != None: 
        fig = create_pie(df, names, values, hole, textinfo, textposition, color, showlegend, orientation, title, height)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", config=ideal_config.PLOTLY_CONFIG)     


@st.cache_data
def create_pie(df, names, values, hole=None, textinfo=None, textposition=None,  color=None, showlegend=None, orientation=None, title=None, height=None):

    fig = px.pie(
        df, 
        names=names,
        values=values,
        title=title if title != None else None,
        color=color if color != None else None,
        hole=hole
    )
    
    fig.update_traces(textposition=textposition, textinfo="+".join(textinfo))
        
    fig.update_xaxes(categoryorder="total descending")
    fig.update_yaxes(categoryorder="total ascending")

    fig.update_layout(showlegend=showlegend)  
    fig.update_layout(legend=dict(orientation=orientation))    
    fig.update_layout(height=height)    

    return fig  
