from sqlalchemy import select, func, text
from services.graph_state import GraphState
from database.database import Session
from database.models import Product


async def retrieve_product(state: GraphState) -> GraphState:
    async with Session() as session:

        result = await session.execute(text(state['refined_query'].lower()))
        final_result = result.fetchall()

    return {
        **state,
        "result": final_result
    }