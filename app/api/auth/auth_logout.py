# import sqlalchemy as sa
# from fastapi import Depends, Response
# from fastapi.exceptions import HTTPException
# from pydantic import BaseModel

# from app.models.user_login import UserLogin
# from app.dependencies.get_db_session import get_db_session


# class LogoutData(BaseModel):
#     refresh_token: str


# async def auth_logout(data: LogoutData, session=Depends(get_db_session)):
#     pass
#     result = session.execute(
#         sa.delete(UserLogin).where(
#             UserLogin.refresh_token == data.refresh_token)
#     )

#     if result.rowcount == 0:
#         raise HTTPException(400, 'Refresh token not found')

#     session.commit()

#     return Response(status_code=204)


import sqlalchemy as sa
from fastapi import Depends, HTTPException, Response
import logging
from pydantic import BaseModel

from app.models.user_login import UserLogin
from app.dependencies.get_db_session import get_db_session


# Request model for logout data (refresh token)
class LogoutData(BaseModel):
    refresh_token: str


# Configure logging to capture more detailed errors
logger = logging.getLogger(__name__)


# Logout function to invalidate a user's refresh token
async def auth_logout(data: LogoutData, session=Depends(get_db_session)):
    try:
        logger.info(f"Attempting logout for refresh_token: {data.refresh_token}")

        # Delete the user login entry with the provided refresh token
        result = session.execute(
            sa.delete(UserLogin).where(UserLogin.refresh_token == data.refresh_token)
        )

        # Log the result of the deletion
        logger.info(f"Rows affected by deletion: {result.rowcount}")

        # If no rows were deleted, refresh token wasn't found
        if result.rowcount == 0:
            logger.error(
                f"Refresh token {data.refresh_token} not found in the database."
            )
            raise HTTPException(status_code=400, detail="Refresh token not found")

        # Commit the transaction
        session.commit()
        logger.info(f"Refresh token {data.refresh_token} successfully logged out.")

        # Return a 204 No Content status to indicate successful logout
        return Response(status_code=204)

    except Exception as e:
        # In case of any error, rollback the transaction and raise an HTTPException
        session.rollback()
        logger.error(
            f"Error during logout: {str(e)}", exc_info=True
        )  # Log full exception details
        raise HTTPException(status_code=500, detail=f"Error during logout: {str(e)}")
