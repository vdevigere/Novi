# Novi
Novi is a simple yet powerful [feature flag](https://en.wikipedia.org/wiki/Feature_toggle) platform built in Python. Novi is "simple" because all of its core capabilities are built around 2 simple concepts. 
- Flags
- and Activations

## Concepts
### Flags
**Flags** are associated with features. Flags turn a feature on or off. The on/off status of a flag is determined by Activations. 
Details about flags are store in the Flag table, which has 3 columns
- A unique ID which is also the primary key for the flag
- A unique name
- A default status.
If the default status is false, the flag is always turned off, irrespective of how the activations get evaluated.

|id| name                              |status|
|---|-----------------------------------|-----|
|1| Date and Random Activated Feature |1|
|2| Random Variant Feature            |1|
|3| Combo AND                         |1|
|4| Combo OR                          |1|

### Activations
**Activations** determine the on/off status of a flag when specific conditions are met. 
Activations are what make novi a **_"dynamic"_** feature flag system, as the runtime conditions are evaluated against an Activations trigger logic
to set the flag status. Some scenarios that Activations are useful:-
- Features could be activated depending on the deployment environment such as production, development or test
- Feature could be shown only to certain usernames and disabled for others.
- Organizations may choose to show a feature to only traffic originating from company IP address ranges during testing
- Features may be shown to a percentage of users selected randomly

The list of scenarios can be infinitely varied and complex. An activation table has four columns:-
- A unique ID,
- A descriptive name,
- A python class name that is used to instantiate an activation object
- A configuration 

|id|name|class_name|config|
|---|-----|-----|----|
|1|Date Activated|novi.client.activations.date_time_activation.DateTimeActivation|{"startDateTime":"11/26/2023 12:00 AM","endDateTime":"11/28/2023 12:00 AM","format": "%m/%d/%Y %I:%M %p"}|
|2|Random Split Activated|novi.client.activations.weighted_random_activation.WeightedRandomActivation|{ "splits":[100, 0, 0], "variations":["A", "B", "C"]}|
|3|Combo AND Activation|novi.client.activations.and_activation.AndActivation|[1,2]|
|4|Combo OR Activation|novi.client.activations.or_activation.OrActivation|[1,2]|

Activation classes are discovered and registered with Novi using two approaches, users can choose which ever is more convenient:- 
- Using the novi_activations folder - Any python modules or packages found in the novi_activations folder on the PYTHON_PATH will be registered as an activation
- Using the @register annotation - Activation classes can be annotated with @register to indicate to Novi to register the class as an activation.

For a class to be considered as a valid Activation class it should inherit from the Abstract base class [BaseActivation](src/novi/core/__init__.py).

Out of the box novi comes with a few activations:-
- [A Weighted Random Activation](src/novi/client/activations/weighted_random_activation.py)
- [A Date/Time based Activation](src/novi/client/activations/date_time_activation.py)
- [AND a list of Activations](src/novi/client/activations/and_activation.py)
- [OR a list of Activations](src/novi/client/activations/or_activation.py)

At the time of instantiation Novi passes the data from the configuration column to the class constructor. 
Configurations enable the business logic that drives activations. The configuration field provides the parameters necessary to do the evaluation, 
in the example of date range check, it could be the start and end date. Think of configurations as a free-form column, containing strings (typically json) 
that can be parsed by the Activation class to build its internal configuration object. Please ee [Creating Activations]() for details on how to create your own custom activations.

### Relationship between Flags and Activations
A given flag can have multiple activations and similarly a given activation can be associated with multiple flags (many to many)
This relationship is captured in the flags_activations table

|flag_id|activation_id|
|-----|---|
|1|1|
|1|2|
|2|2|
|3|3|
|4|4|


## Architecture

![](Novi%20Architecture.png)
### Components

#### novi.core

The core component implements the logic to discover and register activations

#### novi.client

The client component uses SQLAlchemy to retrieve the flags from any supported relational database and evaluates the status of a flag's associated activations

#### novi.web

The web component implements a simple flask API server to implement 4 endpoints

Retrieve the original flag status as defined in the database
- `[GET] /flags` - Retrieve all flags
- `[GET] /flags/<flag_name>` - Retrieve a specific flag by name

Retrieve the evaluated flag status
- `[POST] /evaluatedFlags`
- `[POST] /evaluatedFlags/<flag_name>`


### Implementing Activations

Novi scans a folder by name "novi_activations" on the python path and registers all classes inheriting from [BaseActivation](src/novi/core/__init__.py) found within this folder.

```python
class BaseActivation(object):

    def __init__(self, cfg: Any = None):
        self.config = cfg

    def evaluate(self, context: dict = None) -> bool:
        pass
```
Novi's power comes from being able to implement pretty much any complex logic within these activation classes. 
A flag can be associated with multiple activations:- 
#### Row Based Association
If the association is expressed as a many-to-many relationship in the flags_activations tables the status of evaluating each activation is 'AND'ed with the others to calculate the final status.
In the example above `Date and Random Activated Feature` (id=1) is associated with 2 activations Date based and Random weight as capture in the 
flags_activations table.
#### A List of Activations
Flags can also be associated with Activations by inheriting from `BaseCombinationActivation` class

```python
class BaseCombinationActivation(BaseActivation):

    def __init__(self, config: str = None):
        logging.getLogger(__name__).debug(f"{self.__module__} = {self.__class__}")
        activationIds: list[int] = json.loads(config)
        super().__init__(flag.get_activation_by_ids(activationIds))

    @abstractmethod
    def evaluate(self, context: dict = None) -> bool:
        pass

```
This approach gives implementers more fine grained ability to control how the final status of the flag is calculated.
Rows 3 and 4 in the Activation table shown above are an example of ComboActivations, the configuration column is a list of activations that need to be combined
They activations can be combined using any custom logic implemented in the `def evaluate(..)` method

# Installation and Usage

## Installation

```pip install novi```

## Usage

There are a few ways to check the status of a flag and turn on/of features.

### Using novi.client

The `novi.client.flag` retrieves feature flags from a database. Novi uses sqlalchemy to query from a variety of
databases.

#### Configuration

Before you query a database, you need to tell Novi how to connect to your database. This is done in novi.ini.
An example file is [here](../../../novi.ini). To create the tables you can either run the DDL SQL from the
file [schema.sql](../../../schema.sql) or use the `novi.web`. Instructions to create and seed the table using the [sample_data.sql](sample_data.sql)
script are [here](src/novi/web/README.md).

Once the tables are created and seeded with your feature flag data. You can either use the decorator or the is_enabled
method to check the status of a feature flag using it's name. The example python file demonstrates both ways

```python
import logging.config
from novi.client import flag

dateToTest = "11/26/2023 12:00 AM"


@flag.enabled("Date Activated Feature", {
    'currentDateTime': dateToTest
})
def date_based_activated_func():
    print(f"Feature active as of {dateToTest}")


# Only the variationA will be evaluated as the split is [100,0, 0] in the database
#
@flag.enabled("Random Variant Feature", {
    "seed": 333,
    "variant": "A"
})
def variationA():
    print('variation A')


@flag.enabled("Random Variant Feature", {
    "seed": 333,
    "variant": "B"
})
def variationB():
    print('variation B')


def variationC():
    print('variation C')


if __name__ == '__main__':
    logging.config.fileConfig("logging.conf")
    date_based_activated_func()
    variationA()
    variationB()
    if flag.is_enabled("Random Variant Feature", {
        "seed": 333,
        "variant": "C"
    }):
        variationC()
```

Given the sample tables as shown above

The output will be

```commandline
Feature active as of 11/26/2023 12:00 AM
variation A
```
