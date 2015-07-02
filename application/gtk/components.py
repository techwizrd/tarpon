#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gdk, Gio, Gtk, WebKit


def toolbar_button(themed_icon, button_class):
    """
    Create new Gtk.Button or Gtk.ToogleButton from a stock Gtk icon name

    :param themed_icon: stock Gtk icon name
    :type themed_icon: str
    :param button_class: ``Gtk.Button`` or ``Gtk.ToggleButton``
    :type button_class: classobj
    :return: ``Gtk.Button`` or ``Gtk.ToggleButton`` according to button_class
    """
    image = Gtk.Image()
    image.set_from_gicon(
        Gio.ThemedIcon.new_with_default_fallbacks(themed_icon),
        Gtk.IconSize.SMALL_TOOLBAR
    )
    return button_class(None, image=image)


class Titlebar(Gtk.HeaderBar):
    def __init__(self, title=None, subtitle=None, show_close_button=True):
        super(Gtk.HeaderBar, self).__init__()
        if title:
            self.set_title(title)
        if subtitle:
            self.set_subtitle(title)
        self.set_show_close_button(True)

    def __add_buttons(self, box, buttons, linked, spacing):
        """
        Add linked or non-linked buttons to Titlebar

        :type box: Gtk.Box
        """
        box.set_spacing(spacing)
        if linked:
            Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        for button in buttons:
            box.add(button)

    def add_buttons_to_left(self, buttons, linked=False, spacing=6):
        """
        Add button(s) to left of title. If there is only one button, the button
        will be added on its own. If more than one button is provided, the
        buttons will be added to a Gtk.Box container before being add left of
        the title.

        :param buttons: a list of Gtk.Button elements to be added
        :param linked: True if the buttons should be linked together
        :param spacing: spacing in between buttons in pixels
        """
        if len(buttons) > 1:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.pack_start(box)
            self.__add_buttons(box, buttons, linked, spacing)
        elif buttons:
            self.pack_start(buttons)

    def add_buttons_to_right(self, buttons, linked=False, spacing=6):
        """
        Add button(s) to right of title. If there is only one button, the button
        will be added on its own. If more than one button is provided, the
        buttons will be added to a Gtk.Box container before being add right of
        the title.

        :param buttons: a list of Gtk.Button elements to be added
        :param linked: True if the buttons should be linked together
        :param spacing: spacing in between buttons in pixels
        """
        if len(buttons) > 1:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.pack_end(box)
            self.__add_buttons(box, buttons, linked, spacing)
        elif buttons:
            self.pack_end(buttons)


class WebNotebook(Gtk.Notebook):
    def __init__(self, new_tab_page=None):
        super(Gtk.Notebook, self).__init__()
        self.new_tab_page = new_tab_page

    def new_tab(self, widget, data=None, uri=None):
        """Create a new tab."""
        # TODO: Hiding tab bar if only one tab is present should be an option.
        if self.get_n_pages() < 1:
            self.set_show_tabs(False)
        else:
            self.set_show_tabs(True)

        sw = Gtk.ScrolledWindow()
        wv = WebKit.WebView()
        sw.add(wv)

        if uri:
            wv.load_uri(uri)
        elif self.new_tab_page:
            wv.load_uri(self.new_tab_page)

        tab_label = Gtk.Label("Tab {0}".format(self.get_n_pages() + 1))
        self.append_page(sw, tab_label)
        self.show_all()


    @property
    def browser(self):
        """
        Gets the ``WebKit.WebView`` for the current tab.

        :type self: WebKit.WebView
        :return: ``WebKit.WebView`` form current tab
        """
        return self.get_nth_page(self.get_current_page()).get_child()

    def go_back(self, widget, data=None):
        """Return to the previous page in the current tab."""
        self.browser.go_back()

    def go_forward(self, widget, data=None):
        """Return to the previous page in the next tab."""
        self.browser.go_forward()


class TarponWindow(Gtk.Window):
    def __init__(self):
        super(Gtk.Window, self).__init__(title="Tarpon")
        self.set_default_size(800, 600)
        self.set_gravity(Gdk.Gravity.CENTER)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.build_bars()
        self.set_titlebar(self.__header)
        self.__web_notebook = WebNotebook()
        self.__web_notebook.new_tab(None)
        self.__content = Gtk.Paned()
        self.__content.add(self.__web_notebook)
        self.add(self.__content)

        self.connect('delete-event', Gtk.main_quit)
        self.connect_signals()
        self.show_all()

    def build_bars(self):
        self.__header = Titlebar(title="Tarpon", show_close_button=True)

        self.__back = Gtk.Button()
        self.__back.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.__forward = Gtk.Button()
        self.__forward.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.__new_tab = toolbar_button("tab-new-symbolic", Gtk.Button)
        self.__search = toolbar_button("edit-find-symbolic", Gtk.ToggleButton)
        self.__menu = toolbar_button("open-menu-symbolic", Gtk.ToggleButton)

        # Add buttons to header
        # TODO: Add buttons to a toolbar instead of Titlebar if using Unity.
        # Unity attaches the menu to the top of the screen, so Gtk.HeaderBar
        # looks out of place and a button for opening the menu is unnecessary.
        self.__header.add_buttons_to_left((self.__back, self.__forward),
                                          linked=True, spacing=0)
        self.__header.add_buttons_to_right((self.__new_tab, self.__menu))

    def build_sidebar(self):
        # self.__sidebar = Gtk.ScrolledWindow()
        # self.__sidebar.add(Gtk.Label("hi"))
        # self.__content.add(self.__sidebar)
        self.__content.add(Gtk.Label("hi"))
        self.__content.set_position(200)

    def connect_signals(self):
        self.__back.connect("clicked", self.__web_notebook.go_back)
        self.__forward.connect("clicked", self.__web_notebook.go_forward)
        self.__new_tab.connect("clicked", self.__web_notebook.new_tab)
