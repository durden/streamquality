#!/usr/bin/python

"""
Simple shell implementation to interact with App Engine API.
Taken from: http://code.google.com/intl/en/appengine/articles/remote_api.html
"""

import code
import getpass
import sys

install_dir = "/Applications/GoogleAppEngineLauncher.app/Contents/" + \
              "Resources/GoogleAppEngine-default.bundle/Contents/" + \
              "Resources/google_appengine"
sys.path.append(install_dir)
sys.path.append(install_dir + "/lib/yaml/lib")
sys.path.append(install_dir + "/lib/fancy_urllib/")

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import db


def auth_func():
    return raw_input('Username:'), getpass.getpass('Password:')

if len(sys.argv) < 2:
    print "Usage: %s app_id [host]" % (sys.argv[0],)

app_id = sys.argv[1]

if len(sys.argv) > 2:
    host = sys.argv[2]
else:
    host = '%s.appspot.com' % app_id

remote_api_stub.ConfigureRemoteDatastore(app_id, '/remote_api', auth_func,
                                         host)

code.interact('App Engine interactive console for %s' % (app_id,), None,
                                                        locals())
