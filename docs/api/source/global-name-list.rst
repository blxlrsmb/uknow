..  $File: global-name-list.rst
    $Date: Mon Feb 27 19:18:11 2012 +0800
    -----------------------------------------------------------------
    Copyright (C) 2012 the pynojo development team <see AUTHORS file>
    -----------------------------------------------------------------
    This file is part of pynojo
    pynojo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    pynojo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with pynojo.  If not, see <http://www.gnu.org/licenses/>.


.. _global-name-list:

Global Name List
================

The global names that are not documented in the API Reference should be listed
here.

.. contents::


Database Session
----------------

A contextual session defined in :mod:`pynojo.model` is used. To create
a session instance ``ses`` in some function, just do the following::

    from pynojo.model import Session

    def foo():
        ses = Session()
        # do something with ses

Direct invoking of :meth:`Session.commit` is usually unnecessary, except when
some operations that might fail and call :meth:`Session.rollback` are performed,
in which case :meth:`Session.commit` should be called before starting any of
those operations. The committing is performed in a subscriber defined in
:mod:`pynojo.model`.


Renderers
---------

The following renderers are provided by pynojo (see the source of
:func:`pynojo.view.setup_pyramid_conf`):

    * cjson: replace the json renderer, to gain some efficiency.



Cookies
-------

+-------------+--------------------------------+------------------------+
| Cookie Name | Description                    | Source Reference       |
+=============+================================+========================+
| uid         | the id of the user that logged | :mod:`pynojo.lib.user` |
|             | in                             |                        |
+-------------+--------------------------------+------------------------+
| token       | the authentication code of the | :mod:`pynojo.lib.user` |
+-------------+--------------------------------+------------------------+


Views
-----

.. include:: autogen/viewdoc.rst.txt
