from client.llama_client import client
from services.graph_state import GraphState



async def refine_question(state: GraphState) -> GraphState:
    response = await client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {
                "role": "system",
                "content": "Please refine the question to enhance search results by correcting any typos, grammar errors, or phrasing issues. Do not change the meaning of the question. The question can be in either Vietnamese or English.",
            },
            {
                "role": "user", "content": f"question: {state['question']}"
            }
        ],
        temperature=0.0
    )

    response = response.choices[0].message
    refined_question = response.content
    return {
        **state,
        "refined_question": refined_question
    }