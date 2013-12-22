# Uknow Information Collector

  ![logo](https://git.net9.org/blxlrsmb/unknown/raw/master/docs/logo/logo.png)

  Uknow Information Collector is a web server that can fetch Information and provide it with RESTful api.

  It's a project for Software Engineering course, and is currently deployed at [https://uknow.net9.org]()

## Dependency

  + Python2 with virtualenv
  + Redis server
  + MongoDB

## Installation

Make sure you have python2 and virtualenv in ``PATH``, then run the following command:

	cd manage
	./quickinstall

*Notice* If you are using Mac, you may need to install libevent with your package manager.
And if you are using macports, run following command instead:

	cd manage
	CFLAGS="-I /opt/local/include -L /opt/local/lib" ./quickinstall

## Run
To start the api-website:

	. ./manage/setenv.sh
	api-website

Or:

	cd api-website
	./standalone_server.py

To start the frontend-website:

	. ./manage/setenv.sh
	frontend-website

Or:

	./frontend-website/start_frontend.sh

To start the fetcher server:

	. ./manage/setenv.sh
	./fetcher/celery_worker.sh
	fetcher-server

Or:

	cd fetcher
	./celery_worker.sh
	./general_fetcher_server.py


## Configuration
See ``manage/config.py``
