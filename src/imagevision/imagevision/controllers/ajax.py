from flask import Blueprint, flash
from flask.views import MethodView

from imagevision.injector import inject
from imagevision.services.image import ImageService

ajax = Blueprint('ajax', __name__)


class Image(MethodView):
    methods = ['DELETE']

    @inject(image_service=ImageService)
    def __init__(self, image_service):
        self.image_service = image_service

    def delete(self, image_id):
        self.image_service.delete_image(image_id)
        flash("Image deleted")
        return ''


ajax.add_url_rule('/image/<image_id>', view_func=Image.as_view('image'))


def setup_ajax(app):
    app.register_blueprint(ajax, url_prefix='/ajax')
