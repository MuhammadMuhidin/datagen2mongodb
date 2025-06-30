import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_generators.gen_product_review import ProductReviewGenerator

def main():
    generator = ProductReviewGenerator()
    generator.generate()  # Generate data products and reviews
    prod_data = generator.get_product_data()
    rev_data = generator.get_review_data()
    gdrive_uri = os.getenv('GDRIVE_URI')

    if prod_data:
        generator.to_csv('products.csv', prod_data)
        generator.to_parquet('products.parquet', prod_data)
        generator.to_sqlite('products.db', 'products', prod_data)

    if rev_data:
        generator.to_csv_gdrive('reviews.csv', rev_data)
        generator.to_parquet_gdrive('reviews.parquet', rev_data)
        generator.to_sqlite_gdrive('reviews.db', 'reviews', rev_data)
    else:
        print("No review data generated found.")

if __name__ == "__main__":
    main()