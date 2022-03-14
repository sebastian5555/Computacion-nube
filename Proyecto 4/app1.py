from collections import namedtuple
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import dash
from dash import html
from dash import dcc
from pkg_resources import Distribution
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import boto3

api = KaggleApi()
api.authenticate()
api.dataset_download_files('rajatrc1705/bundesliga-top-7-teams-offensive-stats')
zf = ZipFile('bundesliga-top-7-teams-offensive-stats.zip')
zf.extractall('dataset')
zf.close()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('dataset/bundesliga_top7_offensive.csv')
df["Goals"] = df["Goals"].astype(int)
BarChart = px.bar(df, x= 'Position', y= ['Goals'], barmode = 'relative' , color= "Age" , title="Goals made by position")
PieChart = px.pie(df, values= 'Goals', names= 'Club', color_discrete_sequence=px.colors.sequential.RdBu ,title="Goals made by club")
ScatterPlotChart = px.scatter(df, x= 'Age', y= ['Goals','Assists'], color="Age",title="Goals and assist made by age")

app.layout = html.Div(children=[
    html.H1(children='Bundesliga Top 7 Teams Offensive Stats', style={'text-align': 'center'}),

    html.Div(children='''
        The Bundesliga is one of the most entertaining football leagues to watch. Its constant attacking football provides an environment where its impossible to not like the matches. That is why im presenting here the 7 best teams for the 2020-2021 season and its most important stats related to goals.
    '''),
    
    html.Div(children=[
            html.H3('First, we will take a look at the goals made by position. But first we need to know what each position means:'),
            html.P('- FW: Forward'),
            html.P('- MF: Midfielder'),
            html.P('- DF: Defender'),
            html.P('- GK: Goalkeeper'),
            html.P('When there is two positions together, it means that those players can usually play at either one of those.'),
    ]),

    html.Div([
        dcc.Graph(
            id='Graph1',
            figure=BarChart
        ),  
    ]),

    html.Div(children=[
            html.P('As we expected the most goals are scored by the forwards with more than 150 goals. However, the midfielders and the forwards that can play as midfilerders have a lot of goals aswell with a combined of more than 150 goals.'),
    ]),

    html.Div(children=[
            html.H3('Now, we will take a look at the goals made by club. This information give us an idea about which are the most offensive and effective teams in the top 7 of the league. Then, we will compare this with the top 7 of the league to find any relations about this.'),
            html.P('The seven teams we will look at are the top 7 of the classification. This are:  '),
            html.P('- Bayern Munech'),
            html.P('- Borussia Dortmund'),
            html.P('- Frankfurt'),
            html.P('- Leipzig'),
            html.P('- Wolfsburg'),
            html.P('- Bayer Leverkusen'),
            html.P('- Union Berlin'),
    ]),

    html.Div([
        dcc.Graph(
            id='Graph2',
            figure=PieChart
        ),  
    ]),

     html.Div(children=[
            html.P('As expected Bayern Munech and Borussia Dortmund have the most goals in the league. '),
            html.P('Nonetheless, if we look up the entire Bundesliga table we see that a team like Borussia monchedgladbach, who is eight in position, has more goals than Leipzig, Leverkusen and Union berlin. This tell us that in order to reach the highest rankings you need a good defense aswell.'),
            html.P('Also, we can see that a team like Union Berlin has the least goals in the TOP 12 IN THE LEAGUE. Meaning that they probably win all their games by one goal and defend their way through.'),
    ]),

    html.Div(children=[
            html.H3('Finally, we will take a look at the goals and assist made by age. This way we will found out which is the prime age of the footballers in the bundesliga.'),
    ]),

    html.Div([
        dcc.Graph(
            id='Graph3',
            figure=ScatterPlotChart
        ),  
    ]),

    html.Div(children=[
            html.P('we have 3 peaks of age in this graph. '),
            html.P('First, at 19-20 when players have just only started their carrers, and are adapting to playing professional football. But also, they are hungry to be the very best.'),
            html.P('Then, at 24 when they got some experience and now have the confidence to be the in the starter eleven every weekend for their teams.'),
            html.P('Last, at 31 when the players have acquired enough experienced to be at their top in the game and get the best numbers.'),
    ]),

    html.Div(children=[
            html.H3('So, this teams and their players are not only the best in the bundesliga but some of them are the very best in the world. We learned that the offensive part is crucial but in order to be the best you need a solid defence also. You need a TEAM.'),
    ]),

    html.Div(children=[
            html.P('If you have any suggestions on how to upgrade this web page, please leave a comment below.'),
    ]),

    html.Div([
        dcc.Input(
            id='my_txt_input',
            type='text',
            debounce=True,           # changes to input are sent to Dash server only on enter or losing focus
            pattern=r"^[A-Za-z].*",  # Regex: string must start with letters only
            spellCheck=True,
            inputMode='latin',       # provides a hint to browser on type of data that might be entered by the user.
            name='text',             # the name of the control, which is submitted with the form data
        ),
    ]),   
    html.Button('Submit', id='my_button', n_clicks=0),
    html.Div(id='my_txt_output', style={'whiteSpace': 'pre-line'})
])
@app.callback(
    Output('my_txt_output', 'children'),
    Input('my_button', 'n_clicks'),
    State('my_txt_input', 'value'),
)

def update_output(nclicks, value):
    if nclicks > 0:
        sns = boto3.resource('sns')
        topic = sns.Topic(arn="arn:aws:sns:us-east-1:150839082595:SM_proyecto4_comments")
        topic.publish(Message=value)
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('SM_Proyecto4_comments')
        table.put_item(
            Item={
                'comment' : value,
            })
        return 'Your commentary: "{}"'.format(value) + ' has been submitted.'

if __name__ == '__main__':
    app.run_server(debug=True)

print('done')

