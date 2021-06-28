from typing import List

from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from . import models, schemas


def get_cities(db: Session, skip: int = 0, limit: int = 100,country=''):

    q = db.query(
        models.City, models.Country, ).filter(models.City.country_id == models.Country.country_id,)
    if country != '':
        q = q.filter(models.Country.name == country).offset(skip).limit(limit).all()
    else:
        q = q.offset(skip).limit(limit).all()

    results = []

    for item in q:
        new_city = {'name': item.City.name, 'area': item.City.area, 'no_hospitals': item.City.no_hospitals,
                    'no_parks': item.City.no_parks, 'no_trees': item.City.no_trees,
                    'country': item.City.country_name.name, 'population': item.City.population,
                    'no_roads': item.City.no_roads}
        results.append(new_city)
        print(new_city)

    return results


def update_city(db:Session, city:schemas.City):

    the_country = db.query(models.Country).filter(models.Country.name == city.country).first()

    if the_country is not None:

        the_city = db.query(models.City).filter(models.City.name == city.name).\
            filter(models.City.country_id == the_country.country_id).first()

        # We have found the city in the db we are updating it
        if the_city is not None:

            the_city.name = city.name
            the_city.population = city.population
            the_city.no_parks = city.no_parks
            the_city.no_roads = city.no_roads
            the_city.no_trees = city.no_trees
            the_city.no_hospitals = city.no_hospitals
            the_city.country_id = the_country.country_id

            db.commit()
            return True
        else:
            return False


def remove_city(db:Session, city:schemas.RemoveCity):

    the_country = db.query(models.Country).filter(models.Country.name == city.country).first()
    if the_country is None:
        return {'Error': f'City {city.city} in {city.country} does not exist'}
    else:
        query = db.query(models.City).filter(models.City.name == city.city).filter(models.City.country_id == the_country.country_id)
        to_delete = query.first()

    if to_delete is not None:
        query.delete()
        db.commit()
        return {f'Successfully deleted {city.city} in {city.country}'}
    else:
        return {'Error': f'City {city.city} in {city.country} does not exist'}


def create_country(db: Session, country: schemas.Country):
    the_continent = db.query(models.Continent).filter(models.Continent.name == country.continent).first()
    if the_continent is not None:
        print('AA')
        same_continent = db.query(models.Country).filter(models.Country.continent_id == the_continent.continent_id).filter(
            models.Continent.country_id == the_continent.country_id).first()

    else:
        return {'Error': f'No such continent exist'}


def proxy_to_dictionary(result_proxy):
    return [dict(row) for row in result_proxy]


def get_all_continents(db:Session):
    query_string = "select continent.name as continent_name, sum(population) as population, sum(area) as total_area," \
                   "sum(no_roads) as total_roads , sum(no_parks) as total_parks," \
                   "sum(no_trees) as total_trees" \
                   " from" \
                   " city join country" \
                   " on city.country_id = country.country_id" \
                   " join continent" \
                   " on country.continent_id = continent.continent_id" \
                   " group by continent.name"
    query = db.execute(query_string)
    results = proxy_to_dictionary(query)
    return results


def get_all_countries(db:Session):

    query_string = "select country.name as country_name, sum(population) as population, sum(area) as total_area," \
            "sum(no_roads) as total_roads , sum(no_parks) as total_parks," \
            "sum(no_trees) as total_trees" \
            " from" \
            " city join country" \
            " on city.country_id = country.country_id" \
            " group by country.name"

    query = db.execute(query_string)
    results = proxy_to_dictionary(query)
    return results


def raw_sql(db:Session):
    query=db.execute("Select * from continent where continent_id = '95'")
    aa=proxy_to_dictionary(query)
    print('Stop')
    result= query.fetchall()
    for row in result:
        print(row)

    print('RAAW')


def create_citya(db:Session, create_city : schemas.City):

    query_string = "select country.country_id from city" \
                   " join country " \
                   " on country.country_id = city.country_id" \
                   f" where country.name ='{create_city.country}'" \
                   " limit 1"
    query = db.execute(query_string)
    aa= proxy_to_dictionary(query)
    print('Stop')


def create_country(db:Session, country:schemas.Country):

    query_string = "select continent.continent_id from continent" \
                   " join country " \
                   " on country.continent_id = country.continent_id" \
                   f" where continent.name = '{country.continent}'" \
                   " limit 1"
    query = db.execute(query_string)
    values=proxy_to_dictionary(query)

    if len(values) > 0:
        query_string = "insert into country(name,continent_id)" \
                       f" values ('{country.name}',{values[0]['continent_id']})"
        query = db.execute(query_string)
        db.commit()

    print('AAS')


def create_city(db: Session, city: schemas.City):
    
    target_country = db.query(models.Country).filter(models.Country.name == city.country).first()
    if target_country is not None:

        # Query if the city in the same country exists
        same_city=db.query(models.City).filter(models.City.name == city.name).filter(models.City.country_id == target_country.country_id).first()
        if same_city is None:

            db_city = models.City(name=city.name, population=city.population,
                                  no_parks=city.no_parks, no_roads=city.no_roads,
                                  no_trees=city.no_trees, no_hospitals=city.no_hospitals,
                                  country_id=target_country.country_id)
            db.add(db_city)
            db.commit()
            db.refresh(db_city)
            return db_city
        else:
            return {'Error': f'City {city.name} in {city.country} already exists'}
    else:
        return {'Error': f'No such country named {city.country} exists'}