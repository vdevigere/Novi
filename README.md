# Okapi
## Table of Contents

1. [Concepts](#concepts)
2. [Architecture](#architecture)
  3. [Components](#components)
  4. [Tables](#tables)
  5. [Activations (Implementation and Discovery)](#activations-implementation-and-discovery)

Okapi is a simple yet powerful feature flag and multivariate testing platform built in Python. Okapi is "simple" because all of its core capabilities are built around 2 simple concepts. Flags and Activations


## Concepts
### Flags

**Flags** are associated with features. Flags rely on Activations to determine when to turn on or off features. A flag has three attributes:
- A unique ID which is also the primary key for the flag
- A unique name
- A default status.

If the default status is false, the flag is always turned off, irrespective of how the activations get evaluated.
In the example below the banner_ad is turned on by default, while the 50% discount coupon is always disabled.

| id 	| name         	| status 	|
|----	|--------------	|--------	|
| 1  	| banner_ad    	| true   	|
| 2  	| 50% discount 	| false  	|

### Activations
**Activations** determine the status of the flag. Activations can turn a flag on or off when the activation conditions are met. Activations are what make okapi a **_"dynamic"_** feature flag system. Some scenarios that Activations are useful:-
- Features could be activated depending on the deployment environment such as production, development or test
- Feature could be shown only to certain usernames and disabled for others.
- Organizations may choose to show a feature to only traffic originating from company IP address ranges during testing
- Features may be shown to a percentage of users selected randomly

The list of scenarios can be infinitely varied and complex. An activation has four attributes:-
- A unique ID,
- A descriptive name,
- A python class name that is used to instantiate an activation object
- A configuration

Activation classes are discovered and registered with Okapi using a plugin pattern. Users are expected to provide a folder named "okapi_activations" containing modules and packages with Activation classes. Out of the box Okapi comes with 2 activations:-
- [A Weighted Random Activation]()
- [A Date/Time based Activation]()

Each activation object is passed a configuration at the time of instantiation. Configurations enable the business logic that drives activations. Think of configurations as a free-form column, containing strings (typically json) that can be parsed by the activation logic to build its internal configuration object.
As an example if your activation turns on/off flags for certain users, you may want to provide a list of usernames in the config. The username of the signed-in user at the time of evaluation will be checked against this list of usernames. 

| id 	 | name 	                          | class_name 	                                               | config   	                                                                                                         |
|------|----------------------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 1	   | A weighted random activation     | 	okapi_activations.standard.weighted_random_activation.WeightedRandomActivation  | { "splits":[100, 0, 0], "variations":["A", "B", "C"]}                                        |
| 2	   | A date based activation          | 	okapi_activations.standard.date_time_activation.DateTimeActivation | {"startDateTime":"11/26/2023 12:00 AM","endDateTime":"11/28/2023 12:00 AM","format": "%m/%d/%Y %I:%M %p"} |

See [Creating Activations]() for details on how to create your own custom activations.

## Architecture

### Tables
Okapi captures the details of the above two concepts in just 3 tables: **flags**, **activations** and the association table **flags_activations**. 

The tables can be created manually using [schema.sql](schema.sql) or automatically by setting
`createTables=False` in [okapi.ini](okapi.ini)

### Components

#### okapi.core

The core component that implements the various model classes, the logic to discover and register activations and the logic to evaluate the final flag status, given a list of activations

#### okapi.client

The client component implements the BaseClient interface and two concrete client implementations that retrieve flags and activations from

- Databases (DbClient)
- Remote API endpoint (RemoteClient)

#### okapi.web

The web component implements a simple flask API server to implement two endpoints

- `/flags` - Retrieve all flags
- `/flags/<flag_name>` - Retrieve a specific flag by name

- The web component relies on the DbClient to fetch the flags from a database and expose them via the the `/flags`  resource endpoint


### Implementating Activations

Okapi scans a folder by name "okapi_activations" on the python path and registers all classes inheriting from [BaseActivation](src/okapi/core/__init__.py) found within this folder.

```python
class BaseActivation(object):

    def __init__(self, cfg: Any = None):
        self.config = cfg

    def evaluate(self, context: dict = None) -> bool:
        pass
```
Okapi's power comes from being able to implement pretty much any complex logic within these activation classes. The final status of the flag is determined by ANDing each of the evaluated status
