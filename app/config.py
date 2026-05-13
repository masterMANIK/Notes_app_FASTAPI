from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Notes API"
    
    # Database Settings
    DATABASE_URL: str
    
    # Security Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # This tells Pydantic to read variables from our .env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a global instance of settings to use throughout the app
settings = Settings()
