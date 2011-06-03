#!/usr/bin/env python

# FIXME: Save password/email and use pexpect or similar to prevent typing it
#        more than once


import os


PROJECT_DIR = "/Users/durden/Dropbox/code/web/frameworks/app_engine/streamquality"
DATA_DIR = "%s/sample_data" % (PROJECT_DIR)

APP_NAME = "streamquality"
URL = "http://localhost:8084/remote_api"
CONFIG_FILE = "%s/bulkloader.yaml" % (PROJECT_DIR)

SOURCES = ['Vote', 'SQUser', 'Tweet']


def main():
    """Main"""

    for src in SOURCES:
        filename = "%s/%s.csv" % (DATA_DIR, src.lower())
        ret = os.system("appcfg.py upload_data --application=%s --url=%s --filename=%s  --config_file=%s --kind=%s" % (APP_NAME, URL, filename, CONFIG_FILE, src))
        if ret != 0:
            print "Error importing %s from %s" % (src, filename)


if __name__ == "__main__":
    main()
