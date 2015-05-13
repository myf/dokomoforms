"""Useful reusable functions for handlers, plus the BaseHandler."""

import tornado.web
from tornado.escape import to_unicode


class BaseHandler(tornado.web.RequestHandler):
    @property
    def session(self):
        return self.application.session

    def prepare(self):
        self.xsrf_token

    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(404)

    def get_current_user(self):
        user = self.get_secure_cookie('user')
        if user:
            return to_unicode(user)
        return None
