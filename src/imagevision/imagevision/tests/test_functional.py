import json
import os
import shutil

from unittest import TestCase
from unittest.mock import patch

from imagevision import create_application
from imagevision.repositories.database import create_database, ImageRepository
from imagevision.services.image import create_image_service
from imagevision.services.vision import VisionService


class FunctionalTestCase(TestCase):

    DATABASE_PATH = "database.sqlite"

    config = {
        'DATABASE_URI': "sqlite:///{0}".format(DATABASE_PATH),
        'STORAGE_PATH': 'storage'
    }

    def setUp(self):
        if os.path.exists(self.config['STORAGE_PATH']):
            shutil.rmtree(self.config['STORAGE_PATH'], ignore_errors=True)

        with open('annotations.json', 'rt') as f:
            self.test_annotations_response = json.loads(f.read())

        create_database(self.config['DATABASE_URI'])
        self.app = create_application(self.config).test_client()

    def tearDown(self):
        if os.path.exists(self.config['STORAGE_PATH']):
            shutil.rmtree(self.config['STORAGE_PATH'], ignore_errors=True)

        if os.path.exists(self.DATABASE_PATH):
            os.remove(self.DATABASE_PATH)

    def _create_test_images(self, count):
        with self.app.application.app_context():
            with open('image.jpg', 'rb') as f:
                images = []
                for x in range(0, count):
                    image_service = create_image_service(self.app.application)
                    image_id = image_service.create_image(f, 'test.jpg', 'image/jpeg')
                    images.append(image_id)

        return images

    @patch.object(VisionService, 'annotate_image')
    def test_can_upload_and_annotate_image(self, annotate_image):
        annotate_image.return_value = self.test_annotations_response

        r = self.app.post('/image', data={
            'file': (open('image.jpg', 'rb'), 'test.jpg')
        })

        assert r.status_code == 302
        assert b'/image/1/preview' in r.data

    @patch.object(VisionService, 'annotate_image')
    def test_can_preview_image(self, annotate_image):
        annotate_image.return_value = self.test_annotations_response
        images = self._create_test_images(1)

        r = self.app.get('/image/{0}/preview'.format(images[0]))

        assert b'Image test.jpg analysis results' in r.data
        assert b'social group' in r.data
        assert b'violence : 1' in r.data
        assert b'Harrison Ford' in r.data

    @patch.object(VisionService, 'annotate_image')
    def test_can_view_images_list(self, annotate_image):
        annotate_image.return_value = self.test_annotations_response
        images = self._create_test_images(3)

        r = self.app.get('/')

        for image_id in images:
            assert (b'/image/%d/preview' % image_id) in r.data

    @patch.object(VisionService, 'annotate_image')
    def test_can_delete_image(self, annotate_image):
        annotate_image.return_value = self.test_annotations_response
        images = self._create_test_images(1)

        r = self.app.delete('/ajax/image/{0}'.format(images[0]))

        assert r.status_code == 200

        r = self.app.get('/image/{0}/preview'.format(images[0]))

        assert b'Image not found' in r.data
