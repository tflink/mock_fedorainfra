#
# mock_koji.py - supporting methods for mock Koji XML-RPC interface
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

class MockKoji:
    kernel_build = {'owner_name': 'cebbert', 'package_name': 'kernel', 'task_id': 3085371, 'creation_event_id': 3729725, 'creation_time': '2011-05-21 17:16:58.584573', 'epoch': None, 'nvr': 'kernel-2.6.35.13-92.fc14', 'name': 'kernel', 'completion_time': '2011-05-21 18:37:45.561815', 'state': 1, 'version': '2.6.35.13', 'release': '92.fc14', 'creation_ts': 1305998218.58457, 'package_id': 8, 'id': 244715, 'completion_ts': 1306003065.56182, 'owner_id': 417}

    kernel_taginfo = [{'build_id': 244715, 'tag_name': 'dist-f14-updates-testing', 'owner_name': 'cebbert', 'package_name': 'kernel', 'task_id': 3085371, 'creation_event_id': 3729725, 'creation_time': '2011-05-21 17:16:58.584573', 'epoch': None, 'tag_id': 124, 'name': 'kernel', 'completion_time': '2011-05-21 18:37:45.561815', 'state': 1, 'version': '2.6.35.13', 'release': '92.fc14', 'package_id': 8, 'owner_id': 417, 'id': 244715, 'nvr': 'kernel-2.6.35.13-92.fc14'}]

    ref_10minlist = [{'build_id': 246080, 'owner_name': 'robert', 'package_name': 'x509watch', 'task_id': 3106391, 'creation_event_id': 3749646, 'creation_time': '2011-06-02 16:42:38.806448', 'epoch': None, 'nvr': 'x509watch-0.4.0-1.fc16', 'name': 'x509watch', 'completion_time': '2011-06-02 16:44:24.829474', 'state': 1, 'version': '0.4.0', 'release': '1.fc16', 'creation_ts': 1307032958.80645, 'completion_ts': 1307033064.82947, 'package_id': 10743, 'owner_id': 221}, {'build_id': 246081, 'owner_name': 'robert', 'package_name': 'x509watch', 'task_id': 3106397, 'creation_event_id': 3749652, 'creation_time': '2011-06-02 16:43:34.421701', 'epoch': None, 'nvr': 'x509watch-0.4.0-1.fc14', 'name': 'x509watch', 'completion_time': '2011-06-02 16:45:12.723749', 'state': 1, 'version': '0.4.0', 'release': '1.fc14', 'creation_ts': 1307033014.4217, 'completion_ts': 1307033112.72375, 'package_id': 10743, 'owner_id': 221}, {'build_id': 246083, 'owner_name': 'robert', 'package_name': 'x509watch', 'task_id': 3106395, 'creation_event_id': 3749654, 'creation_time': '2011-06-02 16:43:36.973323', 'epoch': None, 'nvr': 'x509watch-0.4.0-1.fc15', 'name': 'x509watch', 'completion_time': '2011-06-02 16:45:19.614729', 'state': 1, 'version': '0.4.0', 'release': '1.fc15', 'creation_ts': 1307033016.97332, 'completion_ts': 1307033119.61473, 'package_id': 10743, 'owner_id': 221}]


    kernel_taghistory = [{'build_id': 244715, 'create_event': 3729762, 'name': 'kernel', 'creator_name': 'cebbert', 'revoke_ts': 1306430067.66783, 'tag_name': 'dist-f14-updates-candidate', 'tag_id': 120, 'revoke_event': 3737993, 'release': '92.fc14', 'creator_id': 417, 'version': '2.6.35.13', 'revoker_id': 428, 'active': None, 'revoker_name': 'bodhi', 'create_ts': 1306003070.64702}, {'build_id': 244715, 'create_event': 3737993, 'name': 'kernel', 'creator_name': 'bodhi', 'revoke_ts': None, 'tag_name': 'dist-f14-updates-testing', 'tag_id': 124, 'revoke_event': None, 'release': '92.fc14', 'creator_id': 428, 'version': '2.6.35.13', 'revoker_id': None, 'active': True, 'revoker_name': None, 'create_ts': 1306430067.66783}, {'build_id': 244715, 'create_event': 3736082, 'name': 'kernel', 'creator_name': 'bodhi', 'revoke_ts': 1306430448.73177, 'tag_name': 'dist-f14-updates-testing-pending', 'tag_id': 160, 'revoke_event': 3738042, 'release': '92.fc14', 'creator_id': 428, 'version': '2.6.35.13', 'revoker_id': 428, 'active': None, 'revoker_name': 'bodhi', 'create_ts': 1306340123.33062}]

    def __init__(self):
        self.builds = {'kernel':self.kernel_build}

    def get_build(self, nvr):
        return self.builds['kernel']

    def get_tags(self, tag, package=None, latest=True):
        return self.kernel_taginfo

    def list_builds(self, completeAfter=0):
        return self.ref_10minlist

    def tag_history(self, nvr):
        return self.kernel_taghistory

