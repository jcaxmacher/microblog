import datetime
import markdown
from peewee import (
    MySQLDatabase, Model, IntegerField, CharField,
    TextField, DateTimeField, AutoField, ForeignKeyField
)
from playhouse import db_url

import click
from flask.cli import with_appcontext
import boto3


ssm = boto3.client('ssm')
response = ssm.get_parameter(Name='/example-a/prod/mysqldb')
params = db_url.parse(response['Parameter']['Value'])
database = MySQLDatabase(**params)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    password = CharField()


class Post(BaseModel):
    id = AutoField()
    author = ForeignKeyField(User, backref='posts')
    created = DateTimeField(default=datetime.datetime.now)
    title = CharField()
    body = TextField()

    def html_body(self):
        return markdown.markdown(self.body)


def init_db():
    with database:
        database.create_tables([User, Post])


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    @app.before_request
    def before_request():
        database.connect()

    @app.after_request
    def after_request(response):
        database.close()
        return response
    app.cli.add_command(init_db_command)