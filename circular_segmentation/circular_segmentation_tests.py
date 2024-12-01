import unittest
from circular_segmentation import app, circular_objects, CircularObject
import json
import os

class CircularSegmentationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_image_no_file(self):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'No file part')

    def test_upload_image_successful(self):
        with open('uploads/test_image.jpg', 'rb') as img:
            response = self.app.post('/upload', data={'file': img})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), 'Image uploaded successfully')

    def test_segment_image_no_file_path(self):
        response = self.app.post('/segment', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'File path not provided')

    def test_segment_image_invalid_file(self):
        response = self.app.post('/segment', json={'file_path': 'invalid_path.jpg'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Invalid image file')

    def test_segment_image_successful(self):
        # Assuming 'test_image.jpg' is already uploaded
        response = self.app.post('/segment', json={'file_path': 'uploads/test_image.jpg'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Segmentation completed')

    def test_get_objects_empty(self):
        response = self.app.get('/objects')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_object_not_found(self):
        response = self.app.get('/object/non_existent_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode(), 'Object not found')

    def test_load_annotations_not_found(self):
        if os.path.exists('uploads/_annotations.coco'):
            os.remove('uploads/_annotations.coco')
        response = self.app.get('/annotations')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode(), 'Annotations file not found')

    def test_load_annotations_successful(self):
        with open('uploads/_annotations.coco', 'w') as file:
            json.dump({'annotations': []}, file)
        response = self.app.get('/annotations')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

if __name__ == '__main__':
    unittest.main()