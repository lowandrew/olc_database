My Awesome Project
==================

A web interface for OLC's sequence database.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Testing!
^^^^^^^^^^^^^

To run the tests for the data_wrapper app::

 $ docker-compose -f local.yml run --rm django python manage.py test data_wrapper



Deployment
----------

The following details how to deploy this application. You'll need docker and docker-compose!

Local deployment::

 $ docker-compose -f local.yml build
 $ docker-compose -f local.yml up

You should also make and run migrations::

 $ docker-compose -f local.yml run --rm django python manage.py makemigrations
 $ docker-compose -f local.yml run --rm django python manage.py migrate


With that done, just head to 0.0.0.0:8000 in your browser, and you should be good to go.
