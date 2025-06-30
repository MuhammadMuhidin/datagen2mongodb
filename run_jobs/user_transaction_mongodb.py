import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_generators.user_transaction import UserTransactionGenerator

def main():
    generator = UserTransactionGenerator()
    generator.generate() # Generate data user and transaction
    usrdata = generator.get_user_data()
    trxdata = generator.get_transaction_data()
    mongodb_uri = 'mongodb+srv://muhammadmuhidin222:Muhidin94@cluster0.usomldt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

    if usrdata:
        generator.to_mongodb('datagen','user',mongodb_uri, usrdata)
        generator.to_mongodb('datagen','transaction',mongodb_uri, trxdata)
    else:
        print("No data generated found.")

if __name__ == "__main__":
    main ()