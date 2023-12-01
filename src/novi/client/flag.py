import functools
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from novi.client.activations import activation_util
from novi.client.database import engine
from novi.core.models import FlagModel, ActivationModel


def evaluate_flag(flag: FlagModel, context: dict) -> FlagModel:
    if flag is not None:
        logging.getLogger(__name__).debug(f"Flag Name: {flag.name}, Status: {flag.status}")
        logging.getLogger(__name__).debug(f"Associated Activations: {flag.activations}")
        flag.status = flag.status and activation_util.and_all_activations(flag.activations, context)
    return flag


def get_flag_by_name(flag_name: str, context: dict = None, evaluate: bool = False) -> FlagModel:
    stmt = select(FlagModel).where(FlagModel.name == flag_name)
    with Session(engine) as session:
        flag = session.scalars(stmt).unique().first()
        return evaluate_flag(flag, context) if evaluate else flag


def get_flags_by_ids(flag_ids: list[int], context: dict = None, evaluate: bool = False) -> list[FlagModel]:
    stmt = select(FlagModel).where(FlagModel.id.in_(flag_ids))
    with Session(engine) as session:
        flags = list(session.scalars(stmt).unique().fetchall())
        return list(map(lambda flag: evaluate_flag(flag, context), flags)) if evaluate else flags


def get_flags(context: dict = None, evaluate: bool = False) -> list[FlagModel]:
    stmt = select(FlagModel)
    with Session(engine) as session:
        flags = list(session.scalars(stmt).unique().fetchall())
        return list(map(lambda flag: evaluate_flag(flag, context), flags)) if evaluate else flags


def get_activation_by_ids(activation_ids: list[int]) -> list[ActivationModel]:
    stmt = select(ActivationModel).where(ActivationModel.id.in_(activation_ids))
    with Session(engine) as session:
        return list(session.scalars(stmt).unique().fetchall())


def is_enabled(flag_name: str, context: dict = None) -> bool:
    flag: FlagModel = get_flag_by_name(flag_name=flag_name, context=context, evaluate=True)
    return flag.status


def enabled(flag_name: str, context: dict = None):
    def decorator_enabled(func):
        @functools.wraps(func)
        def wrapper_enabled(*args, **kwargs):
            return func(*args, **kwargs) if is_enabled(flag_name, context) else None

        return wrapper_enabled

    return decorator_enabled
