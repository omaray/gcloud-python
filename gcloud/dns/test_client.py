# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.dns.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from gcloud.dns.connection import Connection
        PROJECT = 'PROJECT'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_quotas_defaults(self):
        PROJECT = 'PROJECT'
        PATH = 'projects/%s' % PROJECT
        MANAGED_ZONES = 1234
        RRS_PER_RRSET = 23
        RRSETS_PER_ZONE = 345
        RRSET_ADDITIONS = 456
        RRSET_DELETIONS = 567
        TOTAL_SIZE = 67890
        DATA = {
            'quota': {
                'managedZones': str(MANAGED_ZONES),
                'resourceRecordsPerRrset': str(RRS_PER_RRSET),
                'rrsetsPerManagedZone': str(RRSETS_PER_ZONE),
                'rrsetAdditionsPerChange': str(RRSET_ADDITIONS),
                'rrsetDeletionsPerChange': str(RRSET_DELETIONS),
                'totalRrdataSizePerChange': str(TOTAL_SIZE),
            }
        }
        CONVERTED = dict([(key, int(value))
                          for key, value in DATA['quota'].items()])
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        quotas = client.quotas()

        self.assertEqual(quotas, CONVERTED)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response