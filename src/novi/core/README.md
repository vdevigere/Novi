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
file [schema.sql](../../../schema.sql) or set createTables=True.

Once the tables are created and seeded with your feature flag data. You can either use the decorator or the is_enabled
method to check the status of a feature flag using it's name. The example python file demonstrates both ways

```python
from novi.client import flag


@flag.enabled("Feature B")
def hello_decorator_with_return():
    return "Decorator on method with return!!!!"


def hello_world():
    print("Hello World!!!")


@flag.enabled("Feature C")
def hello_decorator():
    print("Decorator on method with no return")


if __name__ == '__main__':
    if flag.is_enabled("Feature A"):
        hello_world()

    print(hello_decorator_with_return())
    hello_decorator()
```

If the feature table has the following data:

| id | name      | status |
|----|-----------|--------|
| 1  | Feature A | True   |
| 2  | Feature B | False  |
| 3  | Feature C | True   |

The output will be

```commandline
Hello World!!!
None
Decorator on method with no return
```