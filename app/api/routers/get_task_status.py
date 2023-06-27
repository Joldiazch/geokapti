# FastAPi
from fastapi import status, HTTPException, Depends
from fastapi.responses import JSONResponse
# Celery
from celery.result import AsyncResult
# Model/Schemas
from app.api.schemas import User
# Utils
from app.api.dependecies import get_current_user


async def get_task_status(task_id: str, user: User = Depends(get_current_user)) -> float:
    """
    Description:
        This is a function used to get result task to
        calculate lineal distance between Locatioins records,
        and returns the distance as a content of JSONResponse.

    Args:
        task_id str:
            task id to get result.
    """
    try:
        result = AsyncResult(task_id)
        value = result.get() if result.ready() else None
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": result.status, "result": value}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
