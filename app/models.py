from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# class should extend from base
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable = False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # sqlalchemy foreign key
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable = False)

    # create relation
    owner = relationship("User")

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, nullable = False)
    email = Column(String,nullable = False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__="votes"
    id = Column(Integer, primary_key=True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),nullable=False)
    

    


