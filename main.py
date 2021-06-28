from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from vector_ai_app import crud, models, schemas
from vector_ai_app.database import SessionLocal, engine

from fastapi import HTTPException, status

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/city/")
def create_city(city:schemas.City, db:Session = Depends(get_db)):
    return crud.create_city(db=db,city=city)

@app.post("/update_city")
def create_city(city:schemas.City, db:Session = Depends(get_db)):
    return crud.update_city(db, city)


@app.post("/country/")
def create_country(country:schemas.Country, db:Session = Depends(get_db)):
    return crud.create_country(db=db,country=country)


@app.get("/countries/")
def get_countries(db:Session = Depends(get_db)):
    return crud.get_all_countries(db)


@app.post("/remove_city/")
def delete_city(city:schemas.RemoveCity, db:Session = Depends(get_db)):
    return crud.remove_city(db=db,city=city)


@app.get("/cities/")
def read_cities(country:str='', skip: int=0,limit:int=100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db,skip=skip,limit=limit,country=country)
    return cities


@app.get("/continents")
def get_continents(db:Session = Depends(get_db)):
    return crud.get_all_continents(db)


@app.get("/raw/")
def raw_sql(db:Session = Depends(get_db)):
    crud.raw_sql(db)


if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port=800)