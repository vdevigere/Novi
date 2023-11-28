import logging
from typing import Dict

from novi.core import BaseActivation, discovered_activations
from novi.core.models import Activation


class CompositeAndActivation(BaseActivation):
    """
    Iterate through each of the activations in the list to evaluate the status, AND all statuses together
    and return the results
    """

    def __init__(self, config: list[Activation] = None):
        super().__init__(config)

    def evaluate(self, context: Dict = None) -> bool:
        status = True
        for activation in self.config:
            if activation.class_name in discovered_activations:
                logging.getLogger(__name__).debug(f"Applying Activation: {activation.name}")
                obj: BaseActivation = discovered_activations[activation.class_name](activation.config)
                evaluated_status = obj.evaluate(context)
                logging.getLogger(__name__).debug(f"Status Before Eval {status}")
                status = status and evaluated_status
                logging.getLogger(__name__).debug(f"Status After AND with {evaluated_status} = {status}")
        return status
