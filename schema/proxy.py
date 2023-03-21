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
    data: ProxyBd


class ProxyGet(TokenCheck):
    expire: date = (date.today() + timedelta(days=1))
    active: bool = True
    type: Literal['string', 'dict[str,str]', 'dict[str,list]'] = 'string'



