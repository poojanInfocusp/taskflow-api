from fastapi import HTTPException, status, Response
from app.schemas.user import UserCreate, UserLoginRquest, UserLoginResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from sqlalchemy import Select, Update, Values
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import datetime, timezone, timedelta

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
    

async def login(user : UserLoginRquest, db : AsyncSession, response : Response):
    try:
        result =await db.execute(Select(User).where(User.email == user.email))
        myUser = result.scalars().first()


        if myUser is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        #Verify the Password
        if not verify_password(password=user.password,hashed_password=myUser.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Email or Password"
            )

        # Generate the Access_token
        access_token_expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=20)
        access_token = create_access_token(
            {
                "sub" : str(myUser.id),
                "email" : (myUser.email),
                "exp" : (access_token_expiry),
                "type" : "access",
                "role" : myUser.role
            }
        )

        # Generate the refresh_token
        refresh_token_expiry = datetime.now(tz=timezone.utc) + timedelta(days=7)
        refresh_token = create_refresh_token(
            {
                "sub" : str(myUser.id),
                "email" : (myUser.email),
                "exp" : (refresh_token_expiry),
                "type" : "refresh",
                "role" : myUser.role
            }
        )

        #Store the JWT in the db.
        await db.execute(Update(User).where(User.email == myUser.email).values(refresh_token=refresh_token))

        await db.commit()

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=7*24*60*60,
            samesite="lax",
            httponly=True,
            secure=True
        )

        result = UserLoginResponse(
            access_token=access_token,
            token_type="access",
            user=myUser
        )

        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error Occured"
        )