import os


class ImageStorage(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.mkdir(self.storage_path)

    def save_image(self, image_id, image_file):
        image_path = self.get_image_path(image_id)
        with open(image_path, 'wb') as f:
            f.write(image_file.read())

    def load_image(self, image_id):
        image_path = self.get_image_path(image_id)
        return open(image_path, 'rb')

    def delete_image(self, image_id):
        image_path = self.get_image_path(image_id)
        os.remove(image_path)

    def get_image_path(self, image_id):
        return os.path.join(self.storage_path, str(image_id))
