import logging
import pkgutil
from abc import ABC, abstractmethod
from importlib import import_module
from inspect import isclass
from typing import Any

import novi_activations

logging.getLogger(__name__).addHandler(logging.NullHandler())


class BaseActivation(ABC):

    def __init__(self, cfg: Any = None):
        self.config = cfg

    @abstractmethod
    def evaluate(self, context: dict = None) -> bool:
        pass


def iter_namespace(ns_pkg):
    logging.getLogger(__name__).debug(f"Path:{ns_pkg.__path__}, Name:{ns_pkg.__name__}")
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def find_activations(ns_pkg) -> dict[str, type[BaseActivation]]:
    found_activations = dict[str, type[BaseActivation]]()
    # iterate through the modules in the current package
    for (finder, module_name, ispkg) in iter_namespace(ns_pkg):
        if ispkg:
            found_activations = found_activations | find_activations(import_module(module_name))
        # import the module and iterate through its attributes
        logging.getLogger(__name__).debug(f"Module Name:{module_name}")
        module = import_module(module_name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (isclass(attribute)
                    and issubclass(attribute, BaseActivation)
                    and attribute != BaseActivation):
                # Add the class to this package's variables
                qualified_class_name = f"{attribute.__module__}.{attribute.__name__}"
                found_activations[qualified_class_name] = attribute
    return found_activations


discovered_activations: dict[str, type[BaseActivation]] = find_activations(novi_activations)


def register(func):
    logging.getLogger(__name__).debug(f"Registering activation: {func.__module__}.{func.__name__}")
    discovered_activations[f"{func.__module__}.{func.__name__}"] = func
    return func
