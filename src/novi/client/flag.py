import functools
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from novi.client.database import engine
from novi.core import discovered_activations
from novi.core.composite_and_activation import CompositeAndActivation
from novi.core.models import Flag


def do_evaluation(flag: Flag, context: dict) -> Flag:
    if flag is not None:
        logging.getLogger(__name__).debug(f"Flag Name: {flag.name}, Status: {flag.status}")
        logging.getLogger(__name__).debug(f"Discovered Activations: {discovered_activations}")
        logging.getLogger(__name__).debug(f"Associated Activations: {flag.activations}")
        flag.status = flag.status and CompositeAndActivation(flag.activations).evaluate(context)
        logging.getLogger(__name__).debug(f"CompositeAndActivation = {flag.status}")
    return flag


def get_flag_by_name(flag_name: str, context: dict, evaluate: bool = False) -> Flag:
    stmt = select(Flag).where(Flag.name == flag_name)
    with Session(engine) as session:
        flag = session.scalars(stmt).unique().first()
        return do_evaluation(flag, context) if evaluate else flag


def get_flags(context: dict, evaluate: bool = False) -> list[Flag]:
    stmt = select(Flag)
    with Session(engine) as session:
        flags = list(session.scalars(stmt).unique().fetchall())
        return list(map(lambda flag: do_evaluation(flag, context), flags)) if evaluate else flags


def is_enabled(flag_name: str, context: dict = None) -> bool:
    flag: Flag = get_flag_by_name(flag_name=flag_name, context=context, evaluate=True)
    return flag.status


def enabled(flag_name: str, context: dict = None):
    def decorator_enabled(func):
        @functools.wraps(func)
        def wrapper_enabled(*args, **kwargs):
            return func(*args, **kwargs) if is_enabled(flag_name, context) else None

        return wrapper_enabled

    return decorator_enabled
