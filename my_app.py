import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import plotly.express as px
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import ipyvizzu as iz


st.set_page_config(layout='wide',page_title='World Cup Analysis')

# Custom CSS
st.markdown(
    """<style>
            footer {
            visibility: hidden;
      } </style>""",
    unsafe_allow_html=True
)

def data_upload():
    bat = pd.read_csv("dataset/batting_records.csv")
    bowl = pd.read_csv("dataset/bowling_records.csv")
    return bat,bowl

bat,bowl = data_upload()

st.title("World Cup Analysis :trophy:")


records_box = st.sidebar.selectbox("Select Records",["Batting Records","Bowling Records"])

if records_box == 'Batting Records':
    # KPI's
    total_matches = int(bat['mat'].sum())
    total_centuries = int(bat['100'].sum())
    total_sixes = int(bat['6s'].sum())
    total_fours = int(bat['4s'].sum())
    total_ducks = int(bat['0'].sum())

    first_col,sec_col,third_col,fourth_col,fifth_col = st.columns(5)
    
    with first_col:
        st.subheader("Total Matches:")
        st.subheader(total_matches)

    with sec_col:
        st.subheader("Total Centuries:")
        st.subheader(total_centuries)

    with third_col:
        st.subheader("Total Sixes:")
        st.subheader(total_sixes)

    with fourth_col:
        st.subheader("Total Fours:")
        st.subheader(total_fours)

    with fifth_col:
        st.subheader("Total Ducks:")
        st.subheader(total_ducks)
    
    

    # AgGrid Table
    st.markdown("---")
    gd = GridOptionsBuilder.from_dataframe(bat)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True,groupable=True)
    gridoptions = gd.build() 
    AgGrid(bat,gridOptions=gridoptions,height=500,enable_quicksearch=True)

    
    
    # Bar Chart
    st.markdown("---")
    
    st.subheader("Top 10 players with most number of matches")
    match_counts = bat.groupby('player')[['mat','inns']].sum().sort_values('mat',ascending=False).head(10)
        
    match_fig = px.bar(match_counts,x=match_counts.index,y='mat',
                        color='inns',height=450,width=1100,barmode='group')
        
    st.plotly_chart(match_fig,use_container_width=True)

    st.subheader("Runs scored with respect to years")
    span_matches = bat.groupby('span')[['mat']].sum()
    span_graph = px.line(span_matches, x=span_matches.index,y='mat',markers=True)
    st.plotly_chart(span_graph,use_container_width=True)

    

if records_box == 'Bowling Records':
    gd = GridOptionsBuilder.from_dataframe(bowl)
    gd.configure_grid_options(alwaysShowHorizontalScroll=True)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True,groupable=True)
    gridoptions = gd.build()
    AgGrid(bowl,enable_quicksearch=True,height=500,gridOptions=gridoptions)



    

