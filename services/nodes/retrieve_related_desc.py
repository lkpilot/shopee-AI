from sqlalchemy import select, func
from services.graph_state import GraphState
from database.database import Session
from database.models import Product


async def retrieve_related_desc(state: GraphState) -> GraphState:
    async with Session() as session:
        query = (
            select(Product)
            .where(
                Product.name != None,
                func.trim(func.regexp_replace(Product.name, r"[\n\r\u2028]+", "", "g")) != ""
            )
            .order_by(Product.name_embedding.cosine_distance(state['question_embedding']))
            .limit(5)
        )

        result = await session.execute(query)
        products = result.scalars().all()

    return {
        **state,
        "products": products
    }