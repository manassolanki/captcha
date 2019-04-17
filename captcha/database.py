import click

from flask import current_app, g
from flask.cli import with_appcontext

from pymongo import MongoClient


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        client = MongoClient(current_app.config['DATABASE'])
        g.db = client.captche_app_database

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def add_index():
    # add the mongodb index on email id
    get_db().users.createIndex({"email": 1}, {"unique": True})


@click.command('add-db-index')
@with_appcontext
def add_db_index():
    """Clear existing data and create new tables."""
    add_index()
    click.echo('Added the database index on email.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    # app.teardown_appcontext(close_db)
    app.cli.add_command(add_db_index)
