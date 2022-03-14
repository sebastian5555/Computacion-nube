from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np

api = KaggleApi()
api.authenticate()
api.dataset_download_files('rajatrc1705/bundesliga-top-7-teams-offensive-stats')
zf = ZipFile('bundesliga-top-7-teams-offensive-stats.zip')
zf.extractall('dataset')
zf.close()
print('Done')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('dataset/bundesliga_top7_offensive.csv')

BarChart = px.bar(df, x= 'Position', y= 'Goals', color="Position", title="Goals made by position")
PieChart = px.pie(df, values= 'Goals', names= 'Club', color="Club",title="Goals made by club")
ScatterPlotChart = px.scatter(df, x= 'Age', y= ['Goals','Assists'], color="Age",title="Goals and assist made by age")

app.layout = html.Div(children=[
    html.H1(children='Bundesliga Top 7 Teams Offensive Stats', style={'text-align': 'center'}),

    html.Div(children='''
        The best 7 teams of the bundesliga for the 2020-2021 season.
    '''),
    html.Div([
        dcc.Graph(
            id='Graph1',
            figure=BarChart
        ),  
    ]),
    html.Div([
        dcc.Graph(
            id='Graph2',
            figure=PieChart
        ),  
    ]),
    html.Div([
        dcc.Graph(
            id='Graph3',
            figure=ScatterPlotChart
        ),  
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)


