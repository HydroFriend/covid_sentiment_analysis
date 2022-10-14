import pandas as pd
import os
from sqlalchemy import create_engine
from tqdm import tqdm


def csv_to_df(csv_file):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.replace(r'[^a-zA-Z_]*$', '', regex=True)
    df = df[["created_at", "id_str", "text", "user", "lang", "favorite_count", "retweet_count",
             "quote_count", "location", "country", "day", "hour", "Anger",
             "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]]
    return df


def df_to_postgres(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists='append', index=False)


def create_db_connection():
    engine = create_engine('postgresql://postgres:postgrespw@localhost:5432/postgres')
    return engine


def main():
    csv_dir = "D:/covid research/all/"
    csv_list = os.listdir(csv_dir)
    table_name = 'powerbi_data_input'
    engine = create_db_connection()
    for csv_file in (pbar := tqdm(csv_list)):
        try:
            pbar.set_description(f"Uploading {csv_file} to {table_name}")
            df = csv_to_df(csv_dir + csv_file)
            df_to_postgres(df, table_name, engine)
        except:
            print("\nthere is something wrong with this file: ", csv_file)
            logf = open("D:/covid research/logs/csv_to_postgres.txt", "a")
            logf.write(csv_file)
            logf.close()


if __name__ == '__main__':
    main()
