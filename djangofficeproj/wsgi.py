"""
WSGI config for psmprj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from djangoffice.settings import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoffice.settings")

# if settings.STATIC_ENABLE_WSGI_HANDLER:
#     application = StaticFilesHandler(get_wsgi_application())
# else:
#     application = get_wsgi_application()

application = get_wsgi_application()

# Production only, if NGINX not used...
# if not settings.DEBUG and not settings.NGINX_USE:
#     application = WhiteNoise(application, root=settings.STATIC_ROOT)

"""
# to support subdirectory in reverse proxy server; NGINX
#  partial solution: https://stackoverflow.com/questions/47941075/host-django-on-subfolder/47945170#47945170
#  below codes are not necessary, solution is with settings.py and NGINX configuration

settings.py
    MY_PROJECT = env('MY_PROJECT', '')  # example; '/dj'
    if MY_PROJECT:
        USE_X_FORWARDED_HOST = True
        FORCE_SCRIPT_NAME = MY_PROJECT + "/"
        SESSION_COOKIE_PATH = MY_PROJECT + "/"

    LOGIN_URL = "login/"
    LOGIN_REDIRECT_URL = MY_PROJECT + "/"
    LOGOUT_REDIRECT_URL = MY_PROJECT + "/"

NGINX
    location /dj/ {
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header Host $http_host;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_pass http://127.0.0.1:8000/;
    }
"""
# def application(environ, start_response):
#     # http://flask.pocoo.org/snippets/35/
#     script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
#     if script_name:
#         environ['SCRIPT_NAME'] = script_name
#         path_info = environ['PATH_INFO']
#         if path_info.startswith(script_name):
#             environ['PATH_INFO'] = path_info[len(script_name):]

#     scheme = environ.get('HTTP_X_SCHEME', '')
#     if scheme:
#         environ['wsgi.url_scheme'] = scheme

#     return _application(environ, start_response)