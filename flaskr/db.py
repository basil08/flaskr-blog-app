import sqlite3

import click
from flask.cli import with_appcontext
from flask import g
from flask import current_app


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # opens a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        # This throws sqlite3.Warning: cannot execute more than one statement
        # db.execute(f.read().decode('utf8'))
        stmts = f.read().decode('utf8').split('\n')
        for stmt in stmts:
            db.execute(stmt)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear existing data and create new tables """
    init_db()
    click.echo('Intialized the database')

def init_app(app):
    # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

