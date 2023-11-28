# Installation and Usage

Follow the installation and configuration instructions outlined in the [README](../core/README.md) under core, to setup
the database connection and create the tables.
Once your database is configured and seeded, launch the flask app using the following command

## Usage

```commandline
flask --app okapi.web run
```

The web application will serve features at the following endpoints:

http://127.0.0.1:5000/flags

http://127.0.0.1:5000/flags/<flag_name>