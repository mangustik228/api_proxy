import json
from pydantic import BaseModel, validator
import re
from typing import Optional, Literal
from datetime import date, timedelta, datetime

class TokenCheck(BaseModel):
    token: int

class ProxyBd(BaseModel):
    server: str
    username: str
    password: str
    port: int
    expire: date | datetime 
    service: Optional[str]

    @validator('server')
    def valid_server(cls, v):
        try:
            return re.findall(r'\d+\.\d+\.\d+\.\d+', v)[0]
        except:
            raise ValueError(f'Uncorrect field "server": {v}')
        
   
class ProxyPost(TokenCheck):
    data: list[ProxyBd]


class ProxyGet(TokenCheck):
    expire: date = (date.today() + timedelta(days=1))
    type: Literal['string', 'dict[str,str]', 'playwright'] = 'string'


class ProxyGetResponse(BaseModel):
    password: str 
    server: str 
    username: str 
    port: int 

    class Config:
        orm_mode = True

    def string_val(self):
        return {
            'http':f'http://{self.username}:{self.password}@{self.server}:{self.port}',
            'https':f'https://{self.username}:{self.password}@{self.server}:{self.port}',
            }
    
    def dict_str_str(self):
        return { 
            'server':f'http://{self.server}:{self.port}',
            'username':f'{self.username}',
            'password':f'{self.password}'
        }

    def dict_playwright(self):
        return {
            "proxy": {
                'server':f'http://{self.server}:{self.port}',
                'username':f'{self.username}',
                'password':f'{self.password}'
            }
        }   


class ProxyUpdate(ProxyBd):
    id: int 
    server: Optional[str]
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]
    expire: Optional[date | datetime] 
    service: Optional[str]


    