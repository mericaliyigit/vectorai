from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship, relation
from .database import Base


class Continent(Base):
    __tablename__ = 'continent'
    continent_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True,nullable=False)

    def __str__(self):
        return f"{self.name} id = {self.continent_id}"


class Country(Base):
    __tablename__ ='country'
    country_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String, index=True, unique=True,nullable=False)
    continent_id = Column(Integer, ForeignKey('continent.continent_id'),nullable=False)

    def __str__(self):
        return f"{self.name} id = {self.country_id}"


class City(Base):
    __tablename__ ='city'
    city_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,index=True,nullable=False)
    area = Column(Integer,default=1)
    population = Column(Integer,default=1)
    no_roads = Column(Integer,default=1)
    no_trees = Column(Integer,default=1)
    no_parks = Column(Integer,default=1)
    no_hospitals = Column(Integer, default=1)

    country_id = Column(Integer,ForeignKey('country.country_id'), nullable=False)
    country_name = relation(Country,backref='city')

    def __str__(self):
        return f"{self.name} id = {self.city_id}"



