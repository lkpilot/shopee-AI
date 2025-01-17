from datetime import datetime
from typing_extensions import TypedDict
from database.models import Product

class GraphState(TypedDict):
    start_time: datetime
    end_time: datetime | None
    question: str
    refined_question: str | None
    question_embedding: list[float] | None
    answer: str| None
    is_asking_about_desc: str | None
    query: str | None
    refined_query: str | None
    products: list[Product] | None
    result: list[Product] | None