from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_file

from imagevision.services.image import create_image_service

ui = Blueprint('ui', __name__)


def home():
    image_service = create_image_service(current_app)
    images = image_service.get_images(0, 10)
    return render_template('ui/home.html', images=images)


def upload_image():
    if request.method == 'GET':
        return render_template('ui/upload.html')

    elif request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return redirect(url_for('ui.upload_image'))

        image_file = request.files['file']

        if not image_file.filename:
            flash('No file')
            return redirect(url_for('ui.upload_image'))

        image_service = create_image_service(current_app)
        image_id = image_service.create_image(image_file, image_file.filename, image_file.mimetype)

        flash("Image uploaded")

        return redirect(url_for('ui.preview_image', image_id=image_id))


def get_image(image_id):
    image_service = create_image_service(current_app)
    image = image_service.get_image(image_id)
    return send_file(image['image_file_path'], mimetype=image['image_mime_type'],
                     as_attachment=True, attachment_filename=image['image_file_name'])


def preview_image(image_id):
    image_service = create_image_service(current_app)
    image = image_service.get_image(image_id)
    return render_template('ui/preview.html', image=image)


ui.add_url_rule('/', 'home', home)
ui.add_url_rule('/image', 'upload_image', upload_image, methods=['GET', 'POST'])
ui.add_url_rule('/image/<image_id>', 'get_image', get_image)
ui.add_url_rule('/image/<image_id>/preview', 'preview_image', preview_image)


def setup_ui(app):
    app.register_blueprint(ui)
