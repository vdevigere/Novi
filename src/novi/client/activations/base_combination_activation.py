import json
import logging
from abc import abstractmethod

from novi.client import flag
from novi.core import BaseActivation


class BaseCombinationActivation(BaseActivation):

    def __init__(self, config: str = None):
        logging.getLogger(__name__).debug(f"{self.__module__} = {self.__class__}")
        activationIds: list[int] = json.loads(config)
        super().__init__(flag.get_activation_by_ids(activationIds))

    @abstractmethod
    def evaluate(self, context: dict = None) -> bool:
        pass
