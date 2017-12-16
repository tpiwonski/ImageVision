from flask import Flask, g

from imagevision.repositories.database import setup_database, ImageRepository
from imagevision.controllers.ui import setup_ui
from imagevision.controllers.ajax import setup_ajax

from imagevision.injector import container, Scope
from imagevision.repositories.storage import ImageStorage
from imagevision.services.image import ImageService
from imagevision.services.vision import VisionService


def create_application(config=None):
    """
    Create the application.

    :param config: a configuration object to update
    :return: the application
    """
    app = Flask(__name__)
    app.config.from_json('config.json')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    if config:
        app.config.from_mapping(config)
    
    app.secret_key = 'loremipsum'

    app.before_request(set_scope)
    app.teardown_request(dispose_scope)
    container.set_scope_provider(get_scope)

    container.add_singleton_instance(Flask, app)

    container.add_scoped_class(ImageRepository, ImageRepository)
    container.add_scoped_class(ImageStorage, ImageStorage)
    container.add_scoped_class(ImageService, ImageService)
    container.add_scoped_class(VisionService, VisionService)

    setup_database(app)
    setup_ui(app)
    setup_ajax(app)

    return app


def set_scope():
    g.injector_scope = Scope()


def get_scope():
    return g.injector_scope


def dispose_scope(error):
    delattr(g, 'injector_scope')
