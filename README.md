# Udia Server

![UDIA](logo.png)

**Universal Dream | Infinite Awareness**

* The public facing API can be found at [https://udia-server.herokuapp.com](https://udia-server.herokuapp.com)

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/).

```sh
$ pipenv install
$ pipenv shell

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ git remote rm heroku
$ heroku git:remote -a udia-server
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## License

Udia Software Incorporated (UDIA)

Copyright (c) 2016-2017 Udia Software Incorporated. All Rights Reserved.

Common Public Attribution License Version 1.0 (CPAL-1.0)

Full license text can be found at [LICENSE](LICENSE)
