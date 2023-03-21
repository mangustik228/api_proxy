import schema
from sqlalchemy.orm import Session
from database import models


def add_item_to_db(item: schema.proxy.ProxyPost, db: Session):
    db_item = models.Proxy(**item.dict())
    print(item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item