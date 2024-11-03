from dns.dnssecalgs import algorithms
from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"

settings = Settings()
print("*********************************8888888", settings.database_hostname)

