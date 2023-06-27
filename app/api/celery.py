from celery import Celery
from math import radians, sin, cos, sqrt, atan2
from app.api.schemas import Location
from math import sqrt
from typing import List
from app.infrastructure.database import SessionLocal


# Configuración de la cola de tareas de Celery
app = Celery('tasks', broker='amqp://rabbitmq', backend='redis://redis')

# Configuración adicional de Celery
app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC'
)

app.conf.task_routes = {
    'app.api.celery.calculate_distance_task': {'queue': 'celery'},
    'app.api.celery.calculate_distance_haversine_task': {'queue': 'celery'}
}


@app.task
def calculate_distance_task(locations_ids: List[int]) -> float:
    # Realizar el cálculo de la distancia entre las ubicaciones
    session = SessionLocal()
    locations = session.query(Location).filter(Location.id.in_(tuple(locations_ids))).all()
    total_distance = 0.0
    for i in range(len(locations) - 1):
        p = locations[i]
        q = locations[i + 1]
        distance = sqrt((p.latitude - q.latitude) ** 2 + (p.longitude - q.longitude) ** 2)
        total_distance += distance
    session.close()
    return total_distance


@app.task
def calculate_distance_haversine_task(locations_ids: List[int]):
    R = 6371.0  # Earth radius in kilometers

    session = SessionLocal()
    locations = session.query(Location).filter(Location.id.in_(tuple(locations_ids))).all()

    # Verify that there are at least two locations
    if len(locations) < 2:
        raise ValueError("There must be at least two locations")

    total_distance = 0


    for i in range(len(locations) - 1):
        lat1, lon1 = locations[i].latitude, locations[i].longitude
        lat2, lon2 = locations[i + 1].latitude, locations[i + 1].longitude

        # Convert coordinates from degrees to radians
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Difference of longitudes and latitudes
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # Apply Haversine
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        total_distance += distance

    return total_distance