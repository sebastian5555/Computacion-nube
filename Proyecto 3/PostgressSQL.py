import psycopg2
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import pandas as pd
import numpy as np

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
    
    """
    cur.execute('''CREATE TABLE TOP_7_BUNDESLIGA_TEAMS
        (Name TEXT PRIMARY KEY,
        Club TEXT,
        Nationality TEXT,
        Position TEXT,   
        Age INT,
        Matches INT,
        Starts INT,
        Mins INT,
        Goals INT,
        Assists INT,
        Penalty_Goals INT,
        Penalty_Attempted INT,
        xG real,
        xA real,
        Yellow_Cards INT,
        Red_Cards INT
        );''')
    print("Table created successfully")
    """
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('rajatrc1705/bundesliga-top-7-teams-offensive-stats')
    zf = ZipFile('bundesliga-top-7-teams-offensive-stats.zip')
    zf.extractall('dataset')
    zf.close()
    print('Done')

    df = pd.read_csv('dataset/bundesliga_top7_offensive.csv')
    #print(len(df.Name))

    """
    names = "(" + ",".join(list(df.columns)) + ")"
    print(names)
    for i in range(df.shape[0]):
        fila  = [str(j) for j in list(df.iloc[i])] 
        a = "'" + fila[0].replace("'","´") + "'"
        b = "'" + fila[1] + "'"
        c = "'" + fila[2] + "'"
        d = "'" + fila[3] + "'"      
        hola = "INSERT INTO TOP_7_BUNDESLIGA_TEAMS{0} VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16});".format(names, a, b, c, d, fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], fila[12], fila[13], fila[14], fila[15])
        cur.execute(hola)
        print(i)
    """
    postgreSQL_select_Query = "select position, age, goals from TOP_7_BUNDESLIGA_TEAMS"
    aux = pd.read_sql_query(postgreSQL_select_Query, engine)
    print(aux.shape)
    print(aux.head()) 
    
    """
    cur.execute("DROP TABLE IF EXISTS TOP_7_BUNDESLIGA_TEAMS")
    """
except(Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally: 
    if engine:
        engine.commit()
        cur.close()
        engine.close()
        print("PostgreSQL connection is closed")
