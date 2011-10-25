#
# util.py - Utility Functions for boji
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

# since there is so much functionality in boji that isn't important to us
# from a mock perspective, it's easier to just make up a lot of the data
# that would normally be returned from bodhi/koji

default_date = '2000-01-23 12:34:56'

def make_comment(comment):
    return {'group':None, 'karma':0, 'anonymous':False, 'author':'nobody', 'timestamp': default_date, 'text': comment}

def make_bug(bug_id, title):
    return {'bz_id': bug_id, 'security': False, 'parent': True, 'title': title}

def make_update(builds, title, bugs, comments):
    update =  {'status': 'testing', 'close_bugs': False, 'request': None,
            'date_submitted': default_date, 'unstable_karma': -3, 'submitter': 'nobody',
            'critpath': False, 'approved': None, 'stable_karma': 3,
            'date_pushed': default_date, 'builds': builds, 'title': title,
            'notes': 'no notes', 'date_modified': None, 'nagged': None,
            'bugs': bugs, 'comments': comments}
    return update

def make_query_response(updates):
    num_updates = len(updates)
    return {'num_updates': num_updates, 'title': '%d updates found' % num_updates, 'tg_flash': None, 'updates':updates}

def make_build(name, version):
    return {'nvr': '%s-%s' % (name, version), 'package': {'suggest_reboot':
            False, 'committers': ['unicorn-devel', 'django-pony', 'testing-goat'],
            'name': name}}

def make_default_update():
    comments = [make_comment('random, useless comment'), make_comment('another random, useless comment')]
    bugs = [make_bug(123456, 'random bug titles are awesome')]
    builds = [make_build('nothing', '1.2.3-4.fc99')]
    updates = [make_update(builds, 'nothing-1.2.3-4.fc99', bugs, comments)]
    return make_query_response(updates)

