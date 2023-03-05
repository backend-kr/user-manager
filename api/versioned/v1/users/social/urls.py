import os
from django.urls import re_path, include

folder = os.path.dirname(os.path.realpath(__file__))
urlpatterns = []

for path, dirs, files, in os.walk(folder):
    depth = path[len(folder) + len(os.path.sep):].count(os.path.sep)

    if path != folder and 'urls.py' in files:
        version, api_name = path.split(os.path.sep)[-2:]

        _include = 'api.versioned.v1.users.social.{}.urls'.format(api_name)

        urlpatterns.append(re_path(r'^' + api_name + '/', include(_include)))
