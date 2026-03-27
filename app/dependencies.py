from app.db.session import AsyncSession, AsyncSessionLocal
from fastapi import Depends, status
from typing import AsyncGenerator
from fastapi import HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.schemas.user import Payload
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.schemas.user import UserInfo
from sqlalchemy import select
from app.models.user import User

async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        try:
            print("DB Connection has Established")
            yield session
        except HTTPException:
            raise
        except Exception:
            await session.rollback()
            raise

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", scheme_name="jwt")

async def get_profile(user_token: Annotated[str,Depends(oauth2_scheme)],db : Annotated[AsyncSession, Depends(get_db)])->UserInfo:
    try:
        payload = Payload(**jwt.decode(user_token,key=settings.ACCESS_TOKEN_SECRET,algorithms=["HS256"]))

        if payload.type != "access":
            raise InvalidTokenError
        
        result = await db.execute(select(User).where(User.id==payload.sub))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )

        return UserInfo(**{
            "id" : user.id,
            "email": user.email,
            "role" : user.role
        })
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token Expired",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token provided",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
