from client.llama_client import client
from services.graph_state import GraphState
from database.models import Product


def format_menu(document: Product) -> str:
    formatted_document = "=========================\n"
    
    # Check and append each element if it is not None
    if hasattr(document, 'product_link') and document.product_link:
        formatted_document += f"Link: {document.product_link}\n"
    
    if hasattr(document, 'name') and document.name:
        formatted_document += f"Name: {document.name}\n"
    
    if hasattr(document, 'price') and document.price is not None:
        formatted_document += f"Price: {document.price}\n"
    
    if hasattr(document, 'discount') and document.discount is not None:
        formatted_document += f"Discount: {document.discount}\n"
    
    if hasattr(document, 'ratings') and document.ratings is not None:
        formatted_document += f"Ratings: {document.ratings}\n"
    
    if hasattr(document, 'solds') and document.solds is not None:
        formatted_document += f"Sold: {document.solds}\n"
    
    if hasattr(document, 'location') and document.location:
        formatted_document += f"Location: {document.location}\n"
    
    if hasattr(document, 'brand_name') and document.brand_name:
        formatted_document += f"Brand: {document.brand_name}\n"
    
    if hasattr(document, 'category') and document.category:
        formatted_document += f"Category: {document.category}\n"
    
    # Return the formatted string with trailing newline removed
    return formatted_document.strip()


async def generate_query_answer(state: GraphState) -> GraphState:

    query_result = state['result']
    if len(query_result[0]) == 1:
        query_result = query_result[0][0]
    else:
        query_result = [format_menu(document) for document in state["result"]]
        query_result = "\n\n".join(query_result)


    response = await client.chat.completions.create(
        model='gemma2-9b-it',
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Your task is to answer the user's question based only on the provided query result from the database."
            },
            {
                "role": "user", 
                "content": state['refined_question']
            },
            {
                "role": "system", 
                "content": f"Query result: {query_result}"
            },
            {
                "role": "system",
                "content": (
                    "If you don't have enough information to answer the question based on the query result, "
                    "simply return the query result as it is. The query result represents the most accurate information, so "
                    "you should rely on it directly."
                    "If you have enough information and kinda understand the context, answer the question based on the query result."
                )
            },
            {
                "role": "system",
                "content": "Please respond in MARKDOWN format. Your answer should be clear, friendly, and concise, with extra detail where necessary."
            }
        ]
    )

    print(query_result)

    response = response.choices[0].message
    answer = response.content

    return {
        **state,
        'answer': answer
    }