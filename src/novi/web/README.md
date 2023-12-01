# Installation and Usage

Follow the installation and configuration instructions outlined in the [README](../../../README.md), to setup
the database connection. 
To create and seed the database tables use the following command. (sample_data.sql can be any sql script)
```commandline
flask --app "novi.web:create_app(script='sample_data.sql')" run
```
If you have already created the tables and have data then you can run the flask app simply as
```commandline
flask --app novi.web run
```
If you used the [sample_data.sql](../../../sample_data.sql) to seed your tables you can issue the follow requests to 
## Evaluate All flags
```commandline
curl --location '127.0.0.1:5000/evaluatedFlags' \
--header 'Content-Type: application/json' \
--data '{
            "currentDateTime": "11/26/2023 12:00 AM",
            "seed": 90,
            "variant": "A"
}'
```

## Evaluate the Date Activated Feature
```commandline
curl --location '127.0.0.1:5000/evaluatedFlags/Date Activated Feature' \
--header 'Content-Type: application/json' \
--data '{
            "currentDateTime": "11/27/2023 12:00 AM"
}'
```
## All Flags - No Evaluation
```commandline
curl --location '127.0.0.1:5000/flags' \
--data ''
```