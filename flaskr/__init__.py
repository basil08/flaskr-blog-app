from flask import Flask
import os

def create_app(test_config=None):
    """
    application factory

    Any configuration. registration and other setup happens in this function,
    then the application is returned
    """

    # instance_relative_config - configuration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # connect database to application
    from flaskr import db
    db.init_app(app)

    # blueprints
    from flaskr import auth
    app.register_blueprint(auth.bp)

    from flaskr import blog
    app.register_blueprint(blog.bp)
    # app.add_url_rule() associates the endpoint name 'index' with the / url so that url_for('index') or url_for('blog.index') will both work, generating the same / URL either way.
    app.add_url_rule('/', endpoint='index')

    return app


if __name__ == "__main__":
    create_application().run()