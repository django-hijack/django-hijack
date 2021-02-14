MSGLANGS = $(wildcard hijack/locale/*/LC_MESSAGES/*.po)
MSGOBJS = $(MSGLANGS:.po=.mo)

.PHONY: gettext gettext-clean msgcheck translations static dist clean

translations:
	(cd hijack && django-admin makemessages --all --no-obsolete)

gettext: $(MSGOBJS)

gettext-clean:
	-rm $(MSGOBJS)

%.mo: %.po
	msgfmt --check-format --check-domain --statistics -o $@ $*.po

msgcheck:
	msgcheck -n $(MSGLANGS)

static:
	npm ci
	npm run build

dist: static gettext
	python -m pip install --upgrade pip setuptools wheel twine
	python setup.py sdist bdist_wheel

clean: gettext-clean
	-rm -rf dist build .eggs
