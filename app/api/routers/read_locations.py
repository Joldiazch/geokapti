# FastAPi
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# Model/Schemas
from app.api.schemas import Location, User
# Utils
from sqlalchemy.exc import SQLAlchemyError
from app.api.dependecies import get_session, get_current_user


async def read_locations(session=Depends(get_session), user: User = Depends(get_current_user)) -> Location:
    """
    Description:
        This is a function used to read
        all Locatioins records in the database,
        and returns the list of Location objects
        as a content of JSONResponse.

    Raises:
        SQLAlchemyError:
            If there is an error when adding the location
            to the session or committing the transaction,
            an HTTPException with a status code of 500 and details of the error is raised.
    Return:
        locations List(Location):
            list of Location objects
    """
    try:
        locations = session.query(Location).all()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(locations)
        )
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
