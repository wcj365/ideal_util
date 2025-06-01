#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

from ideal_util.common import ideal_server, ideal_config
from ideal_util.data_viz import viz_utils


@st.cache_data
def create_scatter(df, x, y, size=None, text=None, min_bubble=None, max_bubble=None, zero_sub=None, color=None, showlegend=True, orientation=None, title=None, height=None):
    _df = df.copy()   
    if size != None:
        size_list = df[size]
        minimum = size_list.min()
        if minimum <= 0:
            _df[size] = _df[size].apply(lambda x: x if x > 0 else zero_sub)

    fig = px.scatter(
        _df, 
        title=title,
        x=x,
        y=y,
        size=size,
        text=text,
        color=color
    )   


    if size != None:        

        marker = dict(
            sizeref=None if max_bubble == None else 2.*max(df[size])/(max_bubble**2),
            sizemin=min_bubble
        )

        fig.update_traces(marker=marker)

    fig.update_traces(textposition="top center")

    fig.update_layout(showlegend=showlegend)  
    fig.update_layout(legend=dict(orientation=orientation))    
    fig.update_layout(height=height)    

    return fig


def scatter(df):   
    num_cols, cat_cols =ideal_server.get_num_cat_columns(df)
    x = st.sidebar.selectbox("X Axis", num_cols, index=None) 
    if x != None:
        num_cols.remove(x)
        y = st.sidebar.selectbox("Y Axis", num_cols, index=None)  

        if y != None:
            num_cols.remove(y)
            text = st.sidebar.selectbox("Marker Text", cat_cols, index=None) 
            size = st.sidebar.selectbox("Marker Size", num_cols, index=None)  

            if size != None: 
                min_bubble = st.sidebar.number_input("Min Marker Size", min_value=1, value=5)
                max_bubble = st.sidebar.number_input("Max MArker Size", min_value=20, value=50)

                zero_sub = st.sidebar.text_input(
                    "Substitude Zero With", 
                    value="0.001", 
                    help="To be able to show a bubble for a point with zero value."
                )  
                try:
                    zero_sub = float(zero_sub)
                except:
                    st.sidebar.warning("Please enter a valid numeric number.", icon="⚠️") 
                    zero_sub = 0.001 
            else:
                min_bubble = None
                max_bubble = None
                zero_sub = None


    if x != None and y != None:  
        color, showlegend, orientation, title, height = viz_utils.common_params(cat_cols, f"{x} vs {y}") 
        fig = create_scatter(df, x, y, size, text, min_bubble, max_bubble, zero_sub, color, showlegend, orientation, title, height)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", config=ideal_config.PLOTLY_CONFIG) 