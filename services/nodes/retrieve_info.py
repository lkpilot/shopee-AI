from services.graph_state import GraphState
from client.llama_client import client

async def retrieve_info(state: GraphState) -> GraphState:
    response = await client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the user's question into one of the following categories:\n"
                    "1. 'False' if the question refers to a specific brand name or asks for information about a brand.\n"
                    "2. 'False' if the question asks for structured data, such as a list, specific facts, or queries about counts, locations, or other specific details.\n"
                    "3. 'False' if the question asks for information about the quantity, number, or existence of something (e.g., 'how many', 'how much').\n"
                    "4. 'True' if the question asks for a recommendation or specify descriptive information about a product or service. Otherwise return 'False'.\n"
                    "Answer only with either 'True' or 'False'. Provide no additional explanation or details."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {state['question']}  "
            },
            {
                "role": "system",
                "content": "Respond with 'True' or 'False' based solely on the nature of the question, without elaboration."
            }
        ],
        temperature=0.0
    )

    response = response.choices[0].message
    is_asking_about_desc = response.content

    return {
        **state,
        "is_asking_about_desc": is_asking_about_desc
    }