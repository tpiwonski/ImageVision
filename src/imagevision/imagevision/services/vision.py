from google.cloud.vision import ImageAnnotatorClient
from google.cloud.vision import types


class VisionService(object):

    def __init__(self):
        self.vision_client = ImageAnnotatorClient()
        self.response_formatter = ResponseFormatter()

    def annotate_image(self, image_file):
        content = image_file.read()
        request = {
            'image': types.Image(content=content)
        }
        response = self.vision_client.annotate_image(request)
        result = self.response_formatter.format_response(response)
        return result


class ResponseFormatter(object):

    def format_annotation(self, annotation):
        a = {}
        for field, value in annotation.ListFields():
            if isinstance(value, (str, int, float)):
                a[field.name] = value
            else:
                if hasattr(value, 'ListFields'):
                    a[field.name] = self.format_annotation(value)
                else:
                    a[field.name] = self.format_annotations(value)

        return a

    def format_annotations(self, annotations):
        a = []
        for annotation in annotations:
            a.append(self.format_annotation(annotation))

        return a

    def format_response(self, response):
        result = {
            'label_annotations': self.format_annotations(response.label_annotations),
            'safe_search_annotation': self.format_annotation(response.safe_search_annotation),
            'web_detection': self.format_annotation(response.web_detection),
            'crop_hints_annotation': self.format_annotation(response.crop_hints_annotation),
            'face_annotations': self.format_annotations(response.face_annotations),
            'full_text_annotation': self.format_annotation(response.full_text_annotation),
            'image_properties_annotation': self.format_annotation(response.image_properties_annotation),
            'landmark_annotations': self.format_annotations(response.landmark_annotations),
            'logo_annotations': self.format_annotations(response.logo_annotations),
            'text_annotations': self.format_annotations(response.text_annotations)
        }
        return result
