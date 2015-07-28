Tarpon
======

Tarpon is an offline documentation browser written using Python and Gtk+3.

![Screenshot of Tarpon](https://raw.githubusercontent.com/techwizrd/tarpon/master/Screenshot.png)

Installing and Running
----------------------

To run Tarpon, execute it directly for now:

    $ cd tarpon
    $ python tarpon.py

In order to install Tarpon, execute the following autotools commands:

    $ aclocal
    $ autoconf
    $ automake --add-missing
    $ ./configure
    $ make
    $ make install

Uninstall Tarpon using ``make uninstall`` or install Tarpon locally (rather than system-wide) by executing ``./configure --prefix=~/.local``. A distributable package can be built using ``make dist``.

FAQ
---

1. Why did you create your UI in code instead of ``Gtk.Builder``?

Moving to ``Gtk.Builder`` and XML files is a future goal. Originally, I could not figure out how to create a ``Gtk.HeaderBar`` and have it set as the titlebar of a ``Gtk.Window`` automatically using ``Gtk.Builder``.
