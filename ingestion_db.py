#!/usr/bin/env python
# coding: utf-8
# %%

# %%


import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time


# %%


logging.basicConfig(
    filename="logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)


# %%


engine = create_engine('sqlite:///inventory.db')


# %%


def ingest_db(df, table_name, engine):
    '''This function will ingest the dataframe into databse table'''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False,  chunksize=50_000)



# %%


def load_raw_data():
    '''This function will CSV's as dataframe and ingest it to db'''
    start = time.time()
    for file in os.listdir('data/data'):
        if file.endswith('.csv'):
            file_path = os.path.join('data/data', file)
            df = pd.read_csv(file_path)
            logging.info (f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
        end= time.time()
        total_time =  (end-start)/60
        logging.info ('---------------------------Ingestion Complete---------------------------')
        logging.info(f'\nTotal time taken: {total_time} minutes')


# %%


if __name__ == '__main__':
    load_raw_data()


# %%




