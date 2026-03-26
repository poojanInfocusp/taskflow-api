from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url : str = ""
    ACCESS_TOKEN_SECRET : str = ""
    REFRESH_TOKEN_SECRET : str = ""
    
    model_config = SettingsConfigDict(env_file=".env",case_sensitive=False)

settings = Settings()
