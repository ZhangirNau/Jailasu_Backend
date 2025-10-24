# ProjectJailasu/backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ProjectJailasu.backend.database import Base


# ----------- Таблица пользователей -----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с заявками (из форм)
    forms = relationship("FormSubmission", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"


# ----------- Таблица заявок с Тильды -----------
class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    form_name = Column(String(100), nullable=False, default="Tilda Form")
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="forms")

    def __repr__(self):
        return f"<FormSubmission(id={self.id}, form={self.form_name})>"


# ----------- Таблица логов (вебхуки и события) -----------
class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    payload = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WebhookLog(type={self.event_type}, time={self.timestamp})>"
