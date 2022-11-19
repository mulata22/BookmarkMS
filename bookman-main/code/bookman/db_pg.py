import psycopg2

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host = current_app.config['DB_HOST'],
            database = current_app.config['DATABASE'],
            user = current_app.config['DB_USERNAME'],
            password = current_app.config['DB_PASSWORD'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()

    with db:
        with db.cursor() as cursor:
            with current_app.open_resource('schema-pg.sql') as f:
                cursor.execute(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)