from services.graph_state import GraphState

def split_is_asking_about_desc(state: GraphState) -> str:
    
    is_asking_about_desc = state['is_asking_about_desc'].upper()
    if is_asking_about_desc.strip() == "TRUE":
        return "embed_question"
    else:
        return "generate_query"