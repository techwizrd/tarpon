SUBDIRS = tarpon_app

bin_SCRIPTS = tarpon
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = tarpon.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
	-e 's,[@]pkgdatadir[@],$(pkgdatadir),g' \
	-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
	-e 's,[@]VERSION[@],$(VERSION),g' 

tarpon: tarpon.in Makefile
	$(do_substitution) < $(srcdir)/tarpon.in > tarpon
	chmod +x tarpon

