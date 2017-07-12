# flask-tutorial
Instructional Flask Setup

I created this project because it was time that I finally did.

This project demonstrates the following:
- Organization of modules
- OAuth with Github
- Logging
- Database stuff (verifying best practices)
- Running app as a module
- [TODO - testing]

## Setup OAuth
In order to start this app you will need to configure the following environment variables with the appropriate values:

`GITHUB_CLIENT` (Github Client ID)

`GITHUB_SECRET` (Github Secret Key)

If you just want to run this app without OAuth stuff then just set them to dummy values.

make sure to also `export FLASK_APP=tutorial/__init__.py` so that the flask cli can find where all your stuff is

## Setup SQL Database
This app works only with Postgres. Postgres was setup using a docker container running locally (`docker run -p 5432:5432 -it -d postgres
`). The following is the overridable default database address:

`export DATABASE_URI=postgres://postgres@localhost:5432`

You will also need to perform db migrations and stuff (setup db and tables):

`flask db uprade`

If you update the ORM models make sure to `flask db migrate` to let alembic upgrade the migration files before you apply the database migrations using `flask db upgrade`


## Start the App
To start the app you'll first want to install it as a package (along with its dependencies): `make install`

Then just run it: `flask run`

Of course, if you're just running it in dev mode you can just run `make debug`
