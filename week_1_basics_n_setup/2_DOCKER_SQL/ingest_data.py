#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time
import os

def main(params):
    
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url

    # download the CSV
    csv_name = 'output.csv.gz'
    
    os.system(f"wget {url} -O {csv_name}") #download a csv from a URL and name it with csv_name
 
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000,on_bad_lines='warn') # do it a little at a time
    df = next(df_iter)

    try:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    except AttributeError:
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    # engine.connect()

    # use replace since this is just for column headers, this creates the table headers in SQL
    df.head(n=0).to_sql(con=engine, name=table_name, if_exists='replace') 

    # iterate through the whole file and add all the data to the db
    df.to_sql(con=engine, name=table_name, if_exists='append') 

    while True:
        t_start = time()

        df = next(df_iter)
        
        try:
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        except AttributeError:
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            
        df.to_sql(con=engine, name=table_name, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk..., took %.3f second' % (t_end - t_start))

###############################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV to Postgres')

    # user
    # password
    # host
    # port
    # database name
    # table name
    # url of csv

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    # parser.add_argument('user', required=True, help='user name for postgres')
    # parser.add_argument('password', required=True, help='password for postgres')
    # parser.add_argument('host', required=True, help='host for postgres')
    # parser.add_argument('port', required=True, help='port for postgres')
    # parser.add_argument('db', required=True, help='database name for postgres')
    # parser.add_argument('table_name', required=True, help='name of the table where we will write the results to')
    # parser.add_argument('url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)
    # print(args.accumulate(args.integers))


