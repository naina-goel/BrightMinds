import os
import csv
import json
import unittest
from image_resizer_api import app, DATA_FILE

class ImageResizerApiTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Clean up metadata file before each test
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        # Clean up any generated files after each test
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        for file in os.listdir():
            if file.startswith("resized_"):
                os.remove(file)

    def test_resize_image_success(self):
        with open('test_image.jpg', 'rb') as img:
            response = self.app.post('/resize', 
                                     data={'image': img, 'width': 100, 'height': 100, 'depth': '9000.1'})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('file_path', data)
            self.assertTrue(os.path.exists(data['file_path']))

            # Verify metadata is written to CSV
            with open(DATA_FILE, mode='r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]['depth'], '9000.1')
                self.assertEqual(rows[0]['file_path'], data['file_path'])

    def test_resize_image_invalid_dimensions(self):
        with open('test_image.jpg', 'rb') as img:
            response = self.app.post('/resize', 
                                     data={'image': img, 'width': -1, 'height': 100, 'depth': '9000.2'})
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)

    def test_get_image_success(self):
        with open('test_image.jpg', 'rb') as img:
            response = self.app.post('/resize', 
                                     data={'image': img, 'width': 100, 'height': 100, 'depth': '9000.3'})
            data = json.loads(response.data)
            depth = '9000.3'

        response = self.app.get(f'/image/{depth}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/jpeg')

    def test_get_image_not_found(self):
        response = self.app.get('/image/9999.9')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
