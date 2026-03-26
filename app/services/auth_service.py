from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.core.security import hash_password, verify_password

async def create_user(user_data : UserCreate, db : AsyncSession):
    hashed_password = {
        "hashed_password" : hash_password(user_data.password)
    }
    user_obj = User(**user_data.model_dump(exclude={'password'}),**hashed_password)

    try:
        # Add the user_obj in the Session
        db.add(user_obj)
        # Commit the user_obj to the Database
        await db.commit()
        # Refresh the user_obj
        await db.refresh(user_obj)
        
        return user_obj
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occured !"
        )
