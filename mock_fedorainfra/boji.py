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
from mock_fedorainfra import util

# configuration
DATABASE = '/tmp/boji.db'
DEBUG = True
SECRET_KEY = 'test key'
NUM_PAGE = 20

default_response = util.make_default_update()

koji_getbuild_resp = {'owner_name': 'cebbert', 'package_name': 'kernel', 'task_id': 3085371, 'creation_event_id': 3729725, 'creation_time': '2011-05-21 17:16:58.584573', 'epoch': None, 'nvr': 'kernel-2.6.35.13-92.fc14', 'name': 'kernel', 'completion_time': '2011-05-21 18:37:45.561815', 'state': 1, 'version': '2.6.35.13', 'release': '92.fc14', 'creation_ts': 1305998218.58457, 'package_id': 8, 'id': 244715, 'completion_ts': 1306003065.56182, 'owner_id': 417}

app = Flask(__name__)
#app.debug = True
app.config.from_object(__name__)
init_db()

handler = XMLRPCHandler('mockkoji')
handler.connect(app, '/mockkoji')

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

def get_bodhi_connection():
    return fedora.client.bodhi.BodhiClient()

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
        raw_comments = search_comments(update['title'])
        comments = [dict(timestamp=row['date'], update=row['update'] ,text=row['text'], author=row['user'],
                    karma=row['karma'], anonymous=False, group=None) for row in raw_comments]
        update['comments'] = comments
    return json.dumps(result)

def search_comments(update):
    c = db_session.query(BodhiComment).filter(BodhiComment.title.like('%%%s%%' % update)).order_by(BodhiComment.id)
    comments = [dict(date=str(row.date), update=row.title, text=row.text, user=row.username,
                karma=row.karma, send_email=row.send_email, id=row.id) for row in c]
    return comments

def get_comments(start=0, num_comments=NUM_PAGE):
    c = db_session.query(BodhiComment).order_by(BodhiComment.id).slice(start, start+num_comments)
    comments = [dict(date=str(row.date), update=row.title, text=row.text, user=row.username,
                karma=row.karma, send_email=row.send_email, id=row.id ) for row in c]
    return comments

@app.route('/boji/comments', methods=['GET'])
def default_boji_comments():
    return redirect('/boji/comments/0')

@app.route('/boji/comments/<int:start_comment>', methods=['GET'])
def boji_comments(start_comment):
    comments = get_comments(start=start_comment)
    for c in comments:
        c['url'] = url_for('get_boji_comment', comment_id=c['id'])
    next_start = (start_comment + NUM_PAGE)
    prev_start = (start_comment - NUM_PAGE)
    if prev_start < 0:
        prev_start = 0
    return render_template('view_comments.html', bodhi_comments=comments, next_start= next_start, prev_start= prev_start)

@app.route('/boji/comments/search', methods=['GET', 'POST'])
def boji_search_comments():
    if request.method == 'GET':
        return render_template('search_comments.html')
    elif request.method == 'POST':
        if 'title' in request.form.keys():
            comments = search_comments(request.form['title'])
        return render_template('view_comments.html', bodhi_comments=comments, next_start= 0, prev_start=0)

@app.route('/boji/comment/<int:comment_id>', methods = ['GET', 'POST', 'DELETE'])
def get_boji_comment(comment_id):
    c = db_session.query(BodhiComment).filter(BodhiComment.id == comment_id).first()

    if request.method == 'GET':
        comment = dict(date=str(c.date), update=c.title, text=c.text, user=c.username, karma=c.karma, send_email=c.send_email, id=c.id)
        return render_template('comment_detail.html', comment = comment)

    # stupid browsers not supporting HTTP delete calls ...
    elif request.method == 'POST':
        if request.form['request'] == 'DELETE':
            db_session.delete(c)
            db_session.commit()
            flash('Comment %d was deleted' % comment_id)
            return redirect(url_for('default_boji_comments'))

    elif request.method == 'DELETE':
        db_session.delete(c)
        db_session.commit()
        return (url_for('default_boji_comments'))

@app.route('/boji/', methods = ['GET'])
def boji_main():
    return render_template('boji_main.html')

@app.route('/util/cleardb', methods=['POST'])
def clear_db():
    db_session.execute('delete from comments')
    db_session.commit()
    flash('Database was cleared')
    return redirect(url_for('default_boji_comments'))

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
