# Uknow Information Collector

  ![logo](https://git.net9.org/blxlrsmb/unknown/raw/master/docs/logo/logo.png)

  Uknow Information Collector is a highly extensible web server which can fetch and process various information feeds, and provide them with RESTful api.

  It's a project for *Software Engineering (2013Fall)* course in Tsinghua University.

  Note that Uknow is far from complete. We only wrote a proof-of-concept working system to present our highly extensible design.
  Any contribution is welcome.


## Features

  + Plugin-based fetcher and filter for fetching, pre-processing, post-processing information.
  + User-specific fetcher and filter.
  + Distributed fetcher worker.

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
