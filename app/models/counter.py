from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.core.database import Base

class Counter(Base):
    __tablename__ = "counter"

    id = Column(Integer, primary_key=True)
    key = Column(String(50))
    period = Column(String(20))
    last_value = Column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("key", "period", name="uq_counter_key_period"),
    )