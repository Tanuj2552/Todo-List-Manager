import os

from flask import Flask, render_template

def create_app(test_config = None):
    app = Flask("manager")
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'manager.sqlite')
    )

    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import lister
    app.register_blueprint(lister.bp)

    from . import db 
    db.init_app(app) 


    return app