from dotenv import load_dotenv
import os 
from dataclasses import dataclass
from configparser import ConfigParser

_config = ConfigParser()
_config.read('config/config.ini')


load_dotenv()

# Токен используемой на проверку свои или не свои обращаються к API

@dataclass
class DatabaseConfig:
    url: str = _config.get('DATABASE', 'url')


@dataclass
class Config:
    token: int = int(os.getenv('token'))
    db: DatabaseConfig = DatabaseConfig()

config = Config()