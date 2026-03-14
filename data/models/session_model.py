
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey , DateTime
from sqlalchemy.orm import relationship

from data.helpers.db import Base
class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id" , ondelete="CASCADE") , nullable=False , index=True)
    created_at = Column(DateTime, default=datetime.now)
    last_used_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="sessions")