import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_generators.gen_user_transaction import UserTransactionGenerator

def main():
    generator = UserTransactionGenerator()
    generator.generate() # Generate data user and transaction
    usrdata = generator.get_user_data()
    trxdata = generator.get_transaction_data()
    mongodb_uri = os.getenv('MONGODB_URI')

    if usrdata:
        generator.to_mongodb('datagen','user',mongodb_uri, usrdata)
    if trxdata:
        generator.to_mongodb('datagen','transaction',mongodb_uri, trxdata)
    else:
        print("No data generated found.")

if __name__ == "__main__":
    main ()