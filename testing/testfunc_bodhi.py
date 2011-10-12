import pytest
import bunch
import json
import mock_fedorainfra.boji
import tempfile

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
#    print 'comments: %s ' % json.dumps(comments)
    bugs = [make_bug(123456, 'random bug titles are awesome')]
#    print 'bugs: %s' % json.dumps(bugs)
    builds = [make_build('nothing', '1.2.3-4.fc99')]
#    print 'builds: %s' % json.dumps(builds)
    updates = [make_update(builds, 'nothing-1.2.3-4.fc99', bugs, comments)]
#    print 'updates: %s' % json.dumps(updates)
    return make_query_response(updates)

class MockBodhi():
    def __init__(self, update):
        self.update = update

    def query(self, package, limit):
        return bunch.Bunch(self.update)

def get_mock_bodhi():
    return MockBodhi(make_default_update())

@classmethod
def setup_class(cls):
    cls.setup()

class TestFuncBodhi():

    def setup(self):
        self.db_fd, mock_fedorainfra.boji.app.config['DATABASE'] = tempfile.mkstemp()
        print "tempfiledb: %s" % mock_fedorainfra.boji.app.config['DATABASE']
        self.app = mock_fedorainfra.boji.app.test_client()
        mock_fedorainfra.boji.init_db()

    def mock_bodhi_query(self, package, limit):
        print self.ref_query
        return json.dumps(self.ref_query)

    def test_get_comment(self, monkeypatch):
        self.ref_query = make_default_update()

        monkeypatch.setattr(mock_fedorainfra.boji, 'get_bodhi_connection', get_mock_bodhi)

        test_result = self.app.post('/bodhi/list', data={'package':'foo', 'limit':10})

        test_comments = json.loads(test_result.data)['updates'][0]['comments']
        assert len(test_comments) == 0

    def test_make_comment(self, monkeypatch):
        ref_user = 'nobody'
        ref_title = 'nothing-1.2.3-4.fc99'
        ref_comment = 'this is a random comment'

        monkeypatch.setattr(mock_fedorainfra.boji, 'get_bodhi_connection', get_mock_bodhi)

        test_result = self.app.post('/bodhi/comment', data={'title':ref_title, 'text': ref_comment, 'user_name': ref_user, 'karma':0, 'email': 'False', 'password': 'password' })

        test_comments = json.loads(self.app.post('/bodhi/list', data={'package': ref_title, 'limit':10}).data)['updates']

        assert len(test_comments) == 1
        assert len(test_comments[0]['comments']) == 1
        assert test_comments[0]['comments'][0]['text'] == ref_comment
