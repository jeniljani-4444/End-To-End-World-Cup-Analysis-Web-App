import pandas as pd#type: ignore
import numpy as np#type: ignore

def batting_data_cleaning():
    df_runs = pd.read_html("https://www.espncricinfo.com/records/trophy/batting-most-runs-career/world-cup-12")[0]
    df_runs.columns = df_runs.columns.str.lower()
    df_runs['country'] = df_runs['player'].str.split('(').str.get(1).str.replace(')','')
    df_runs['player'] = df_runs['player'].str.split('(').str.get(0)

    # df_runs['mat'] = df_runs['mat'].str.replace('*','').astype('int')
    df_runs['hs'] = df_runs['hs'].str.replace('*','').astype('int')
    # df_runs['no'] = df_runs['no'].str.replace('-','0').astype('int')

    df_runs['50'] = df_runs['50'].replace('-',0).astype('int')
    df_runs['100'] = df_runs['100'].replace('-',0).astype('int')

    df_runs['4s'] = df_runs['4s'].str.replace('+','').astype('int')
    df_runs['6s'] = df_runs['6s'].str.replace('+','').astype('int')

    df_runs = df_runs.reindex(columns=['player','country','span','mat','inns','no','runs','hs','ave','bf','sr',
                        '100','50','0','4s','6s'])
    
    df_runs['0'] = df_runs['0'].replace("-",0)
    df_runs['player'] = df_runs['player'].str.strip()

    df_runs.to_csv('dataset/batting_records.csv',index=False)

    df_bat = pd.read_csv("dataset/batting_records.csv")

    return df_bat



def bowl_data_cleaning():
    df_bowl = pd.read_html("https://www.espncricinfo.com/records/trophy/bowling-most-wickets-career/world-cup-12")[0]

    df_bowl.columns = df_bowl.columns.str.lower()

    df_bowl['country'] = df_bowl["player"].str.split('(').str.get(1).str.replace(')','')
    df_bowl['player'] = df_bowl['player'].str.split('(').str.get(0).str.strip()

    df_bowl['4'] = df_bowl['4'].replace('-',0).astype('int')
    df_bowl['5'] = df_bowl['5'].replace('-',0).astype('int')

    # df_bowl['mat'] = df_bowl['mat'].str.replace('*','').astype('int')

    df_bowl = df_bowl.reindex(columns=['player','country','span','mat','inns','balls','overs','mdns','runs','wkts',
                                       'sr','bbi', 'ave','econ','4','5'])

    df_bowl['year_one'] = df_bowl.span.str.split('-').str.get(0).astype('int')
    df_bowl['year_two'] = df_bowl.span.str.split('-').str.get(1).astype('int')
    df_bowl['year_diff'] = df_bowl['year_two'] - df_bowl['year_one']

    df_bowl.to_csv("dataset/bowling_records.csv",index=False)

    bowling = pd.read_csv("dataset/bowling_records.csv")

    return bowling