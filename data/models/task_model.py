from data.helpers.db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey ,Integer , Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
class Task(Base):
    __tablename__ = "tasks"
    id = Column(String , primary_key=True , index=True)
    task_name = Column(String , nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    due_at = Column(DateTime , nullable=True)
    type  = Column(Integer , nullable=False)
    priority = Column(Integer , nullable=False)
    has_done = Column(Boolean , default=False)
    tags = Column(String , nullable= False)
    updated_at = Column(DateTime, default=datetime.utcnow , onupdate=datetime.utcnow , index=True)
    belongs_to_date = Column(DateTime , default=datetime.utcnow , index=True)
    expiry_time = Column(DateTime , nullable=True)
    is_deleted = Column(Boolean , default=False)
    user = relationship("User")
