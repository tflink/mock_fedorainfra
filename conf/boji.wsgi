activate_this = '/var/www/boji/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from mock_fedorainfra.boji import app as application
