# FastAPi
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# Model/Schemas
from app.api.schemas import Location, LocationBase, User
# Utils
from sqlalchemy.exc import SQLAlchemyError
from app.api.dependecies import get_session, get_current_user


async def create_location(location: LocationBase, session=Depends(get_session), user: User = Depends(get_current_user)) -> Location:
    """
    Description:
        This is a function used to create a new
        location record in a database by taking in a Location object.
        It uses SQLAlchemy to interact with the database,
        and returns the created Location object as a JSONResponse.

    Args:
        location (Location):
            This is the Location object that contains
            the information needed to create a new location record in the database.
    Raises:
        SQLAlchemyError:
            If there is an error when adding the location
            to the session or committing the transaction,
            an HTTPException with a status code of 500 and details of the error is raised.
    Return:
        Location:
            The newly created Location object
            is returned as a JSONResponse with a status code of 200.
    """
    try:
        location_data = jsonable_encoder(location)
        location_data |= {
            "added_by": user.username,
            "user": user
        }
        location = Location(**location_data)
        session.add(location)
        session.commit()
        session.refresh(location)
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
