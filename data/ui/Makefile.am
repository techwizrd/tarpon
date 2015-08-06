uidir = $(pkgdatadir)/ui
ui_DATA = menu.ui menubar.ui about_dialog.ui about_dialog_hb.ui

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
	-e 's,[@]pkgdatadir[@],$(pkgdatadir),g' \
	-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
	-e 's,[@]VERSION[@],$(VERSION),g' 

about_dialog.ui: about_dialog.ui.in Makefile
	$(do_substitution) < about_dialog.ui.in > about_dialog.ui

about_dialog_hb.ui: about_dialog_hb.ui.in Makefile
	$(do_substitution) < about_dialog_hb.ui.in > about_dialog_hb.ui

EXTRA_DIST = $(ui_DATA)
