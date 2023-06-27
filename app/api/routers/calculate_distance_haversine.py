# FastAPi
from fastapi import status, HTTPException, Depends
from fastapi.responses import JSONResponse
# Model/Schemas
from app.api.schemas import Location, User
# Celery
from app.api.celery import calculate_distance_haversine_task
# Utils
from typing import List
from app.api.dependecies import  get_current_user



async def calculate_distance_haversine(locations_ids: List[int], user: User = Depends(get_current_user)) -> Location:
    """
    Description:
        This is a function used to create task to
        calculate lineal distance between Locatioins records
        in locations_ids list, and returns the
        taskid as a content of JSONResponse.

    Args:
        locations_ids List[int]:
            list of location ids record in database.

    Return:
        task_id:
            id of the task to calculate distance.
    """
    try:
        task = calculate_distance_haversine_task.delay(locations_ids)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"task_id": task.id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
