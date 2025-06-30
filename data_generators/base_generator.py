from pymongo import MongoClient
import pandas as pd
import sqlite3


class BaseGenerator:
    def __init__(self):
        """
        Initialize the base generator.
        This class can be extended to create specific data generators.
        """
        pass
    
    def get_dataframe(self, data):
        """
        Convert a list of dictionaries to a pandas DataFrame.
        """
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)

    def to_csv(self, filename, data):
        """
        Convert the data to a CSV file.
        """
        df = self.get_dataframe(data)
        if not df.empty:
            df.to_csv(filename, index=False)
            print(f"CSV file {filename} created successfully.")
        else:
            print("No data to write to CSV.")

    def to_parquet(self, filename, data):
        """
        Convert the data to a Parquet file.
        """
        df = self.get_dataframe(data)
        if not df.empty:
            df.to_parquet(filename, index=False)
            print(f"Parquet file {filename} created successfully.")
        else:
            print("No data to write to Parquet.")

    def to_sqlite(self, db_filename, table_name, data):
        """
        Save the generated data to a SQLite database.
        """
        conn = sqlite3.connect(db_filename)
        try:
            df = self.get_dataframe(data)
            if not df.empty:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Data inserted into {table_name} table in {db_filename}.")
            else:
                print("No data to insert into SQLite.")
        except Exception as e:
            print(f"Error inserting data into SQLite: {e}")
        finally:
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
