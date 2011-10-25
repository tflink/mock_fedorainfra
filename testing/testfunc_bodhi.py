#
# testfunc_bodhi.py - functional tests for the bodhi portion of boji
#
# Copyright 2011, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author: Tim Flink <tflink@redhat.com>

import pytest
import bunch
import json
import mock_fedorainfra.boji
import tempfile
from mock_fedorainfra import util


class MockBodhi():
    def __init__(self, update):
        self.update = update

    def query(self, package, limit):
        return bunch.Bunch(self.update)

def get_mock_bodhi():
    return MockBodhi(util.make_default_update())

@classmethod
def setup_class(cls):
    cls.setup()

class TestFuncBodhi():

    def setup(self):
        self.db_fd, mock_fedorainfra.boji.app.config['DATABASE'] = tempfile.mkstemp()
        print "tempfiledb: %s" % mock_fedorainfra.boji.app.config['DATABASE']
        mock_fedorainfra.database.db_url = 'file://%s' % self.db_fd
        self.app = mock_fedorainfra.boji.app.test_client()
        mock_fedorainfra.boji.init_db()

    def mock_bodhi_query(self, package, limit):
        print self.ref_query
        return json.dumps(self.ref_query)

    def test_get_comment(self, monkeypatch):
        self.ref_query = util.make_default_update()

        monkeypatch.setattr(mock_fedorainfra.boji, 'get_bodhi_connection', get_mock_bodhi)
        monkeypatch.setattr(mock_fedorainfra.database, 'db_url', 'file://%s' % self.db_fd)

        test_result = self.app.post('/bodhi/list', data={'package':'foo', 'limit':10})

        test_comments = json.loads(test_result.data)['updates'][0]['comments']
        assert len(test_comments) == 0

    def test_make_comment(self, monkeypatch):
        ref_user = 'nobody'
        ref_title = 'nothing-1.2.3-4.fc99'
        ref_comment = 'this is a random comment'

        monkeypatch.setattr(mock_fedorainfra.boji, 'get_bodhi_connection', get_mock_bodhi)
        monkeypatch.setattr(mock_fedorainfra.database, 'db_url', 'file://%s' % self.db_fd)

        test_result = self.app.post('/bodhi/comment', data={'title':ref_title, 'text': ref_comment, 'user_name': ref_user, 'karma':0, 'email': 'False', 'password': 'password' })

        test_comments = json.loads(self.app.post('/bodhi/list', data={'package': ref_title, 'limit':10}).data)['updates']

        assert len(test_comments) == 1
        assert len(test_comments[0]['comments']) == 1
        assert test_comments[0]['comments'][0]['text'] == ref_comment
