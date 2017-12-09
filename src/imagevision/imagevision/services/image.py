
class ImageService(object):

    def __init__(self, repository, storage, vision):
        self.repository = repository
        self.storage = storage
        self.vision = vision

    def create_image(self, image_file, file_name, mime_type):
        image_id = self.repository.create_image(file_name, mime_type)
        self.storage.save_image(image_id, image_file)
        return image_id

    def get_image(self, image_id):
        image = self.repository.get_image(image_id)
        image_file = self.storage.load_image(image_id)
        image['image_file'] = image_file
        return image

    def get_images(self, offset, limit):
        images = self.repository.get_images(offset, limit)
        # for image in images:
        #     image['image_file'] = image_file
        return images

    def annotate_image(self, image_id):
        image = self.get_image(image_id)
        with image['image_file'] as f:
            annotations = self.vision.annotate_image(f)

        self.repository.annotate_image(image_id, annotations)
