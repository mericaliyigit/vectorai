from typing import Optional

from pydantic import BaseModel, validator


class Continent(BaseModel):
    name:str

    @validator('name')
    def prevent_numeric(cls,v):
        if any (i.isdigit() for i in v):
            raise ValueError('Cant contain numbers')
        return v


class Country(BaseModel):
    name:str
    continent:str

    @validator('name','continent')
    def prevent_numeric(cls,v):
        if any (i.isdigit() for i in v):
            raise ValueError('Cant contain numbers')
        return v


class City(BaseModel):
    name:str
    country:str
    area:int
    no_roads:int
    no_trees:int
    no_parks:int
    no_hospitals:int
    population:int

    @validator('name','country')
    def prevent_numeric(cls,v):
        if any (i.isdigit() for i in v):
            raise ValueError('Cant contain numbers')
        return v


class UpdateCity(BaseModel):
    name:str
    country:str
    area: Optional[int]
    no_roads: Optional[int]
    no_trees: Optional[int]
    no_parks: Optional[int]
    no_hospitals: Optional[int]
    population: Optional[int]

    @validator('name','country')
    def prevent_numeric(cls,v):
        if any (i.isdigit() for i in v):
            raise ValueError('Cant contain numbers')
        return v


class RemoveCity(BaseModel):
    city:str
    country:str






