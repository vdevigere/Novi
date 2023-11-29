import logging

from sqlalchemy import create_engine

from novi.client import config

url = config.get('database', 'url', fallback='sqlite:///novi.db')
echo = config.getboolean('database', 'echo', fallback=False)
logging.getLogger(__name__).debug(f"URL: {url}, Echo:{echo}")
engine = create_engine(url, echo=echo)
