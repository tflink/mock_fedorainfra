#
# boji.py - mock koji XML-RPC and bodhi RESTful interface
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


from __future__ import with_statement
from flask import Flask, request, g, url_for, render_template, flash, redirect
from flaskext.xmlrpc import XMLRPCHandler, Fault
import mock_fedorainfra.koji.mock_koji as mock_koji
import json
from contextlib import closing
from datetime import datetime
import fedora.client
from mock_fedorainfra.database import db_session, init_db
from mock_fedorainfra.models import BodhiComment

# configuration
DATABASE = '/tmp/boji.db'
DEBUG = True
SECRET_KEY = 'test key'

default_response = {"num_items": 1, "title": "1 update found", "tg_flash": None, "updates": [{"status": "testing", "close_bugs": False, "request": None, "date_submitted": "2011-05-25 16:14:36", "unstable_karma": -3, "submitter": "cebbert", "critpath": True, "approved": None, "stable_karma": 3, "date_pushed": "2011-05-26 21:13:37", "builds": [{"nvr": "kernel-2.6.35.13-92.fc14", "package": {"suggest_reboot": True, "committers": ["kernel-maint", "nhorman", "cebbert", "glisse", "jwrdegoede", "davej", "linville", "steved", "airlied", "oliver", "chrisw", "myoung", "roland", "dwmw2", "jwilson", "mjg59", "eparis", "josef", "ajax", "bskeggs", "dcbw", "markmc", "quintela", "mchehab", "jforbes", "sandeen", "kyle", "katzj"], "name": "kernel"}}], "title": "kernel-2.6.35.13-92.fc14", "notes": "Some small but critical bug fixes and one security fix.", "date_modified": None, "nagged": None, "bugs": [{"bz_id": 703011, "security": True, "parent": True, "title": "CVE-2011-1770 kernel: dccp: handle invalid feature options length"}, {"bz_id": 704059, "security": False, "parent": False, "title": "Machine doesn\'t smoothly boot after installing 2.6.35.13-91.fc14.x86_64"}, {"bz_id": 704125, "security": False, "parent": False, "title": "kernel-2.6.35.13-91 breaks  mount.cifs"}], "comments": [{"group": None, "karma": 0, "anonymous": False, "author": "bodhi", "timestamp": "2011-05-25 16:15:20", "text": "This update has been submitted for testing by cebbert. "}, {"group": None, "karma": 0, "anonymous": False, "author": "autoqa", "timestamp": "2011-05-25 16:43:08", "text": "AutoQA: depcheck test PASSED on i386. Result log:\nhttp://autoqa.fedoraproject.org/results/101163-autotest/172.16.0.17/depcheck/results/output.log\n(results are informative only)"}, {"group": None, "karma": 0, "anonymous": False, "author": "autoqa", "timestamp": "2011-05-25 16:44:11", "text": "AutoQA: depcheck test PASSED on x86_64. Result log:\nhttp://autoqa.fedoraproject.org/results/101162-autotest/172.16.0.18/depcheck/results/output.log\n(results are informative only)"}, {"group": None, "karma": 0, "anonymous": False, "author": "bodhi", "timestamp": "2011-05-26 21:50:11", "text": "This update has been pushed to testing"}, {"group": None, "karma": 1, "anonymous": False, "author": "sanchan", "timestamp": "2011-05-27 06:56:43", "text": "704125 verified, works fine here."}, {"group": None, "karma": -1, "anonymous": True, "author": "Paran0rmaL1983@gmail.com", "timestamp": "2011-05-27 11:51:53", "text": "again does not work kmod-nvidia driver"}, {"group": "proventesters", "karma": 1, "anonymous": False, "author": "watzkej", "timestamp": "2011-05-31 01:17:49", "text": "kernel still boots and works fine"}, {"group": None, "karma": 0, "anonymous": False, "author": "bodhi", "timestamp": "2011-05-31 01:17:49", "text": "Critical path update approved"}, {"group": None, "karma": 1, "anonymous": False, "author": "sanchan", "timestamp": "2011-05-31 11:38:25", "text": "@Paran0rmaL1983: just use rpmfusion-nonfree-updates-testing, kmod-nvidia driver\nworks fine."}, {"group": None, "karma": 1, "anonymous": True, "author": "kks@iki.fi", "timestamp": "2011-06-01 06:11:01", "text": "704059 OK now"}], "critpath_approved": True, "updateid": "FEDORA-2011-7551", "karma": 2, "release": {"dist_tag": "dist-f14", "id_prefix": "FEDORA", "locked": False, "name": "F14", "long_name": "Fedora 14"}, "type": "security"}]}

koji_getbuild_resp = {'owner_name': 'cebbert', 'package_name': 'kernel', 'task_id': 3085371, 'creation_event_id': 3729725, 'creation_time': '2011-05-21 17:16:58.584573', 'epoch': None, 'nvr': 'kernel-2.6.35.13-92.fc14', 'name': 'kernel', 'completion_time': '2011-05-21 18:37:45.561815', 'state': 1, 'version': '2.6.35.13', 'release': '92.fc14', 'creation_ts': 1305998218.58457, 'package_id': 8, 'id': 244715, 'completion_ts': 1306003065.56182, 'owner_id': 417}

app = Flask(__name__)
#app.debug = True
app.config.from_object(__name__)
init_db()

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

def get_bodhi_connection():
    return fedora.client.bodhi.BodhiClient()

handler = XMLRPCHandler('mockkoji')
handler.connect(app, '/mockkoji')

@handler.register
def getBuild(nvr):
    if nvr is None:
        raise Fault("no_build", "there has to be some build passed in!")

    k = mock_koji.MockKoji()
    return k.get_build(nvr)

@handler.register
def listTagged(args):
    print args
    params, opts = decode_args(*args)
    k = mock_koji.MockKoji()
    return k.get_tags(*params, **opts)

@handler.register
def tagHistory(args):
    print args
    print type(args)
    if type(args) != str:
        params, opts = decode_args(*args)
    else:
        params = (args,)
        opts = {}
    print params
    print opts
    k = mock_koji.MockKoji()
    return k.tag_history(*params, **opts)

@handler.register
def listBuilds(args):
    if type(args) != dict:
        params, opts = decode_args(*args)
    else:
        params = ()
        opts = args
        del opts['__starstar']
    print params
    print opts
    k = mock_koji.MockKoji()
    return k.list_builds(*params, **opts)

@app.route('/bodhi/comment', methods=['POST'])
def bodhi_comment():
    current_time = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    db_session.add(BodhiComment(current_time, str( request.form['title']),
                str(request.form['text']), str(request.form['user_name']),
                int(request.form['karma']), request.form['email'] in ['false', 'False']))
    db_session.commit()
    return json.dumps(default_response)

@app.route('/bodhi/list', methods=['POST','GET'])
def bodhi_list():
    # we need username, release, package, request, status, type_, bugs, mine
    user= release= package= bodhirequest= status= update_type= bugs= mine = ''
    limit = 1

    if 'username' in request.form.keys():
        user = str(request.form['username'])
    if 'release' in request.form.keys():
        release = str(request.form['release'])
    if 'package' in request.form.keys():
        package = str(request.form['package'])
    if 'request' in request.form.keys():
        bodhirequest = str(request.form['request'])
    if 'status' in request.form.keys():
        status = str(request.form['status'])
    if 'type_' in request.form.keys():
        update_type = str(request.form['type_'])
    if 'bugs' in request.form.keys():
        bugs = request.form['bugs']
    if 'mine' in request.form.keys():
        mine = str(request.form['mine'])
    if 'tg_paginate_limit' in request.form.keys():
        limit = int(request.form['tg_paginate_limit'])

    bodhi = get_bodhi_connection()
    result = bodhi.query(package=package, limit=limit).toDict()
    for update in result['updates']:
        comments = search_comments(update['title'])
        update['comments'] = comments
    return json.dumps(result)

def search_comments(update):
    c = db_session.query(BodhiComment).filter(BodhiComment.title == update).order_by(BodhiComment.id)
    comments = [dict(timestamp=row.date, update=row.title,text=c.text, author=row.username,
                    karma=row.karma, anonymous=False, group=None) for row in c]
    return comments

def get_comments():
    c = db_session.query(BodhiComment).order_by(BodhiComment.id)
    comments = [dict(date=str(row.date), update=row.title, text=row.text, user=row.username,
                karma=row.karma, send_email=row.send_email) for row in c]
    return comments

@app.route('/view/bodhi_comments')
def view_bodhi_comments():
    comments = get_comments()
    return render_template('view_comments.html', bodhi_comments=comments)


@app.route('/util/cleardb', methods=['POST'])
def clear_db():
    db_session.execute('delete from comments')
    db_session.commit()
    flash('Database was cleared')
    return redirect(url_for('view_bodhi_comments'))

def decode_args(*args):
    """Decodes optional arguments from a flat argument list

    Complementary to encode_args
    Returns a tuple (args,opts) where args is a tuple and opts is a dict
    """
    print args
    opts = {}
    if len(args) > 0:
        if type(args) == dict:
            return (),args

        last = args[-1]
        if type(last) == dict and last.get('__starstar',False):
            del last['__starstar']
            opts = last
            args = args[:-1]
            # this is a bit of a dirty hack, didn't want to enable
            # allow_none right now
            if args[0] == '__none':
                args = ()

    return args,opts

if __name__ == '__main__':
    app.run(host='localhost')
