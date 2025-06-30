import random
from faker import Faker
from data_generators.base_generator import BaseGenerator

class ProductReviewGenerator(BaseGenerator):
    def __init__(self):
        self.fake = Faker('id_ID')
        self.products = []
        self.reviews = []

    def generate(self):
        prod_inserted = 0
        rev_inserted = 0
        prod_without_review_inserted = 0
        prod_with_review_inserted = 0
        max_products = random.randint(1, 50)  # Randomly choose number of products to generate

        for i in range(1, max_products + 1):
            product = {
                "product_id": self.fake.uuid4(),
                "name": self.fake.word(),
                "description": self.fake.sentence(),
                "price": round(random.uniform(10.0, 1000.0), 2),
                "category": random.choice(["electronics", "clothing", "home", "books", "toys"])
            }
            self.products.append(product)
            prod_inserted += 1

            if random.random() < 0.5:  # 50% chance to skip review generation for this product
                prod_without_review_inserted += 1
                continue
            
            max_reviews = random.randint(1, 10)  # Randomly choose number of reviews to generate for this product
            for j in range(1, max_reviews + 1):
                review = {
                    "review_id": self.fake.uuid4(),
                    "product_id": product["product_id"],
                    "user_name": self.fake.name(),
                    "rating": random.randint(1, 5),
                    "comment": self.fake.sentence(),
                    "review_date": self.fake.date_time_this_year().isoformat()
                }
                self.reviews.append(review)
                rev_inserted += 1
            prod_with_review_inserted += 1

        print("=== Summary Generation data (this session only) ===")
        print(f"Total products inserted: {prod_inserted}")
        print(f"Total reviews inserted: {rev_inserted}")
        print(f"Products with reviews: {prod_with_review_inserted}")
        print(f"Products without reviews: {prod_without_review_inserted}")
        print("=== End of Summary ===")

    def get_product_data(self):
        return self.products
    
    def get_review_data(self):
        return self.reviews