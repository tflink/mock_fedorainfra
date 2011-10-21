from fabric.api import *

# the user to use for the remote commands
#env.user = 'root'
# the servers where the commands are executed
#env.hosts = ['localhost']

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/boji.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/boji')
    with cd('/tmp/boji'):
        run('tar xzf /tmp/boji.tar.gz')

        with cd(dist):
            # now setup the package with our virtual environment's
            # python interpreter
            run('/var/www/boji/env/bin/python setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/boji /tmp/boji.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/boji.wsgi')
