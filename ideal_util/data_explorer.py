#!/usr/bin/env python3

import streamlit as st

from ideal_util.common import ideal_config as config
from ideal_util.common import ideal_ui
from ideal_util.data_viz import histogram, boxplot, bar_chart, pie_chart, line_chart, scatter_plot, choropleth
from ideal_util.data_prep import data_filter, data_aggregate
from ideal_util import univariate

CHARTS = [
    "Histogram",
    "Boxplot",
    "Bar Chart", 
    "Pie Chart", 
    "Line Chart",
    "Scatter Plot",
    "Choropleth"
]


def explore(
    df_in, 
    display=True,
    select_cols=True,
    filter_rows=True,
    summ_stats=False,
    explore_var=True,
    aggregate=True,
    visualize=True
):

    df = df_in.copy()

    if display:
        with st.expander(f"{config.EXPANDER_ICON} DISPLAY DATA", expanded=True):
            ideal_ui.display_dataframe(df)

    if select_cols:
        with st.expander(":sunny: SELECT COLUMNS", expanded=False):
            columns = st.multiselect(
                "Select columns", 
                list(df.columns), 
                default=list(df.columns), 
                label_visibility="collapsed"
            )
            df = df[columns]

    if filter_rows:
        with st.expander(f"{config.EXPANDER_ICON} FILTER ROWS", expanded=False):
            df = data_filter.filter(df)   
            if df.shape[0] < df_in.shape[0]:      
                ideal_ui.display_dataframe(df)

    if summ_stats:
        with st.expander(f"{config.EXPANDER_ICON} SUMMARY STATISTICS", expanded=False):
            ideal_ui.display_stats(df)

    if explore_var:
        with st.expander(f"{config.EXPANDER_ICON} EXPLORE VARIABLES", expanded=False):
            univariate.explore(df)

    if aggregate:
        with st.expander(f"{config.EXPANDER_ICON} AGGREGATE DATA", expanded=False):
            df_agg = data_aggregate.aggregate(df)
            if not df_agg.empty:
                ideal_ui.display_dataframe(df_agg)
                df = df_agg

    if visualize:
        with st.expander(f"{config.EXPANDER_ICON} VISUALIZE DATA", expanded=True):
            cols = st.columns((1,2))
            with cols[0]:
                chart = st.selectbox("Chart Type", CHARTS, placeholder="Choose a chart type", index=None, label_visibility="collapsed")
            if chart != None:
                with cols[1]:
                    st.info("Use the left panel to enter parameters.", icon=config.INFO_ICON)

            if chart == "Histogram":
                histogram.histo(df)
            elif chart == "Boxplot":
                boxplot.box(df)
            elif chart == "Bar Chart":
                bar_chart.bar(df)
            elif chart == "Pie Chart":
                pie_chart.pie(df)
            elif chart == "Line Chart":
                line_chart.line(df)
            elif chart == "Scatter Plot":
                scatter_plot.scatter(df)
            elif chart == "Choropleth":
                choropleth.choropleth(df)