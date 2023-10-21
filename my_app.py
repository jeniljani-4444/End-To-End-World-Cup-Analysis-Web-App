import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="World Cup Analysis",
    page_icon=":trophy:",
    layout="wide"
)

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
    return bat, bowl


bat, bowl = data_upload()

st.title("World Cup Analysis :trophy:")


records_box = st.sidebar.selectbox(
    "Select Records", ["Batting Records", "Bowling Records"])

if records_box == 'Batting Records':
    # KPI's
    total_matches = int(bat['mat'].sum())
    total_centuries = int(bat['100'].sum())
    total_sixes = int(bat['6s'].sum())
    total_fours = int(bat['4s'].sum())
    total_ducks = int(bat['0'].sum())

    first_col, sec_col, third_col, fourth_col, fifth_col = st.columns(5)

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

    # AgGrid Table----------------------------------------------------
    st.markdown("---")
    gd = GridOptionsBuilder.from_dataframe(bat)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True, groupable=True)
    gridoptions = gd.build()
    AgGrid(bat, gridOptions=gridoptions, height=500, enable_quicksearch=True)

    # Bar Chart----------------------------------------------------
    st.markdown("---")
    st.subheader("Top 10 batsman with most number of matches")
    match_counts = bat.groupby('player')[['mat', 'inns']].sum(
    ).sort_values('mat', ascending=False).head(10)

    match_fig = px.bar(match_counts, x=match_counts.index, y='mat',
                       color='inns', height=450, width=1100, barmode='group',text_auto=True)

    st.plotly_chart(match_fig, use_container_width=True)

    # Line Chart----------------------------------------------------
    st.markdown('---')
    st.subheader("Runs scored with respect to years")
    span_matches = bat.groupby('span')[['runs']].sum()
    span_graph = px.line(span_matches, x=span_matches.index,
                         y='runs', markers=True)
    st.plotly_chart(span_graph, use_container_width=True)

    # donut chart for 4s and 6s----------------------------------------------------
    st.markdown('---')
    pie_col_first, pie_col_sec = st.columns(2)

    with pie_col_first:
        st.subheader('Top 5 five players with most number of 4s')
        fours_count = bat.groupby('player')[['4s']].sum(
        ).sort_values('4s', ascending=False).head()
        pie_chart_fours = px.pie(
            fours_count, names=fours_count.index, values='4s', hole=0.4)
        st.plotly_chart(pie_chart_fours, use_container_width=True)

    with pie_col_sec:
        st.subheader('Top 5 five players with most number of 6s')
        sixes_count = bat.groupby('player')[['6s']].sum(
        ).sort_values('6s', ascending=False).head()
        pie_chart_sixes = px.pie(
            sixes_count, names=sixes_count.index, values='6s', hole=0.4)
        st.plotly_chart(pie_chart_sixes, use_container_width=True)

    # donut chart for 100s and 50s----------------------------------------------------
    
    donut_col1, donut_col2 = st.columns(2)

    with donut_col1:
        st.subheader('Top 5 five players with most number of 100s')
        hund_counts = bat.groupby('player')[['100']].sum(
        ).sort_values('100', ascending=False).head()
        donut_chart_hund = px.pie(
            hund_counts, names=hund_counts.index, values='100', hole=0.4)
        st.plotly_chart(donut_chart_hund, use_container_width=True)

    with donut_col2:
        st.subheader('Top 5 five players with most number of 50s')
        fifty_counts = bat.groupby('player')[['50']].sum(
        ).sort_values('50', ascending=False).head()
        donut_chart_fifty = px.pie(
            fifty_counts, names=fifty_counts.index, values='50', hole=0.4)
        st.plotly_chart(donut_chart_fifty, use_container_width=True)

    # Tree Map----------------------------------------------------
    st.markdown('---')
    st.subheader("Runs scored by each batsman of that particular country")
    tree_map_plot = px.treemap(bat, path=[px.Constant("country"), 'country', 'player'], values='runs',
                               color='player', color_continuous_scale='RdBu',
                               )
    tree_map_plot.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(tree_map_plot, use_container_width=True)

    # Subplots----------------------------------------------------
    st.markdown("---")
    st.subheader("Top batsman with highest strike rate in world cup")
    first_df, sec_chart = st.columns(2)

    with first_df:
        top_five_sr = bat.groupby('player')[['player', 'country', 'mat', 'sr']].max(
        ).sort_values('sr', ascending=False).head(10).reset_index(drop=True)
        st.dataframe(top_five_sr)

    with sec_chart:
        sr_bar_chart = bat.groupby('player')[['player', 'country', 'sr']].max(
        ).sort_values('sr', ascending=False).head()
        sr_fig = px.bar(sr_bar_chart, x='player',
                        y='sr', height=400, width=500)
        st.plotly_chart(sr_fig, use_container_widht=True)

    # Not Out and High Score BarChart----------------------------------------------------
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Top 5 players with most no. of not outs')
        not_out_counts = bat.nlargest(n=5, columns='no')[
            ['player', 'country', 'no']]
        not_out_chart = px.bar(not_out_counts, x='no',
                               y='player', color='country')
        not_out_chart.update_layout(xaxis_title='Not Out Counts')
        st.plotly_chart(not_out_chart, use_container_width=True)

    with col2:
        st.subheader('Top 5 batsman with highest individual score')
        hs_counts = bat.nlargest(n=5, columns='hs')[
            ['player', 'country', 'hs']]
        hs_counts = px.bar(hs_counts, x='hs', y='player', color='country')
        hs_counts.update_layout(xaxis_title='High Score')
        st.plotly_chart(hs_counts, use_container_width=True)

    # Scatter Plot
    st.markdown('---')
    st.subheader('Average with respect to runs scored by players')
    scatter_plot = px.scatter(bat, x='runs', y='ave',
                              size='mat', color='country')
    scatter_plot.update_layout(xaxis_title='Runs', yaxis_title='Average')
    st.plotly_chart(scatter_plot, use_container_width=True)

if records_box == 'Bowling Records':
    # Bowling KPI's
    total_matches = int(bowl['mat'].sum())
    total_overs = int(bowl['overs'].sum())
    total_maidens = int(bowl['mdns'].sum())
    total_wickets = int(bowl['wkts'].sum())
    total_runs_conceded = int(bowl['runs'].sum())

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.subheader("Total Matches:")
        st.subheader(total_matches)
    with col2:
        st.subheader("Total Overs:")
        st.subheader(total_overs)
    with col3:
        st.subheader("Total Maidens:")
        st.subheader(total_maidens)
    with col4:
        st.subheader("Total Wickets:")
        st.subheader(total_wickets)
    with col5:
        st.subheader("Runs Conceded:")
        st.subheader(total_runs_conceded)

    gd = GridOptionsBuilder.from_dataframe(bowl)
    gd.configure_grid_options(alwaysShowHorizontalScroll=True)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True, groupable=True)
    gridoptions = gd.build()
    AgGrid(bowl, enable_quicksearch=True, height=500, gridOptions=gridoptions)

    # Bar Chart for matches-----------------------------------------------------------
    st.markdown('---')
    st.subheader('Top 10 bowlers with most number of matches')
    most_matches = bowl.nlargest(10,columns='mat')[['player','mat','inns','country']].sort_values('mat',ascending=True)
    color_scales = st.selectbox('Select color for bar chart',['viridis','sunsetdark','redor','rdpu','rdbu',
                                                              'ylgnbu','ylgn','algae','amp','ice','matter','solar','haline','thermal','icefire'])
    fig = px.bar(most_matches,x='player',y='mat',hover_data='country',text_auto=True,color='inns',color_continuous_scale=color_scales)
    st.plotly_chart(fig,use_container_width=True) 