from pymongo import MongoClient
import pandas as pd
import sqlite3


class BaseGenerator:
    def __init__(self):
        self.data = []

    def to_csv_gdrive(self, filename, gdrive_uri, data):
        """
        Save the generated data to a CSV file.
        """
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

    def to_parquet_gdrive(self, filename, gdrive_uri, data):
        """
        Save the generated data to a Parquet file.
        """
        df = pd.DataFrame(self.data)
        df.to_parquet(filename, index=False)

    def to_sqlite_gdrive(self, db_name, table_name, gdrive_uri, data):
        """
        Save the generated data to a SQLite database.
        """
        df = pd.DataFrame(self.data)
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

    def to_mongodb(self, database_name, collection_name, mongodb_uri, data):
        """
        Save the generated data to a MongoDB collection.
        """
        client = MongoClient(mongodb_uri)
        try:
            client.admin.command('ping')  # Check connection
            db = client[database_name]
            collection = db[collection_name]
            if data:
                collection.insert_many(data)
                print(f"Insert {collection_name} done.")
            else:
                print("No data to insert.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
        finally:
            client.close()
