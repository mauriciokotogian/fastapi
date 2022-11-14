from pydantic import BaseSettings


# checks all env variables are set and in the correct type
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str = "postgres"
    secret_key: str 
    access_token_expire_in_minutes: int
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()
