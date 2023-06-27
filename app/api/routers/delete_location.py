# FastAPi
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# Model/Schemas
from app.api.schemas import Location, User
# Utils
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.api.dependecies import get_session, get_current_user


async def delete_location(location_id: int, session=Depends(get_session), user: User = Depends(get_current_user)) -> Location:
    """
    Description:
        This is a function used to delete
        a Locatioin by id record in the database.

    Args:
        location_id (int):
            id of location record in database.

    Raises:
        SQLAlchemyError:
            If there is an error when adding the location
            to the session or committing the transaction,
            an HTTPException with a status code of 500 and details of the error is raised.
    Return:
        successfull message
    """
    try:
        location = session.query(Location).filter(Location.id == location_id).one()
        session.delete(location)
        session.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Location deleted successfully"
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
