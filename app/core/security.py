from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=['bcrypt'],
    default='bcrypt',
    bcrypt__rounds=14
)

def hash_password(password : str)->str:
    return pwd_context.hash(password)

def verify_password(password : str, hashed_password : str)->bool:
    return pwd_context.verify(secret=password,hash=hashed_password)
