import random, time
from faker import Faker
from data_generators.base_generator import BaseGenerator

class UserTransactionGenerator(BaseGenerator):
    def __init__(self):
        self.fake = Faker('id_ID')
        self.users = []
        self.transactions = []
    
    def generate(self):

        usr_trx_inserted = 0
        trx_inserted = 0
        usr_with_trx_inserted = 0
        usr_without_trx_inserted = 0
        max_users = random.randint(1, 50)  # Randomly choose number of users to generate

        for i in range(1, max_users + 1): # Randomly choose number of users to generate
            user = {
                "user_id": self.fake.uuid4(),
                "name": self.fake.name(),
                "email": self.fake.email(),
                "address": self.fake.address(),
                "phone_number": self.fake.phone_number(),
                "date_of_birth": self.fake.date_of_birth().isoformat()
            }
            self.users.append(user)
            usr_trx_inserted += 1

            if random.random() < 0.5:  # 50% chance to skip transaction generation for this user
                usr_without_trx_inserted += 1
                print(f'No data transaction found.')
                continue
            
            max_transactions = random.randint(1, 10)  # Randomly choose number of transactions to generate for this user
            for j in range(1, max_transactions + 1):  # Randomly generate 1 to 5 transactions per user
                transaction = {
                    "transaction_id": self.fake.uuid4(),
                    "user_id": user["user_id"],
                    "amount": self.fake.random_number(digits=5),
                    "transaction_date": self.fake.date_time_this_year().isoformat(),
                    "transaction_type": random.choice(["credit", "debit"]),
                    "status": random.choice(["completed", "pending", "failed"])
                }
                self.transactions.append(transaction)
                trx_inserted += 1
                usr_with_trx_inserted += 1
        
        print("\nData generation completed successfully, now ready to connect to MongoDB.")
        print("=== Summary Generation data (this session only) ===")
        print(f"Total users inserted: {usr_trx_inserted}")
        print(f"Total transactions inserted: {trx_inserted}")
        print(f"Users with transactions: {usr_with_trx_inserted}")
        print(f"Users without transactions: {usr_without_trx_inserted}")
        print("=== End of Summary ===\n")
        
    def get_user_data(self):
        return(self.users)
    
    def get_transaction_data(self):
        return self.transactions
