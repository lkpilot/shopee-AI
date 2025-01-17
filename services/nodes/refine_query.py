from client.llama_client import client
from services.graph_state import GraphState



async def refine_query(state: GraphState) -> GraphState:
    response = await client.chat.completions.create(
        model='llama3-70b-8192',
        messages=[
            {
                "role": "system",
                "content": """
                    You are a validator and corrector for SQL queries, specifically for PostgreSQL. 
                    The database only has one table (products). The table contains the following columns:

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

                    Your task is to:
                    - Evaluate whether the query correctly and fully answers the user's question. If the query does not solve the question, modify it to accurately address the user's request.
                    - Ensure the SQL query adheres strictly to PostgreSQL syntax and conventions.
                    - Only correct the query if there are actual syntax errors or issues that would cause it to fail in PostgreSQL.
                    - Do not modify the query for stylistic reasons, including unnecessary quoting of identifiers, unless required for correctness.
                    If the query is already valid and requires no changes, return it exactly as it is without modification.
                    """
            },
            {
                "role": "user", "content": f"question: {state['question']}"
            },
            {
                "role": "user", "content": state['query'],
            },
            {
                "role": "system",
                "content": """
                    Return only the SQL query as output. Do not include any explanations, additional text, or unnecessary modifications.
                    If no modifications are required, return the query exactly as it was inputted.
                    """
            }
        ],
        temperature=0.0
    )


    response = response.choices[0].message
    refine_query = response.content

    print(refine_query)
    return {
        **state,
        "refined_query": refine_query
    }