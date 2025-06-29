import os, time, random
from pymongo import MongoClient
from faker import Faker


class DataGenerator:
        def __init__(self, mongodb_uri):
            self.client = MongoClient(mongodb_uri)
            self.db = self.client["datagen"]
            self.collection_users = self.db["user_data"]
            self.collection_transactions = self.db["transaction_data"]
            self.fake = Faker()

        def connect_to_mongodb(self):
            try:
                self.client.admin.command('ping')
                print("Connected to MongoDB successfully.")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise e

        def generate_users(self):
            return {
                "user_id": self.fake.uuid4(),
                "name": self.fake.name(),
                "email": self.fake.email(),
                "address": self.fake.address(),
                "phone_number": self.fake.phone_number(),
                "date_of_birth": self.fake.date_of_birth().isoformat()
            }
        
        def generate_transactions(self, user_id):
            return {
                "transaction_id": self.fake.uuid4(),
                "user_id": user_id,
                "amount": self.fake.random_number(digits=5),
                "transaction_date": self.fake.date_time_this_year().isoformat(),
                "transaction_type": random.choice(["credit", "debit"]),
                "status": random.choice(["completed", "pending", "failed"])
            }
        
        def run(self):
            print("Starting data generation...")

            max_users = random.randint(1, 50)  # Randomly choose number of users to generate
            usr_trx_inserted = 0
            trx_inserted = 0
            usr_with_trx_inserted = 0
            usr_without_trx_inserted = 0
                
            for i in range(1, max_users + 1):
                user_data = self.generate_users()
                self.collection_users.insert_one(user_data)
                usr_trx_inserted += 1
                print(f"{i}/{max_users} Inserted user: {user_data['name']}")

                if random.random() < 0.3:  # 30% chance to skip transaction generation for this user
                    usr_without_trx_inserted += 1
                    print("No transactions for this user.")
                    continue
                
                max_transactions = random.randint(1, 10) # Randomly choose number of transactions to generate for this user
                for j in range(1, max_transactions + 1):
                    transaction_data = self.generate_transactions(user_data["user_id"])
                    self.collection_transactions.insert_one(transaction_data)
                    trx_inserted += 1
                    print(f"Inserted {j}/{max_transactions} transaction for user {user_data['name']}")
                    time.sleep(1)
                usr_with_trx_inserted += 1

        print("\n=== Summary (this session only) ===")
        print(f"Total users inserted: {usr_trx_inserted}")
        print(f"Total transactions inserted: {trx_inserted}")
        print(f"Users with transactions: {usr_with_trx_inserted}")
        print(f"Users without transactions: {usr_without_trx_inserted}")

        def close_connection(self):
            self.client.close()

if __name__ == "__main__":
    mongodb_uri = os.getenv("MONGODB_URI")
    data_gen = DataGenerator(mongodb_uri)
    data_gen.connect_to_mongodb()
    try:
        data_gen.run()
    except Exception as e:
        print(f"An error occurred during data generation: {e}")
    finally:
        data_gen.close_connection()
        print("Data generation completed and connection closed.")
