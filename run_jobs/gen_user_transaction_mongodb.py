import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_generators.user_transaction import UserTransactionGenerator
from pymongo import MongoClient

def insert_to_mongodb(data, collection):
    if data:
        collection.insert_many(data)
        print(f"Insert {collection.name} done")
    else:
        print("No data to insert.")

if __name__ == "__main__":
    # Initialize the generator and generating user transactions data
    generator = UserTransactionGenerator()
    generator.generate()
    
    # Get user and transaction data
    user_data = generator.get_user_data()
    transaction_data = generator.get_transaction_data()
    
    # MongoDB connection setup
    mongo_client = MongoClient(os.getenv('MONGODB_URI'))
    print("MongoDB is connected successfully, ready to insert data.")
    db = mongo_client['datagen']  # Database name
    
    # Insert user data into MongoDB
    insert_to_mongodb(user_data, db['users_data'])
    insert_to_mongodb(transaction_data, db['transactions_data'])

    # Close the MongoDB connection
    mongo_client.close()
    print("MongoDB is closed successfully, all data inserted.")
