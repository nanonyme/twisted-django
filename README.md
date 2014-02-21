Twisted-django
=============
The WSGI wiring inspired by http://blog.vrplumber.com/b/2010/01/24/making-your-twisted-resources/
The point of this library is that it's better to deliver your static resources with Twisted than
with a WSGI middleware

Basically what happens when using this is that Twisted tries to send all your static files if you 
configure STATIC_URL without a scheme. Otherwise this assumes that you're using a CDN or whatnot
anyway and skips statics. They are sent from STATIC_ROOT so collectstatic works as normally.
Actual WSGI containers are in threads in Twisted.web as before. Effectively the difference with
WSGI middleware is that with that setup your WSGI processes or threads get occupied with delivering
the static resources. With this setup all your threads (Twisted.web always uses threads for WSGI)
will be available for the application and statics are delivered in a nonblocking fashion.

Usage
==============
Once having been installed with pip, usage is really simple. Simply add eg

DJANGO_SETTINGS_MODULE=dust.settings twistd -n twisted-django

into your Heroku Procfile. Port can be changed with a parameter -p or --port but the default should be
fine with Heroku. This package relies on DJANGO_SETTINGS_MODULE being set in the environment. Feel free
not to be limited in setting prefixed in the command but it works there too.