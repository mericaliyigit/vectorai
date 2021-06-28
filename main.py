from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from vector_ai_app import crud, models, schemas
from vector_ai_app.database import SessionLocal, engine
from celery_worker import create_country_celery, create_city_celery, remove_city_celery, \
    update_city_celery, create_continent_celery
from vector_ai_app.crud import raw_sql, remove_city

from fastapi import HTTPException, status

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#CRUD
@app.get("/cities/")
def read_cities(country:str='', skip: int=0,limit:int=100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db,skip=skip,limit=limit,country=country)
    return cities

#Done
@app.post("/create_city/")
def create_city(city:schemas.City):
    create_city_celery.delay(city.dict())


#Done
@app.post("/update_city")
def update_city(city:schemas.City):
    update_city_celery.delay(city.dict())


#Done
@app.post("/remove_city/")
def delete_city(city:schemas.RemoveCity):
    remove_city_celery.delay(city.dict())


# Done
@app.post("/create_country/")
def create_country(country:schemas.Country):
    create_country_celery.delay(country.dict())

#CRUD
@app.get("/countries/")
def get_countries(db:Session = Depends(get_db)):
    return crud.get_all_countries(db)

#DONE
@app.post("/create_continent")
def create_continent(continent:schemas.Continent):
    create_continent_celery(continent.dict())
    return {'Message': f"Request to create continent with name {continent.name} received"}



#CRUD
@app.get("/continents/")
def get_continents(db:Session = Depends(get_db)):
    return crud.get_all_continents(db)


if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port=800)
