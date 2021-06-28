from pydantic import BaseModel
from typing import List,Optional


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


class RemoveCity(BaseModel):
    city:str
    country:str






