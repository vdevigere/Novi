from sqlalchemy import select
from sqlalchemy.orm import Session

from novi.client.client_base import BaseClient
from novi.client.database import engine
from novi.core.models import Flag


class DbClient(BaseClient):
    def get_flag_by_name(self, flag_name: str) -> Flag:
        stmt = select(Flag).where(Flag.name == flag_name)
        with Session(engine) as session:
            return session.scalars(stmt).unique().first()

    def get_flags(self) -> list[Flag]:
        stmt = select(Flag)
        with Session(engine) as session:
            return list(session.scalars(stmt).unique().fetchall())
