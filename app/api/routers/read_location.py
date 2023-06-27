# FastAPi
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# Model/Schemas
from app.api.schemas import Location, User
# Utils
from sqlalchemy.exc import SQLAlchemyError
from app.api.dependecies import get_session, get_current_user


async def read_location(location_id: int, session=Depends(get_session), user: User = Depends(get_current_user)) -> Location:
    """
    Description:
        This is a function used to read
        a Locatioin by id record in the database,
        and returns of Location object
        as a content of JSONResponse.

    Args:
        location_id (int):
            id of location record in database.

    Raises:
        SQLAlchemyError:
            If there is an error when adding the location
            to the session or committing the transaction,
            an HTTPException with a status code of 500 and details of the error is raised.
    Return:
        location Location:
            Location objects
    """
    try:
        location = session.query(Location).filter(Location.id == location_id).first()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(location)
        )
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
