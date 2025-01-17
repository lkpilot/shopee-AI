from datetime import datetime
from langgraph.graph import START, StateGraph, END
from services.graph_state import GraphState

from services.conditional_nodes.split_is_asking_about_desc import split_is_asking_about_desc


from services.nodes.refine_question import refine_question
from services.nodes.embed_question import embed_question
from services.nodes.retrieve_related_desc import retrieve_related_desc
from services.nodes.generate_desc_answer import generate_desc_answer
from services.nodes.generate_query_answer import generate_query_answer
from services.nodes.generate_query import generate_query
from services.nodes.refine_query import refine_query
from services.nodes.retrieve_info import retrieve_info
from services.nodes.retrieve_product import retrieve_product



workflow = StateGraph(GraphState)

workflow.add_node("refine_question", refine_question)
workflow.add_node("embed_question", embed_question)
workflow.add_node("retrieve_related_desc", retrieve_related_desc)
workflow.add_node("generate_query_answer", generate_query_answer)
workflow.add_node("generate_desc_answer", generate_desc_answer)
workflow.add_node("generate_query", generate_query)
workflow.add_node("refine_query", refine_query)
workflow.add_node("retrieve_info", retrieve_info)
workflow.add_node("retrieve_product", retrieve_product)

workflow.add_edge(START, "refine_question")
workflow.add_edge("refine_question", "retrieve_info")
workflow.add_conditional_edges("retrieve_info", split_is_asking_about_desc)


workflow.add_edge("embed_question", "retrieve_related_desc")
workflow.add_edge("retrieve_related_desc", "generate_desc_answer")

workflow.add_edge("generate_query", "refine_query")
workflow.add_edge("refine_query", "retrieve_product")
workflow.add_edge("retrieve_product", "generate_query_answer")


workflow.add_edge("generate_query_answer", END)
workflow.add_edge("generate_desc_answer", END)

app = workflow.compile()


async def answer_question(question: str) -> str:
    input = {
        "start_time": datetime.utcnow(),
        "question": question,
    }

    try:
        result = await app.ainvoke(input)  # Make sure app.ainvoke is defined
        result['end_time'] = datetime.utcnow()
        duration = result['end_time'] - result['start_time']
        answer = result['answer']
        return answer
    except Exception as e:
        return f"An error occurred: {e}"
