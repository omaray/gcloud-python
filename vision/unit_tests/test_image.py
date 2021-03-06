# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import unittest

from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode

IMAGE_SOURCE = 'gs://some/image.jpg'
IMAGE_CONTENT = _to_bytes('/9j/4QNURXhpZgAASUkq')
B64_IMAGE_CONTENT = _bytes_to_unicode(base64.b64encode(IMAGE_CONTENT))
CLIENT_MOCK = {'source': ''}


class TestVisionImage(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.vision.image import Image
        return Image

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_image_source_type_content(self):
        image = self._makeOne(CLIENT_MOCK, content=IMAGE_CONTENT)

        _AS_DICT = {
            'content': B64_IMAGE_CONTENT
        }

        self.assertEqual(B64_IMAGE_CONTENT, image.content)
        self.assertEqual(None, image.source)
        self.assertEqual(_AS_DICT, image.as_dict())

    def test_image_source_type_google_cloud_storage(self):
        image = self._makeOne(CLIENT_MOCK, source_uri=IMAGE_SOURCE)

        _AS_DICT = {
            'source': {
                'gcs_image_uri': IMAGE_SOURCE
            }
        }

        self.assertEqual(IMAGE_SOURCE, image.source)
        self.assertEqual(None, image.content)
        self.assertEqual(_AS_DICT, image.as_dict())

    def test_cannot_set_both_source_and_content(self):
        image = self._makeOne(CLIENT_MOCK, content=IMAGE_CONTENT)

        self.assertEqual(B64_IMAGE_CONTENT, image.content)
        with self.assertRaises(AttributeError):
            image.source = IMAGE_SOURCE

        image = self._makeOne(CLIENT_MOCK, source_uri=IMAGE_SOURCE)
        self.assertEqual(IMAGE_SOURCE, image.source)
        with self.assertRaises(AttributeError):
            image.content = IMAGE_CONTENT
