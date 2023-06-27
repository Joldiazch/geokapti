# FastApi
from fastapi import APIRouter
# Routes
from .create_location import create_location
from .read_locations import read_locations
from .read_location import read_location
from .update_location import update_location
from .delete_location import delete_location
from .calculate_distance import calculate_distance
from .calculate_distance_haversine import calculate_distance_haversine
from .get_task_status import get_task_status

from .token import login_for_access_token
from .register_user import register_user


location_router = APIRouter(tags=["Location"])

location_router.add_api_route('/create_location/', endpoint=create_location, methods=['POST'])
location_router.add_api_route('/read_locations/', endpoint=read_locations, methods=['GET'])
location_router.add_api_route('/read_location/', endpoint=read_location, methods=['GET'])
location_router.add_api_route('/update_location/', endpoint=update_location, methods=['PUT'])
location_router.add_api_route('/delete_location/', endpoint=delete_location, methods=['DELETE'])
location_router.add_api_route('/calculate_distance/', endpoint=calculate_distance, methods=['POST'])
location_router.add_api_route('/calculate_distance_haversine/', endpoint=calculate_distance_haversine, methods=['POST'])
location_router.add_api_route('/get_task_status/', endpoint=get_task_status, methods=['GET'])

auth_router = APIRouter(tags=["auth"])

auth_router.add_api_route('/token/', endpoint=login_for_access_token, methods=['POST'])
auth_router.add_api_route('/register_user/', endpoint=register_user, methods=['POST'])