from typing import Annotated

from fastapi import Depends
from aiohttp import ClientSession
from app.db.clickhouse import get_async_session

Session = Annotated[ClientSession, Depends(get_async_session)]
