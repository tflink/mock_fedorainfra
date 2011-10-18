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

