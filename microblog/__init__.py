import os
import base64

from flask import Flask
import boto3


APP_NAME = os.environ['APP_NAME']
ENV_NAME = os.environ['ENV_NAME']

ssm = boto3.client('ssm')
response = ssm.get_parameter(Name=f'/{APP_NAME}/{ENV_NAME}/secret-key')
secret_key = base64.b64decode(response['Parameter']['Value'])


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secret_key
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app