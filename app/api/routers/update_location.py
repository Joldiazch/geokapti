# FastAPi
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# Model/Schemas
from app.api.schemas import LocationBase, Location, User
# Utils
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.api.dependecies import get_session, get_current_user


async def update_location(location_id: int, location: LocationBase, session=Depends(get_session), user: User = Depends(get_current_user)) -> Location:
    """
    Description:
        This is a function used to updated
        Locatioin record in the database by location_id,
        and returns the of Location objects updated
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
        locations List(Location):
            list of Location objects
    """
    try:
        existing_location = session.query(Location).filter(Location.id == location_id).one()
        for attr in ('name', 'latitude', 'longitude'):
            if value := getattr(location, attr, None):
                setattr(existing_location, attr, value)

        existing_location.changed_by = user.username
        session.commit()
        session.refresh(existing_location)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(existing_location)
        )
    except NoResultFound as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
