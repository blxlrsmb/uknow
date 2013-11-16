..  $File: devnotes.rst
    $Date: Sat Nov 16 22:59:02 2013 +0800
    -----------------------------------------------------------------
    Copyright (C) 2012 the uknow development team <see AUTHORS file>
    Contributors to this file:
       Kai Jia	<jia.kai66@gmail.com>
    -----------------------------------------------------------------
    This file is part of uknow
    uknow is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    uknow is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with uknow.  If not, see <http://www.gnu.org/licenses/>.


Notes for Developers
====================

.. contents::

Contact Kai Jia <jia.kai66@gmail.com> if you have any question about this page.


Getting Started
---------------


Environment Setup
^^^^^^^^^^^^^^^^^

#.  Install MongoDB, Redis and their development packages if you don't already
    have them installed.  Usually this is via your system's package
    manager.

#.  Install virtualenv:

    .. code-block:: sh

        $ sudo pip install virtualenv

#.  Install python packages as dependencies

    .. code-block:: sh

        $ cd manage
        $ ./quickinstall

.. _devnotes.sysconf:

Configuration
^^^^^^^^^^^^^

The static system configuration file is :mod:`manage/config.py`, allowing the
developers applying their local settings without having to change the system
defaults.

An example file::

    FRONTEND_PORT = 4999
    API_PORT = 5000

    API_RUN_OPTIONS = {
        'debug': True
    }

    FRONTEND_RUN_OPTIONS = {
        'debug': True
    }


Miscellaneous Specifications and Instructions
---------------------------------------------

Framework
^^^^^^^^^

`Flask`_ is used as the web framework, and `MongoDB`_ as the database


Code Style
^^^^^^^^^^

Follow the `Style Guide for Python Code`_.  Use `pylint`_ to check the style and
find potential bugs. Execute the *run-pylint* script to invoke pylint.

The following lines should be included in every Python source file::

    # $File: <file name>
    # $Date: <last modification time>
    #
    # Copyright (C) 2012 the uknow development team <see AUTHORS file>
    #
    # Contributors to this file:
    #    <you name and email here>
    #
    # This file is part of uknow
    #
    # uknow is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # uknow is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with uknow.  If not, see <http://www.gnu.org/licenses/>.
    #

Configure your editor to update the *$File* and *$Date* fields automatically.
Add your name to the contributors field and the AUTHORS file.

By the way, if vim is your favorite, you can add the following lines to
your vimrc:

.. code-block:: vim

    autocmd filetype python set expandtab
    autocmd filetype python set textwidth=79


.. _devnotes.documenting:

Documenting
^^^^^^^^^^^

Write docstrings for every package, module, public class, public method, public
function, etc. The documents should be written in English.

Register all the global names in :ref:`global-name-list`.

These documents are generated from `reStructuredText`_ sources and docstrings by
`Sphinx`_.  Issue the following command to generate all the documents:

.. code-block:: sh

    $ cd <path-to-uknow-source-root>/docs/api
    $ ./gendoc.sh




.. links
.. _Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008
.. _pylint: http://pypi.python.org/pypi/pylint
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org/
.. _Flask: http://flask.pocoo.org/
.. _MongoDB: http://www.mongodb.org/
