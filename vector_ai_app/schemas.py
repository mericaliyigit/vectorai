from typing import Optional

from pydantic import BaseModel


class Continent(BaseModel):
    name:str


class Country(BaseModel):
    name:str
    continent:str


class City(BaseModel):
    name:str
    country:str
    area:int
    no_roads:int
    no_trees:int
    no_parks:int
    no_hospitals:int
    population:int


class UpdateCity(BaseModel):
    name:str
    country:str
    area: Optional[int] = 1
    no_roads: Optional[int] = 1
    no_trees: Optional[int] = 1
    no_parks: Optional[int] = 1
    no_hospitals: Optional[int] = 1
    population: Optional[int] = 1


class RemoveCity(BaseModel):
    city:str
    country:str






