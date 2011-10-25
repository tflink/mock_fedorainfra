.. _installation-wsgi-app:

Installing Boji as a WSGI Application
================================
Since it is unlikely that this would ever be installed outside a Fedora
environment, these installation instructions are for Fedora.

Local Preparation
------------------

Boji uses fabric to do the remote deployments, so you'll need that locally
if you want to deploy to a remote server (not needed for a local install).
 ``yum install fabric``

Grab the code from github:
 ``git clone git://github.com/tflink/mock_fedorainfra.git``

Remote Host Preparation
-----------------------
Distribute takes care of most of the python dependencies on the remote host
and boji will be installed into a virtualenv, so you don't have to worry about
messing up your default python installation.

Remote Python dependencies:
  * Flask >= .8
  * Flask-XML-RPC
  * SQLAlchemy >= 0.7
  * py.test >= 2.0.0

However, there are some dependencies that need to be installed with yum.

On the target host, run:
 ``yum install httpd mod_wsgi python-virtualenv python-fedora``

On some hosts (specifically, Fedora 16) you need to append the following line
to /etc/httpd/conf.d/wsgi.conf
 ``WSGISocketPrefix /var/run/wsgi``

Initial Environment Setup
--------------------------

Setup the virtualenv used for boji
 ``mkdir /var/www/boji``
 ``cd /var/www/boji``
 ``virtualenv --distribute env``

Copy these files to the target host:
 * conf/boji.conf to /etc/httpd/conf.d
 * conf/boji.wsgi to /var/www/boji/.

Installing boji
---------------

There are two ways to install boji depending on whether you want to use fabric
or do it manually (in case you don't want to use fabric or can't use it).

Remote Installation With Fabric
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From a local host, run
 ``fab -u <remote_user> -H <remote_host> pack deploy``

Fabric will prompt you for the remote password once while installing.

Manual Installation
^^^^^^^^^^^^^^^^^^^^

If you are deploying to a local machine or something that fabric can't work with
(ie needing to forward ssh keys etc.) you can install directly.

From the directory containing a boji checkout, run:
``/var/www/boji/env/bin/python setup.py install``

To make sure that the wsgi app is reloaded, run:
``touch /var/www/boji/boji.wsgi``

Start The Server
----------------

On the remote host, run:
 ``systemctl start httpd.service``

Everything should be set and boji will now be running at ``http://hostname.domain/boji``
and everlasting happiness shall ensue ...

Updating boji
-------------

From the local machine, update the git checkout:
 ``git pull``

Run fabric to update the remote install:
 ``fab -u <remote_user> -H <remote_host> pack deploy``

The wsgi app is configured to reload on file changes, so httpd won't need to be restarted.



.. _installation-devel-server:

Using the Development Server
============================

Boji can also be run with a development server. The easiest way to do this is to
set up a virtualenv containing all of the dependencies.

``yum install python-virtualenv``
``sh runtests.sh``

Running the tests this way will set up a virtualenv for you and install all of the required
dependencies.

Development Server Configuration
--------------------------------
By default, the development server will run on localhost. This means that nothing outside the
local machine will be able to access the application. To change this, edit the main method of
boji.py.

| if __name__ == '__main__':
|    app.run(host='localhost')

Changing the ``host='localhost'`` to be ``host=<my_ipaddr>`` where <my_ipaddr> is the external
ip or hostname of your machine will allow the application to be accessed from other machines.

Starting the Development Server
-------------------------------

Before starting the development server, activate the virtualenv:

``source env_flask/bin/activate``

To start the development server:

``python mock_fedorainfra/boji.py``

By default, the development server will run on port 5000 and reloads the application
whenever you change any files associated with the application.

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

