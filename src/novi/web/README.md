# Installation and Usage

Follow the installation and configuration instructions outlined in the [README](../core/README.md) under core, to setup
the database connection and create the tables.
Once your database is configured and seeded, launch the flask app using the following command

## Usage

```commandline
flask --app novi.web run
```

The web application will serve features at the following endpoints:

- [POST] http://127.0.0.1:5000/flags
- [POST] http://127.0.0.1:5000/flags/<flag_name>

By default the flags are evaluated and require the context json to be passed in the POST request body.
To turn off evaluation and return the default status instead, use the query parameter `evaluate=true`
or `evaluate=false`
