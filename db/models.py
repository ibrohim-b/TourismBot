from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)  # path: media/images/city_xxx.jpg

    excursions = relationship("Excursion", back_populates="city")
    
    def __str__(self):
        return f"{self.id} - {self.name}"

class Excursion(Base):
    __tablename__ = "excursions"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    title = Column(String)
    description = Column(Text)
    image = Column(String, nullable=True)  # path: media/images/excursion_xxx.jpg
    video = Column(String, nullable=True)  # path: media/videos/excursion_xxx.mp4

    city = relationship("City", back_populates="excursions")
    points = relationship("Point", back_populates="excursion", order_by="Point.order")
    
    def __str__(self):
        return f"{self.id} - {self.title}"

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True)
    excursion_id = Column(Integer, ForeignKey("excursions.id"))

    order = Column(Integer)
    title = Column(String)
    text = Column(Text)

    lat = Column(Float)
    lng = Column(Float)

    audio = Column(String)   # path: media/audio/xxx.mp3
    image = Column(String)   # path: media/images/xxx.jpg
    video = Column(String, nullable=True)  # path: media/videos/xxx.mp4

    excursion = relationship("Excursion", back_populates="points")
