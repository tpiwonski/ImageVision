from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_file
from flask.views import MethodView

from imagevision.services.image import create_image_service

ui = Blueprint('ui', __name__)


class Home(MethodView):
    methods = ['GET']

    def get(self):
        image_service = create_image_service(current_app)
        images = image_service.get_images(0, 10)
        return render_template('ui/home.html', images=images)


class ImageUpload(MethodView):
    methods = ['GET', 'POST']

    def get(self):
        return render_template('ui/upload.html')

    def post(self):
        if 'file' not in request.files:
            flash('No file')
            return redirect(url_for('ui.image_upload'))

        image_file = request.files['file']

        if not image_file.filename:
            flash('No file')
            return redirect(url_for('ui.image_upload'))

        image_service = create_image_service(current_app)
        image_id = image_service.create_image(image_file, image_file.filename, image_file.mimetype)

        flash("Image uploaded")

        return redirect(url_for('ui.image_preview', image_id=image_id))


class Image(MethodView):
    methods = ['GET']

    def get(self, image_id):
        image_service = create_image_service(current_app)
        image = image_service.get_image(image_id)
        if image is None:
            raise Exception('Image not found')

        return send_file(image['image_file_path'], mimetype=image['image_mime_type'],
                         as_attachment=True, attachment_filename=image['image_file_name'])


class ImagePreview(MethodView):
    methods = ['GET']

    def get(self, image_id):
        image_service = create_image_service(current_app)
        image = image_service.get_image(image_id)
        if image is None:
            raise Exception('Image not found')

        return render_template('ui/preview.html', image=image)


ui.add_url_rule('/', view_func=Home.as_view('home'))
ui.add_url_rule('/image', view_func=ImageUpload.as_view('image_upload'))
ui.add_url_rule('/image/<image_id>', view_func=Image.as_view('image'))
ui.add_url_rule('/image/<image_id>/preview', view_func=ImagePreview.as_view('image_preview'))


def error_handler(error):
    current_app.logger.error(error)
    return render_template('ui/error.html', error=error)


def setup_ui(app):
    ui.register_error_handler(Exception, error_handler)
    app.register_blueprint(ui)
