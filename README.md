# Okapi
## Table of Contents

1. [Concepts](#concepts)
2. [Architecture](#architecture)
  3. [Components](#components)
  4. [Tables](#tables)
  5. [Activations (Implementation and Discovery)](#activations-implementation-and-discovery)

Okapi is a simple yet powerful feature flag and multivariate testing platform built in Python. okapi is "simple" because all of its core
capabilities are built around 2 simple concepts. Flags and Activations


## Concepts
### Flags

**Flags** are associated with features and the **status** of a flag (True or False) can be used to turn on or off
features

### Activations
**Activations** are associated with Flags and determine under what conditions a flag is turned on or off. Activations are
what make okapi a **_"dynamic"_** feature flag system. The status of a flag is not constant and can change if 
certain conditions are met. Some scenarios that Activations are useful in are below:-
- A feature could be turned on or off depending on the environment such as production, development or test it is 
deployed in
- A feature could be shown only to certain usernames and disabled for others.
- Organizations may choose to show a feature to only traffic originating from company IP address ranges during testing
- A feature may be shown to a randomly selected %age of all application or website users.

The list of scenarios can be infinitely varied and can be implemented through Activations.

## Architecture

### Components

#### okapi.core

The core component that implements the various model classes, the logic to discover and register activations and the
logic to evaluate the final flag status, given a list of activations

#### okapi.client

The client component implements the BaseClient interface and two concrete client implementations that retrieve flags and
activations from

- Databases (DbClient)
- Remote API endpoint (RemoteClient)

#### okapi.web

The web component implements a simple flask API server to implement two endpoints

- `/flags` - Retrieve all flags
- `/flags/<flag_name>` - Retrieve a specific flag by name

- The web component relies on the DbClient to fetch the flags from a database and expose them via the the `/flags`
  resource endpoint

### Tables
okapi captures the details of the above two concepts in just 3 tables: **flags**, **activations** and the association table
**flags_activations**. 

The tables can be created manually using [schema.sql](schema.sql) or automatically by setting
`createTables=False` in [okapi.ini](okapi.ini)

#### flags table

The flags table contains 3 columns the:-

- id: The primary key identifier for the flag
- name: A unique name of the flag
- status: The default status of the flag. As you will see later in the document, the status can be made dynamic via
  Activations.

If the default status is false, the flag is always turned off, irrespective of how the activations get evaluated.
In the example below the banner_ad is turned on by default, while the 50% discount coupon is always disabled.

| id 	| name         	| status 	|
|----	|--------------	|--------	|
| 1  	| banner_ad    	| true   	|
| 2  	| 50% discount 	| false  	|

#### activations table
The activations table contains 4 columns: id, name, class_name and config.
- id: The primary key identifier for the activation
- name: A user friendly name  for the activation
- class_name: The name of the python class that will be instantiated and used to evaluate the flag status
- config: Activations may rely on configurations the enable the business logic, for example if your activation turns on 
or off flags for certain users, you may want to provide a list of usernames in the config. The username of the signed-in
user at the time of evaluation will be checked against this list of usernames.

| id 	 | name 	                           | class_name 	                                                 | config 	                           |
|------|----------------------------------|--------------------------------------------------------------|------------------------------------|
| 1	   | A production activation         | 	okapi_activations.env_based_activations.EnvBasedActivation  | {"environment":"prod"}             |
| 2	   | A username based activation      | 	okapi_activations.user_based_activation.UserBasedActivation | {"username":["johndoe","janedoe"]} |
| 3	   | A dev and test activation | 	okapi_activations.env_based_activations.EnvBasedActivation  | {"environment":["dev", "test"]}    |

In the table above there are two activations. The logic of the activations are implemented in two classes:
- okapi_activations.env_based_activations.EnvBasedActivation
- okapi_activations.user_based_activation.UserBasedActivation

They rely on configurations that are represented as json strings, which configure the environment (prod and dev, test)
and usernames (johndoe and janedoe) the activations should check against. **_Note:_** config field can be represented
pretty much in any form, it is left to the implementers of the activation
class to parse the config string and implement the necessary logic

#### flags_activations table
The many-to-many relationship between flags and activations is captured in this association table.

### Activations [Implementation and Discovery]

okapi scans for a package by name "okapi_activations" on the python path and registers all classes within this package
that inherit from [BaseActivation](src/okapi/core/__init__.py).

```python
class BaseActivation(object):

    def __init__(self, cfg: Any = None):
        self.config = cfg

    def evaluate(self, context: dict = None) -> bool:
        pass
```
okapi's power comes from being able to implement pretty much any complex logic within these activation classes. 

If say in the example above the "banner ad" feature above were to be associated with activation ids 1 and 2
okapi will search for a package named "okapi_activations" on the python path and search within it for classes with the 
fully qualified names
- `okapi_activations.env_based_activations.EnvBasedActivation` 
- `okapi_activations.user_based_activation.UserBasedActivation`

and instantiates these classes by passing in the config values in the form of JSON to the constructor. The config is
read from the database table

- `{"environment":"prod"}`
- `{"username":["johndoe","janedoe"]}`

The final status of the flag is determined by ANDing each of the evaluated status