from services.graph_state import GraphState
from client.embedding import load_model


async def embed_question(state: GraphState) -> GraphState:
    model = load_model('xlm-roberta-base')
    embedding =  model.encode(state['refined_question'])


    return{
        **state,
        "question_embedding": embedding
    }