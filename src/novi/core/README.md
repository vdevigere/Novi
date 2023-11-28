# Installation and Usage

## Installation

```pip install novi```

## Usage

There are a few ways to check the status of a flag and turn on/of features.

### Using DbClient

DbClient retrieves feature flags from a database. Novi uses sqlalchemy to query from a variety of databases.

#### Configuration

Before you query a database, you need to tell Novi how to connect to your database. This is done in novi.ini.
An example file is [here](../../../novi.ini):
You can either run the DDL SQL from the file [schema.sql](../../../schema.sql) or set createTables=True. 

Once the tables are created and seeded with your feature flag data. You can either use the decorator or the is_enabled
method to check the status of a feature flag using it's name. The example python file demonstrates both ways

```python
from novi.client.dbclient import DbClient


@DbClient.enabled("Feature B")
def hello_decorator_with_return():
    return "Decorator on method with return!!!!"


def hello_world():
    print("Hello World!!!")


@DbClient.enabled("Feature C")
def hello_decorator():
    print("Decorator on method with no return")


if __name__ == '__main__':
    if DbClient.is_enabled("Feature A"):
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

### Using RemoteClient

Novi can also retrieve feature flags from an API endpoint. For instructions on how to setup an API server to serve
feature flags, see the [README](../web/README.md) under web.

#### Configuration

Using a remote client, requires Novi to know the url of the remote client, this is specified in novi.ini,
as illustrated in the example below

```toml
[remote]
url = http://127.0.0.1:5000/flags
```

Usage is similar to DbClient, instead of DbClient, you would use RemoteClient from the same package.

```python
from novi.client.remoteclient import RemoteClient

...
```