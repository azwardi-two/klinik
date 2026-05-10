from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.core.database import Base

class Counter(Base):
    __tablename__ = "counter"

    id = Column(Integer, primary_key=True)
    key = Column("key_name",String(50))
    period = Column("period_key",String(20))
    last_value = Column("lastvalue",Integer, default=0)

    __table_args__ = (
        UniqueConstraint("key_name", "period_key", name="uq_counter_key_period"),
    )