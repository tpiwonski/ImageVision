from flask import Blueprint, current_app, flash, request
from flask.views import MethodView

from imagevision.services.image import create_image_service

api = Blueprint('api', __name__)


class ImageResource(MethodView):

    def delete(self, image_id):
        image_service = create_image_service(current_app)
        image_service.delete_image(image_id)
        flash("Image deleted")
        return ''


class ImageAnnotationsResource(MethodView):

    def put(self, image_id):
        image_service = create_image_service(current_app)
        image_service.annotate_image(image_id)
        flash("Image annotated")
        return ''


api.add_url_rule('/image/<image_id>', view_func=ImageResource.as_view('image'), methods=['DELETE'])
api.add_url_rule('/image/<image_id>/annotations', view_func=ImageAnnotationsResource.as_view('image_annotations'))


def setup_api(app):
    app.register_blueprint(api, url_prefix='/api')
