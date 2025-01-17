from client.llama_client import client
from services.graph_state import GraphState
from database.models import Product


def format_menu(document: Product) -> str:
    document = f"""
=========================
Link: {document.product_link}
Name: {document.name}
Price: {document.price}
Discount: {document.discount}
Ratings: {document.ratings}
Sold: {document.solds}
Location: {document.location}
Brand: {document.brand_name}
Category: {document.category}
"""
    return document



async def generate_desc_answer(state: GraphState) -> GraphState:

    documents = [format_menu(document) for document in state["products"]]
    
    document = "\n\n".join(documents)

    print(document)
    

    openai_response = await client.chat.completions.create(
        model='gemma2-9b-it',
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI Assistnat tasked with answer questions from users."
            },
            {"role": "system", "content": "The user will ask you a question."},
            {"role": "system", 'content': "Question: "},
            {"role": "user", "content": state['refined_question']},
            {"role": "system", "content": "You have been given a list of products which are the result of query to read and answer question about."},
            {"role": "system", "content": "The products are sold on shopee platform, They are as follows:"},
            {"role": "system", "content": document},
            {"role": "system", "content": "If the products is None, You can apologize and ask if the user can ask again."},
            {
                "role": "system",
                'content': "Please answer in MARKDOWN format, if there are some product fit the question, give some information (link, name, Price, discount, ratings, solds, ...) about them. Answer friendly, oonly answer based on the question with products information, do not make it up."
            }
        ]
    )

    response = openai_response.choices[0].message
    answer = response.content

    return {
        **state,
        'answer': answer
    }