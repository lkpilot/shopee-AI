import pandas as pd
from database.models import Product
import asyncio
from database.database import Session
from sqlalchemy import select
from sentence_transformers import SentenceTransformer
from tqdm import tqdm  # Import tqdm
from client.embedding import load_model


df = pd.read_csv("Data/shopee_products.csv")
df.dropna(inplace=True)
df = df.astype(str)
# Use a synchronous wrapper for the async insert
async def insert_data(model):

    async with Session() as session:
        async with session.begin():
            products = []
            
            # Using tqdm to track progress in a synchronous way
            for index, row in tqdm(df.iterrows(), total=len(df), desc="Inserting productss"):
                try:
                    name_embedding = model.encode(row['name'])
                    
                    product = Product(
                        product_link=row['product_link'],
                        name=row['name'],
                        name_embedding=name_embedding,
                        image_url=row['image_url'],
                        price=float(row['Price']),
                        discount=float(row['discount']),
                        ratings=float(row['ratings']),
                        solds=int(row['solds']),
                        deliver_durations=row['deliver_durations'],
                        location=row['location'],
                        brand_name=row['brand_name'],
                        category=row['Category']
                    )

                    products.append(product)
                except Exception as e:
                    print(e)
                    continue

            # Add all Job_1 objects to the session
            session.add_all(products)
            await session.commit()

        print("Inserted successfully!")


async def main():
    await insert_data(load_model('xlm-roberta-base'))


if __name__ == "__main__":
    asyncio.run(main())