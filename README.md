# To Eat List API 🦑🥒🥢

This project is the backend for a `To Eat List` application. `To Eat List` allows managing your home food stock. Please note, this is a pet project, and due to the limited time and resources, it does not always follow best practices.

## Setup

Setup and serve
```BASH
pipenv install
```
Run server
```BASH
pipenv run flask run
```

## Setup environment
There is a [.env.sample](./.env.sample) file with the environment variables that can be defined.

### Setup CORS
The [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) config uses the `ALLOWED_ORIGINS` env variable to set allowed origins

### Setup test db
Use the `TEST_DATABASE_URL` env variable to link test db when running in `test` env

## Test
Run tests using
```BASH
pipenv run pytest  
```

## Setup DB
Create DB 
```BASH
pipenv run flask db_create
```

Seeding some data
```BASH
pipenv run flask db_seed  
```

Drop DB
```BASH
pipenv run flask db_drop  
```

## Deployment
### Deploy to Heroku
The API is deployed to Heroku  
Before you can deploy to heroku add the following files: 
- [Procfile](./Procfile)
- [runtime.txt](./runtime.txt)

Then:
```BASH
heroku login    
```
if you haven't yet
```BASH
 heroku create <app_name>
```
or 
```BASH
 heroku git:remote -a <existing_app>
```
finally
```BASH
git push heroku master
```

### Setup Postgres DB on Heroku
Although this would not be ideal for a scalable service, but for now we can setup a DB manually,when you run:
```BASH
heroku addons:add heroku-postgresql:hobby-dev
```
Heroku automatically defines the `DATABASE_URL` env varible for the new postgres db.
We needed to install the following packages in our project:
`marshmallow-sqlalchemy = "*"`
`psycopg2-binary`

After `git push heroku master`, run the create command:
```BASH
heroku run bash
```
cd into the `Lib` folder and run

```BASH
flask db_create
```

If needed, connect to the the `production` db in your terminal by changing the env varible `DATABASE_URL` to this connection URL:

```
heroku pg:credentials:url DATABASE
```
