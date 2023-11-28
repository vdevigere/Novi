import json
import random

from novi.core import BaseActivation


class WeightedRandomActivation(BaseActivation):
    def __init__(self, cfg: str = None):
        configuration = json.loads(cfg)

        if ({'splits', 'variations'} <= configuration.keys()
                and len(configuration['splits']) == len(configuration['variations'])):
            super().__init__(configuration)

    def evaluate(self, context: dict = None) -> bool:
        if {'seed', 'variant'} <= context.keys():
            random.seed(context.get('seed'))
            choice = random.choices(self.config['variations'], weights=self.config['splits'])
            return choice[0] == context.get('variant')
        else:
            return False
