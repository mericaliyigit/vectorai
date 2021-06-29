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

    return results


def update_city(db:Session, city_to_update):

    city=schemas.UpdateCity.parse_obj(city_to_update)
    the_country = db.query(models.Country).filter(models.Country.name == city.country).first()

    if the_country is not None:

        the_city = db.query(models.City).filter(models.City.name == city.name).\
            filter(models.City.country_id == the_country.country_id).first()

        # We have found the city in the db we are updating it
        if the_city is not None:
            if city.population is not None:
                the_city.population = city.population
            if city.area is not None:
                the_city.area = city.area
            if city.no_parks is not None:
                the_city.no_parks = city.no_parks
            if city.no_roads is not None:
                the_city.no_roads = city.no_roads
            if city.no_trees is not None:
                the_city.no_trees = city.no_trees
            if city.no_hospitals is not None:
                the_city.no_hospitals = city.no_hospitals
            db.commit()
            return True
        else:
            return False


def remove_city(db:Session, city_to_remove):

    city = schemas.RemoveCity.parse_obj(city_to_remove)

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


def proxy_to_dictionary(result_proxy):
    return [dict(row) for row in result_proxy]


def get_all_continents(db:Session):
    query_string = "select continent.name as continent_name, sum(population) as population, sum(area) as total_area," \
                   "sum(no_roads) as total_roads , sum(no_parks) as total_parks," \
                   "sum(no_trees) as total_trees" \
                   " from" \
                   " continent full join country" \
                   " on continent.continent_id = country.continent_id" \
                   " full join city" \
                   " on country.country_id = city.country_id" \
                   " group by continent.name" \
                   " order by continent_name"
    query = db.execute(query_string)
    results = proxy_to_dictionary(query)
    return results


def get_all_countries(db:Session):

    query_string = "select country.name as country_name, sum(population) as population, sum(area) as total_area," \
            "sum(no_roads) as total_roads , sum(no_parks) as total_parks," \
            "sum(no_trees) as total_trees" \
            " from" \
            " country full join city" \
            " on country.country_id = city.country_id" \
            " group by country.name" \
            " order by country_name" \

    query = db.execute(query_string)
    results = proxy_to_dictionary(query)
    return results


def create_country(db:Session, new_country):

    country=schemas.Country.parse_obj(new_country)

    query_string = "select continent_id from" \
                   f" continent where continent.name = '{country.continent}'"

    query = db.execute(query_string)
    values = proxy_to_dictionary(query)

    if len(values) > 0:
        query_string = "insert into country(name,continent_id)" \
                       f" values ('{country.name}',{values[0]['continent_id']})"
        query = db.execute(query_string)
        db.commit()


def create_city(db: Session, city):

    city = schemas.City.parse_obj(city)

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


def create_continent(db:Session, new_continent):

    continent = schemas.Continent.parse_obj(new_continent)

    new_continent = models.Continent(name=continent.name)
    db.add(new_continent)
    db.commit()



