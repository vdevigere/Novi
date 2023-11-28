import functools
import logging
from abc import ABC, abstractmethod
from typing import Any

from okapi.core import discovered_activations
from okapi.core.composite_and_activation import CompositeAndActivation
from okapi.core.models import Flag


class BaseClient(ABC):
    @abstractmethod
    def get_flag_by_name(self, flag_name: str) -> Flag:
        pass

    @abstractmethod
    def get_flags(self) -> list[Flag]:
        pass

    @classmethod
    def is_enabled(cls, flag_name: str, context: Any = None) -> bool:
        flag: Flag = cls().get_flag_by_name(flag_name=flag_name)
        if flag is not None:
            logging.getLogger(__name__).debug(f"Flag Name: {flag.name}, Status: {flag.status}")
            logging.getLogger(__name__).debug(f"Discovered Activations: {discovered_activations}")
            logging.getLogger(__name__).debug(f"Associated Activations: {flag.activations}")
            evaluated_status = flag.status and CompositeAndActivation(flag.activations).evaluate(context)
            logging.getLogger(__name__).debug(f"CompositeAndActivation = {evaluated_status}")
            return evaluated_status
        else:
            return False

    @classmethod
    def enabled(cls, flag_name: str, context: Any = None):
        def decorator_enabled(func):
            @functools.wraps(func)
            def wrapper_enabled(*args, **kwargs):
                return func(*args, **kwargs) if cls.is_enabled(flag_name, context) else None

            return wrapper_enabled

        return decorator_enabled
