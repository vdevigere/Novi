import logging

from sqlalchemy import create_engine

from okapi.client import config
from okapi.core.models import Base

url = config.get('database', 'url', fallback='sqlite://')
echo = config.getboolean('database', 'echo', fallback=False)
logging.getLogger(__name__).debug(f"URL: {url}, Echo:{echo}")
engine = create_engine(url, echo=echo)

if config.getboolean('database', 'createTables', fallback=False):
    Base.metadata.create_all(engine)
