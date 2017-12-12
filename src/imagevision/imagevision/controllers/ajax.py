from flask import Blueprint, current_app, flash
from flask.views import MethodView

from imagevision.services.image import create_image_service

ajax = Blueprint('ajax', __name__)


class Image(MethodView):
    methods = ['DELETE']

    def delete(self, image_id):
        image_service = create_image_service(current_app)
        image_service.delete_image(image_id)
        flash("Image deleted")
        return ''


ajax.add_url_rule('/image/<image_id>', view_func=Image.as_view('image'))


def setup_ajax(app):
    app.register_blueprint(ajax, url_prefix='/ajax')
