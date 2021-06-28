from time import sleep
from celery import Celery
from celery.utils.log import get_task_logger
from vector_ai_app.database import celery_session
from vector_ai_app.crud import create_city, create_country, remove_city, update_city, create_continent

celery = Celery('tasks')
celery_log = get_task_logger(__name__)


@celery.task
def create_city_celery(city):
    create_city(celery_session, city)


@celery.task
def remove_city_celery(city_to_remove):
    remove_city(celery_session, city_to_remove)


@celery.task
def update_city_celery(city_to_update):
    update_city(celery_session, city_to_update)


@celery.task
def create_country_celery(country):
    print(country)
    create_country(celery_session, country)


@celery.task
def create_continent_celery(continent):
    create_continent(celery_session, continent)






