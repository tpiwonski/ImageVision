from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_file, \
    send_from_directory
from flask.views import View

from imagevision.repositories.database import ImageRepository
from imagevision.repositories.storage import ImageStorage
from imagevision.services.vision import VisionService
from imagevision.services.image import ImageService

ui = Blueprint('ui', __name__)


def create_image_service(app):
    repository = ImageRepository(app.config['DATABASE_URI'])
    storage = ImageStorage(app.config['STORAGE_FOLDER'])
    vision = VisionService()
    service = ImageService(repository, storage, vision)
    return service


def home():
    image_service = create_image_service(current_app)
    images = image_service.get_images(0, 10)
    return render_template('ui/home.html', images=images)


def upload_image():
    if request.method == 'GET':
        return render_template('ui/upload.html')

    elif request.method == 'POST':
        if 'file' not in request.files:
            flash('No file was selected')
            redirect(url_for('ui.upload_image'))

        image_file = request.files['file']

        image_service = create_image_service(current_app)
        image_id = image_service.create_image(image_file, image_file.filename, image_file.mimetype)

        return redirect(url_for('ui.home'))


def get_image(image_id):
    image_service = create_image_service(current_app)
    image = image_service.get_image(image_id)
    return send_file(image['image_file'], mimetype=image['image_mime_type'], attachment_filename=image['image_file_name'])


def preview_image(image_id):
    image_service = create_image_service(current_app)
    image = image_service.get_image(image_id)
    return render_template('ui/preview.html', image=image)


def annotate_image(image_id):
    image_service = create_image_service(current_app)
    image_service.annotate_image(image_id)

    return redirect(url_for('ui.preview_image', image_id=image_id))


ui.add_url_rule('/', 'home', home)
ui.add_url_rule('/upload', 'upload_image', upload_image, methods=['GET', 'POST'])
ui.add_url_rule('/image/<image_id>', 'get_image', get_image)
ui.add_url_rule('/annotate/<image_id>', 'annotate_image', annotate_image)
ui.add_url_rule('/preview/<image_id>', 'preview_image', preview_image)


def setup_ui(app):
    app.register_blueprint(ui)
