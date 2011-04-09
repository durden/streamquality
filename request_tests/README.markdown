# Testing
Currently I don't have any formal tests since unit testing on App
[Google AppEngine](http://code.google.com/appengine/) is not straightfoward in
python yet.

However, it looks like Google is trying to
[improve this](http://code.google.com/appengine/docs/python/tools/localunittesting.html) recently.

I hope to add more standard unit tests in the future, but for now request_tests
module is a good substitute to test some of your requests with Google's
urlfetch module, etc.

## Testing setup
The setup is a bit clunky right now.

- Point the request_tests/google symlink to your AppEngine installation.  It
  currently points to the standard location for AppEngine on Mac OSX.
- Create request_tests/private_oauth_creds/tokens.py and add in your secret
  oauth tokens. Example:
        user_secret="notarealtoken"
        user_token="notarealtoken"
- Go into the request_tests directory and run the following:
        import cli
        cli.try_request()
- You can pass the try_request() method a url to hit
