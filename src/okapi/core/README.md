# Installation and Usage

## Installation

```pip install okapi```

## Usage

There are a few ways to check the status of a flag and turn on/of features.

### Using DbClient

DbClient retrieves feature flags from a database. okapi uses sqlalchemy to query from a variety of databases.

#### Configuration

Before you query a database, you need to tell okapi how to connect to your database. This is done in okapi.ini.
An example file is below:

```toml
[database]
url = sqlite:///features.sqlite
echo = False
createTables=True
```

- **url:** is the connection url to your database.
  In the above example, we connect to a sqlite database called _features.sqlite_ in the current folder. If the database
  does not exist, it will be created
- **echo:** Tells the app to log or not log sql statements that are executed
- **createTables:** True means tables will be created if they do not exist in the database

The following 3 tables will be created **flags**, **activations** and **flags_activations**

```sql
CREATE TABLE flags (
	id INTEGER NOT NULL, 
	name VARCHAR(30) NOT NULL, 
	status BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)

CREATE TABLE activations (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	class_name VARCHAR NOT NULL, 
	config VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)

CREATE TABLE flags_activations (
	flag_id INTEGER, 
	activation_id INTEGER, 
	FOREIGN KEY(flag_id) REFERENCES flag (id), 
	FOREIGN KEY(activation_id) REFERENCES activation (id)
)
```

Once the tables are created and seeded with your feature flag data. You can either use the decorator or the is_enabled
method to check the status of a feature flag using it's name. The example python file demonstrates both ways

```python
from okapi.client.dbclient import DbClient


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

okapi can also retrieve feature flags from an API endpoint. For instructions on how to setup an API server to serve
feature flags, see the [README](../web/README.md) under web.

#### Configuration

Using a remote client, requires okapi to know the url of the remote client, this is specified in okapi.ini,
as illustrated in the example below

```toml
[remote]
url = http://127.0.0.1:5000/flags
```

Usage is similar to DbClient, instead of DbClient, you would use RemoteClient from the same package.

```python
from okapi.client.remoteclient import RemoteClient

...
```