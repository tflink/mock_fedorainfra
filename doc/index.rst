mock_fedorainfra Documentation
============================================

mock_fedorainfra is a partial implementation of the Fedora infrastructure to use for
testing without needing to actually set up instances of all the services.

The project was initially designed to assist in the testing of AutoQA.

At this point, this is a very QnD project and the code is really ugly. Use at
your own risk and know that everything is likely to change in the not so far
future.

Capabilities:
    - Capturing bodhi comments
    - Proxying bodhi queries
    - Providing fake data for koji queries

Installation
==============
Since it is unlikely that this would ever be installed outside a Fedora
environment, these installation instructions are for Fedora.

Local Preparation
------------------

Boji uses fabric to do the remote deployments, so you'll need that locally
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

Install boji
------------

From a local host, run
 ``fab -u <remote_user> -H <remote_host> pack deploy``

Fabric will prompt you for the remote password once while installing.


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

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

