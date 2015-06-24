#!/usr/bin/env python3

"""Main Dokomo Forms entry point.

Execute this script to start the Tornado server and WSGI container. It will
ensure that the proper tables and extensions exist in the specified schema
of the PostgreSQL database.

The application looks for gettext translation files like
locale/{locale}/LC_MESSAGES/dokomoforms.mo
"""
import os.path
import textwrap
import sys
import logging

from sqlalchemy import DDL

from sqlalchemy.orm import sessionmaker

from tornado.web import url
import tornado.httpserver
import tornado.web

from dokomoforms.options import options

if __name__ == '__main__':
    from dokomoforms.options import parse_options
    # Necessary to load the schema properly. Feels like a hack...
    parse_options()

import dokomoforms.handlers as handlers
from dokomoforms.models import create_engine, Base
from dokomoforms.models.survey import _set_tzinfos

_pwd = os.path.dirname(__file__)
bold = '\033[1m'
green = '\033[92m'


def modify_text(text: str, modifier: str) -> str:
    """Modify text for printing to the command line.

    :param text: the string to modify
    :param modifier: the escape sequence that marks the modifier
    :return: the modified string
    """
    return modifier + text + '\033[0m'


def get_cookie_secret() -> bytes:
    """Return the secret from the cookie_secret file.

    The cookie secret is in the file <project_directory>/cookie_secret. If
    the file doesn't exist, the script will exit with code 1 and tell the
    user how to generate it.

    :return: the cookie secret as bytes
    """
    try:
        with open(os.path.join(_pwd, 'cookie_secret'), 'rb') as cookie_file:
            cookie_secret = cookie_file.read()
        return cookie_secret
    except IOError:
        print(textwrap.fill(
            '{error} no secret key found for creating secure user session'
            ' cookies. Create it by running the following command:'.format(
                error=modify_text('Error:', bold)
            )
        ))
        print('head -c 24 /dev/urandom > cookie_secret')
        sys.exit(1)


def ensure_that_user_wants_to_drop_schema():
    """Check that user asked to drop the schema intentionally.

    Interrogates the user to make sure that the schema specified by
    options.schema should be dropped. If the user decides against it,
    exits the application.
    """
    answer = input(textwrap.fill(
        'Do you really want to drop the schema {schema}? Doing so will {erase}'
        ' all the data {permanently} y/n (default n)'.format(
            schema=options.schema,
            erase=modify_text('ERASE', bold),
            permanently=modify_text('PERMANENTLY!!!', bold),
        )
    ) + ' ')
    if answer.lower().startswith('y'):
        schema_check = input('Enter the exact name of the schema to drop: ')
        if schema_check == options.schema:
            return
        else:
            print('"{}" does not match the schema "{}"'.format(
                schema_check, options.schema
            ))
    print('Not dropping the schema. Exiting...')
    sys.exit()


class Application(tornado.web.Application):

    """The tornado.web.Application for Dokomo Forms."""

    def __init__(self):
        """Set up the application with handlers and a db connection.

        Defines the URLs (with associated handlers) and settings for the
        application, drops the database schema (if the user selected that
        option), then prepares the database and creates a session.

        """
        urls = [
            # Administrative
            url(r'/', handlers.Index, name='index'),
            url(r'/user/login/?', handlers.Login, name='login'),
            url(r'/user/logout/?', handlers.Logout, name='logout'),
        ]
        settings = {
            'template_path': os.path.join(_pwd, 'dokomoforms/templates'),
            'static_path': os.path.join(_pwd, 'dokomoforms/static'),
            'default_handler_class': handlers.NotFound,
            'xsrf_cookies': True,
            'cookie_secret': get_cookie_secret(),
            'login_url': '/',
            'debug': options.debug,
        }
        super().__init__(urls, **settings)
        self.engine = create_engine()
        if options.kill:
            logging.info('Dropping schema {}.'.format(options.schema))
            self.engine.execute(
                DDL('DROP SCHEMA IF EXISTS {} CASCADE'.format(options.schema))
            )
        Base.metadata.create_all(self.engine)
        _set_tzinfos()
        self.session = sessionmaker(bind=self.engine, autocommit=True)()


def main():
    """Start the Tornado web server."""
    if options.kill:
        ensure_that_user_wants_to_drop_schema()
    http_server = tornado.httpserver.HTTPServer(Application())
    tornado.locale.load_gettext_translations(
        os.path.join(_pwd, 'locale'), 'dokomoforms'
    )
    logging.info(
        '{dokomo}{starting}'.format(
            dokomo=modify_text(
                'Dokomo Forms for {}: '.format(options.organization), bold
            ),
            starting=modify_text(
                'starting server on port {}'.format(options.port), green
            ),
        )
    )
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
