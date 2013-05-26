from sqlalchemy import Column, Integer, String
from database import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False)
    text = Column(String(120), nullable=False)

    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Entry%d, title=%r text=%r>' % (self.id, self.title, self.text)
