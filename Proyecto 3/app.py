import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
import psycopg2


engine = None
resultDataFrame = None

try:
    engine = psycopg2.connect(
        database="Proyecto3DB",
        user = "SMDATABASE",
        password = "Sebas2000",
        host = "database-1.cr7zw8vvqze4.us-east-1.rds.amazonaws.com",
        port = "5432"
    )
    cur = engine.cursor()
    
    Query1 = "select position, age, goals from TOP_7_BUNDESLIGA_TEAMS"
    aux1 = pd.read_sql_query(Query1, engine)
    Query2 = "select goals, club from TOP_7_BUNDESLIGA_TEAMS"
    aux2 = pd.read_sql_query(Query2, engine)
    Query3 = "select age, goals, assists from TOP_7_BUNDESLIGA_TEAMS"
    aux3 = pd.read_sql_query(Query3, engine)

    print(aux1.head())
    print(aux2.head())
    print(aux3.head())

except(Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally: 
    if engine:
        cur.close()
        engine.close()
        print("PostgreSQL connection is closed")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

BarChart = px.bar(aux1, x= 'position', y= ['goals'], barmode = 'relative' , color= "age" , title="Goals made by position")
PieChart = px.pie(aux2, values= 'goals', names= 'club', color_discrete_sequence=px.colors.sequential.RdBu ,title="Goals made by club")
ScatterPlotChart = px.scatter(aux3, x= 'age', y= ['goals','assists'], color="age",title="Goals and assist made by age")

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
])

if __name__ == '__main__':
    app.run_server(debug=True)


