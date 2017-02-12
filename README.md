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

## Setup SQL Database
In order to start this app you will need to configure the following environment variables with the appropriate values:

`DATABASE_URI` (Database endpoint for SQLAlchemy)

This app has been tested with Sqlite and Postgres. Postgres was setup using a docker container running locally. Use the following to configure your backend:

``export DATABASE_URI=sqlite:///`pwd`/test.db``

`export DATABASE_URI=postgres://postgres@localhost:5432`

You will also need to perform db migrations and stuff (setup db and tables):

```
make init
make migrate
```

## Start the App
To start the app you'll first want to install it as a package (along with its dependencies): `make install`

Then just run it: `make run`

Of course, if you're just running it in dev mode you can just run `make debug`
