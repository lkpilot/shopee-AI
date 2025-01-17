from client.llama_client import client
from services.graph_state import GraphState



async def generate_query(state: GraphState) -> GraphState:
    response = await client.chat.completions.create(
        model='llama3-70b-8192',
        messages=[
            {
                "role": "system",
                "content": """
                    You are tasked with writing SQLAlchemy queries for a database table called products. The database only has one table (products). The table contains the following columns:

                    id (UUID, primary key): Unique identifier for each product.
                    product_link (String, unique, indexed): A unique URL link to the product.
                    name (String): Name of the product.
                    name_embedding (Vector): Embedding representation of the product's name.
                    image_url (String): URL of the product image.
                    price (Float): Price of the product.
                    discount (Float): Discount percentage on the product.
                    ratings (Float): Ratings of the product.
                    solds (Integer): Number of units sold.
                    deliver_durations (String): Delivery durations for the product.
                    location (String): Location of the seller, which contains the name of the province or city. In the case of Ho Chi Minh, it is represented as 'TP. Hồ Chí Minh'.  
                    brand_name (String): Brand name of the product.
                    category (String): Category to which the product (11 Values: 'chăm sóc da mặt', 'tắm & chăm sóc cơ thể', 'vệ sinh răng miệng', 'trang điểm', 'chăm sóc phụ nữ', 'chăm sóc nam giới', 'dụng cụ & phụ kiện làm đẹp', 'chăm sóc tóc', 'nước hoa', 'bộ sản phẩm làm đẹp', 'khác')


                    You will receive a question that you need to refine and then write a Python function using SQLAlchemy to perform the operation. The question is as follows:

                    For example: 
                    question: how many brands in Ho Chi Minh City? 
                    response:
                    SELECT COUNT(DISTINCT brand_name) FROM products WHERE location = 'TP. Hồ Chí Minh';

                    If the question involve to brand:
                    question: hada labo bán chạy nhất sản phẩm nào?
                    response:
                    SELECT * from products where brand_name = 'hada labo' ORDER BY solds DESC LIMIT 1;
                    
                    If the question involve to product name:
                    question: Có bao nhiêu nhãn hàng bán sữa rửa mặt hương tự nhiên?
                    response:
                    SELECT COUNT(DISTINCT brand_name) FROM products WHERE location = 'TP. Hồ Chí Minh' and name like '%sữa rửa mặt hương tự nhiên%';
                    
                    The output should be a string containing the SQL query that answers the question. Do not add any additional text or explanation.
                    Your output should strictly follow the format shown above. Return only the SQL query as a string, without any code block formatting or extra characters.
                """   
            },
            {
                "role": "user", "content": f"question: {state['question']}"
            },
            {
                "role": "system",
                "content": """
                    Only return the SQL query that you would use to answer the question.
                    Do not include any additional text, explanation, or code block formatting.
                """
            }
        ],
        temperature=0.0
    )


    response = response.choices[0].message
    query = response.content

    print(query)
    return {
        **state,
        "query": query
    }