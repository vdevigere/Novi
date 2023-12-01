from novi.client.activations import activation_util
from novi.client.activations.base_combination_activation import BaseCombinationActivation
from novi.core import register


@register
class OrActivation(BaseCombinationActivation):
    def evaluate(self, context: dict = None) -> bool:
        return activation_util.or_all_activations(self.config, context)
