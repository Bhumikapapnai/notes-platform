from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base
#in sqlalchemy each class is table nad its variable is its column
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Resource(Base):
    __tablename__="resources"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    subject=Column(String, nullable=False)
    semester=Column(Integer, nullable=False)
    resource_type=Column(String, nullable=False)
    year=Column(Integer, nullable=True)
    file_url=Column(String, nullable=False)
    uploader_id=Column(Integer, ForeignKey("users.id"))