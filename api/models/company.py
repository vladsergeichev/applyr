from sqlalchemy import BigInteger, Column, DateTime, String, Text
from sqlalchemy.sql import func

from database import Base


class CompanyModel(Base):
    __tablename__ = "company"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
