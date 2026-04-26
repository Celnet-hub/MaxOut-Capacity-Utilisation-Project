import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the path to the root directory's .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

class Settings(BaseSettings):
    # Core Application Settings
    PROJECT_NAME: str = "MaxOut Capacity Utilisation Project"
    DATABASE_URL: str
    
    # Middleware 
    MIDDLEWARE_API_URL_NETBOSS: str
    
    # instruct Pydantic to look for the .env file at the root level
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")

# Instantiate it once to be used as a singleton across your app
settings = Settings()