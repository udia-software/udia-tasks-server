# Udia Server (Tasks)

![UDIA](logo.png)

**Universal Dream | Infinite Awareness**

* The public facing API can be found at [https://udia-tasks-server.herokuapp.com](https://udia-tasks-server.herokuapp.com)

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org), [Heroku Toolbelt](https://toolbelt.heroku.com/), and access to a running PostgreSQL instance (like [Postgres.app](http://postgresapp.com/)).

If using Postgres.app as the DB, no configuration of the `DATABASE_URL` is needed.

```sh
$ pipenv install
$ pipenv shell

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploy to Heroku

1. Ensure Heroku is added as one of your Git remotes
```bash
$ git remote -v
heroku	https://git.heroku.com/udia-tasks-server.git (fetch)
heroku	https://git.heroku.com/udia-tasks-server.git (push)
...
# otherwise set the remote
$ heroku git:remote -a udia-tasks-server
set git remote heroku to https://git.heroku.com/udia-tasks-server.git
$ git remote add heroku https://git.heroku.com/udia-tasks-server.git
```

2. Push your changes to heroku with `git push heroku master`
3. Migrations will automatically be applied upon successful release.

## Environment Variables

The environment variables are set when the application is first loaded. **Set these values on your production server accordingly.**

| Environment Variable  | Default Value      | Description                         |
| --------------------- |:------------------:| -----------------------------------:|
| `DJANGO_ENVIRONMENT`  | `DEV`              | May be one of `DEV`, `TEST`, `PROD` |
| `ALLOWED_HOST`        | `localhost:5000`   | Value of API (server) host url      |
| `CORS_DOMAIN`         | `localhost:3000`   | Value of Client url                 |
| `SECRET_KEY`          | `<hash>`           | Django Secret Key                   |
| `DATABASE_URL`        | `postgres://<foo>` | DB URL                              |
| `EMAIL_HOST`          | `smtp.mailgun.org` | Host for sending email              |
| `EMAIL_PORT`          | `2525`             | Port for sending email              |
| `EMAIL_HOST_USER`     | `<user>`           | Sending Email username              |
| `EMAIL_HOST_PASSWORD` | `<pass>`           | Sending Email password              |
| `HTTP_PROTOCOL`       | `http://`          | May be `http://` or `https://`      |
| `HTTP_PROTOCOL`       | `http://`          | May be `http://` or `https://`      |
| `FROM_EMAIL`          | `noreply@udia.ca`  | Set to be the server's email        |
| `ENABLE_PROD_DEBUG`   | ` `                | Enable Debug in Production if value |

## Email Gotchas

In Django Admin, set the value for `SITE_ID=1` in the Sites to be:

* `DOMAIN_NAME=localhost:3000` and `DISPLAY_NAME=UDIA` for dev
* `DOMAIN_NAME=udia.ca` and `DISPLAY_NAME=UDIA` for prod

## Deploying to Heroku

```sh
$ git remote rm heroku
$ heroku git:remote -a udia-tasks-server
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## License

Udia Software Incorporated (UDIA)

Copyright (c) 2016-2017 Udia Software Incorporated. All Rights Reserved.

Common Public Attribution License Version 1.0 (CPAL-1.0)

Full license text can be found at [LICENSE](LICENSE)
