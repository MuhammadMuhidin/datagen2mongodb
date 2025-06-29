import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_generators.user_transaction import UserTransactionGenerator
from pymongo import MongoClient

def insert_to_mongodb(data, collection):
    """
    Insert data into MongoDB collection.
    """
    if data:
        collection.insert_many(data)
        print(f"Inserted {len(data)} records into {collection.name} collection done!")
    else:
        print("No data to insert.")

if __name__ == "__main__":
    # Initialize the generator
    generator = UserTransactionGenerator()
    
    # Generate user and transaction data
    generator.generate()
    
    # Get user and transaction data
    user_data = generator.get_user_data()
    transaction_data = generator.get_transaction_data()
    
    # MongoDB connection setup
    mongo_client = MongoClient('mongodb+srv://muhammadmuhidin222:Muhidin94@cluster0.usomldt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = mongo_client['datagen']  # Database name
    
    # Insert user data into MongoDB
    insert_to_mongodb(user_data, db['users_data'])
    
    # Insert transaction data into MongoDB
    insert_to_mongodb(transaction_data, db['transactions_data'])
    
    print("Data generation and insertion completed.")
    mongo_client.close()
    # Close the MongoDB connection