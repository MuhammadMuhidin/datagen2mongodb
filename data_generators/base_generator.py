from pymongo import MongoClient
import pandas as pd
import sqlite3


class BaseGenerator:
    def __init__(self):
        self.data = []

    def to_csv(self, filename):
        """
        Save the generated data to a CSV file.
        """
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

    def to_parquet(self, filename):
        """
        Save the generated data to a Parquet file.
        """
        df = pd.DataFrame(self.data)
        df.to_parquet(filename, index=False)

    def to_sqlite(self, db_name, table_name):
        """
        Save the generated data to a SQLite database.
        """
        df = pd.DataFrame(self.data)
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

    def to_mongodb(self, collection_name, mongo_client):
        """
        Save the generated data to a MongoDB collection.
        """
        df = pd.DataFrame(self.data)
        collection = mongo_client[collection_name]
        collection.insert_many(df.to_dict('records'))
    
