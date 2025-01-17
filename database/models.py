from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, table, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid 
from pgvector.sqlalchemy import Vector


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_link = Column(String, index=True)
    name = Column(String)
    name_embedding = Column(Vector)
    image_url = Column(String)
    price = Column(Float)
    discount = Column(Float)
    ratings = Column(Float)
    solds = Column(Integer)
    deliver_durations = Column(String(100))
    location = Column(String(100))
    brand_name = Column(String(100))
    category = Column(String(100))




