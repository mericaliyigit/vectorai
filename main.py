import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from vector_ai_app import crud, models, schemas
from vector_ai_app.database import SessionLocal, engine
from celery_worker import create_country_celery, create_city_celery, remove_city_celery, \
    update_city_celery, create_continent_celery

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"Message" : "Vector AI API Index See /docs for more info"}


@app.get("/cities/")
def read_cities(country:str= '', skip: int=0,limit:int=100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db,skip=skip,limit=limit,country=country)
    return cities


@app.post("/create_city/")
def create_city(city:schemas.City):
    create_city_celery.delay(city.dict())
    return {'Message' : f'Request to create {city.name} is received'}


@app.put("/update_city")
def update_city(city:schemas.UpdateCity):
    update_city_celery.delay(city.dict())
    return {'Message' : f'Request to update {city.name} is received'}


@app.delete("/remove_city/")
def delete_city(city:schemas.RemoveCity):
    remove_city_celery.delay(city.dict())
    return {'Message' : f'Request to remove {city.city} is received'}


@app.post("/create_country/")
def create_country(country:schemas.Country):
    create_country_celery.delay(country.dict())
    return {'Message' : f'Request to create {country.name} is received'}


@app.get("/countries/")
def get_countries(db:Session = Depends(get_db)):
    return crud.get_all_countries(db)


@app.post("/create_continent")
def create_continent(continent:schemas.Continent):
    create_continent_celery(continent.dict())
    return {'Message': f"Request to create {continent.name} is received"}


@app.get("/continents/")
def get_continents(db:Session = Depends(get_db)):
    return crud.get_all_continents(db)


if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port=800)
