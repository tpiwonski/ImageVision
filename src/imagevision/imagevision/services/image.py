from imagevision.repositories.database import ImageRepository
from imagevision.repositories.storage import ImageStorage
from imagevision.services.vision import VisionService


class ImageService(object):

    def __init__(self, repository, storage, vision):
        self.repository = repository
        self.storage = storage
        self.vision = vision

    def create_image(self, image_file, file_name, mime_type):
        image_id = self.repository.create_image(file_name, mime_type)
        self.storage.save_image(image_id, image_file)
        self.annotate_image(image_id)
        return image_id

    def get_image(self, image_id):
        image = self.repository.get_image(image_id)
        if image is None:
            return None

        image['image_file_path'] = self.storage.get_image_path(image_id)
        return image

    def get_images(self, offset, limit):
        images = self.repository.get_images(offset, limit)
        for image in images:
            image['image_file_path'] = self.storage.get_image_path(image['image_id'])

        return images

    def annotate_image(self, image_id):
        image_file = self.storage.load_image(image_id)
        with image_file as f:
            annotations = self.vision.annotate_image(f)

        self.repository.annotate_image(image_id, annotations)

    def delete_image(self, image_id):
        self.repository.delete_image(image_id)
        self.storage.delete_image(image_id)


def create_image_service(app):
    repository = ImageRepository(app.config['DATABASE_URI'])
    storage = ImageStorage(app.config['STORAGE_PATH'])
    vision = VisionService()
    service = ImageService(repository, storage, vision)
    return service
