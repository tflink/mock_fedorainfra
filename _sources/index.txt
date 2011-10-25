Boji Documentation
============================================

Boji is part of project to mock up the Fedora infrastructure for testing
purposes. Specifially, `AutoQA <http://fedorahosted.org/autoqa>`_ is
tightly coupled with `Koji <http://koji.fedoraproject.org/koji/>`_ and
`Bodhi <https://admin.fedoraproject.org/updates/>`_.

The idea is to implement only as much of those interfaces as we need so that
we can test AutoQA without needing separate instances of Koji or Bodhi.

At this point, this is a very young project and the code isn't very pretty. Use at
your own risk and know that everything is likely to change in the not so far
future.

If you find bugs or have feature requests, `please file an issue in github
<https://github.com/tflink/mock_fedorainfra/issues>`_.

Capabilities:
    - Capturing bodhi comments
    - Proxying bodhi queries

Downloads
=========
The boji code is hosted on github:
 * ``git clone git://github.com/tflink/mock_fedorainfra.git``
 * `Browsable Repository <https://github.com/tflink/mock_fedorainfra>`_

Installation
============
You can install boji in one of two ways
 * :ref:`installation-wsgi-app`
 * :ref:`installation-devel-server`




.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

