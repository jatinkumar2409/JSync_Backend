from sqlalchemy import Column, ForeignKey, DateTime, String, Boolean
from datetime import datetime

from sqlalchemy.orm import relationship

from data.helpers.db import Base
class TaskCompletion(Base):
    __tablename__ = "task_completions"
    id = Column(String  ,primary_key=True, nullable=False , index=True)
    task_id = Column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    completion_date = Column(DateTime , default=datetime.utcnow, nullable=False , index=True)
    is_deleted = Column(Boolean , default=False)
    task = relationship("Task")