import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


# Custom CSS
st.markdown(
    """<style>
            footer {
            visibility: hidden;
      } </style>""",
    unsafe_allow_html=True
)

def data_upload():
    bat = pd.read_csv("batting_records.csv")
    bowl = pd.read_csv("dataset/bowling_records.csv")
    return bat,bowl

bat,bowl = data_upload()

st.title("World Cup Analysis :trophy:")


records_box = st.sidebar.selectbox("Select Records",["Batting Records","Bowling Records"])

if records_box == 'Batting Records':
    gd = GridOptionsBuilder.from_dataframe(bat)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True,groupable=True)
    gridoptions = gd.build() 
    AgGrid(bat,gridOptions=gridoptions,height=500,enable_quicksearch=True)

if records_box == 'Bowling Records':
    gd = GridOptionsBuilder.from_dataframe(bowl)
    gd.configure_grid_options(alwaysShowHorizontalScroll=True)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True,groupable=True)
    gridoptions = gd.build()
    AgGrid(bowl,enable_quicksearch=True,height=500,gridOptions=gridoptions)



    

