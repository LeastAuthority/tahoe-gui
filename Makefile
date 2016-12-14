SHELL := /bin/bash

test:
	tox

pytest:
	@case `uname` in \
		Linux) xvfb-run -a python -m pytest || exit 1;;\
		Darwin) python -m pytest || exit 1;;\
	esac

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf .tox/
	rm -rf htmlcov/
	rm -f .coverage
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

ico:
	mkdir -p build/ico
	for i in 16 32 48 256; do \
        convert \
            -scale $$i\x$$i \
            -gravity center \
            -extent $$i\x$$i \
            -background transparent \
            images/icon.svg  \
            build/ico/icon-$$i\-$$i.png; \
    done
	# from 'icoutils' debian package
	icotool --create \
        build/ico/icon-16-16.png \
        build/ico/icon-32-32.png \
        build/ico/icon-48-48.png \
        build/ico/icon-256-256.png \
        -o images/icon.ico

png:
	mkdir -p build
	convert -scale 1024x1024 \
		-gravity center \
		-extent 1024x1024 \
		-background transparent \
		images/icon.svg images/icon.png;
	
icns:
	mkdir -p build/icon.iconset
	# OS X only
	sips \
        -s format png \
        --resampleWidth 1024 \
        images/icon.png \
        --out build/icon.iconset/icon_512x512@2x.png
	sips \
        -s format png \
        --resampleWidth 512 \
        images/icon.png \
        --out build/icon.iconset/icon_512x512.png
	cp build/icon.iconset/icon_512x512.png \
        build/icon.iconset/icon_256x256@2x.png
	sips \
        -s format png \
        --resampleWidth 256 \
        images/icon.png \
        --out build/icon.iconset/icon_256x256.png
	cp build/icon.iconset/icon_256x256.png \
        build/icon.iconset/icon_128x128@2x.png
	sips \
        -s format png \
        --resampleWidth 128 \
        images/icon.png \
        --out build/icon.iconset/icon_128x128.png
	sips \
        -s format png \
        --resampleWidth 64 \
        images/icon.png \
        --out build/icon.iconset/icon_32x32@2x.png
	sips \
        -s format png \
        --resampleWidth 32 \
		images/icon.png \
		--out build/icon.iconset/icon_32x32.png
	cp build/icon.iconset/icon_32x32.png \
        build/icon.iconset/icon_16x16@2x.png
	sips \
        -s format png \
        --resampleWidth 16 \
        images/icon.png \
        --out build/icon.iconset/icon_16x16.png
	iconutil -c icns build/icon.iconset
	mv build/icon.icns images

sip:
	mkdir -p build/sip
	curl --progress-bar --retry 20 --output "build/sip.tar.gz" --location \
		"https://sourceforge.net/projects/pyqt/files/sip/sip-4.18.1/sip-4.18.1.tar.gz"
	tar zxf build/sip.tar.gz -C build/sip --strip-components=1
	cd build/sip && $${PYTHON=python} configure.py --incdir=build/sip/sipinc
	$(MAKE) -C build/sip -j 4
	$(MAKE) -C build/sip install || sudo $(MAKE) -C build/sip install

pyqt: sip
	mkdir -p build/pyqt
	curl --progress-bar --retry 20 --output "build/pyqt.tar.gz" --location \
		"https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.7/PyQt5_gpl-5.7.tar.gz"
	tar zxf build/pyqt.tar.gz -C build/pyqt --strip-components=1
	cd build/pyqt && \
		QT_SELECT=qt5 $${PYTHON=python} configure.py \
			--confirm-license \
			--sip ../sip/sipgen/sip \
			--sip-incdir ../sip/siplib \
			--enable QtCore \
			--enable QtGui \
			--enable QtWidgets
	$(MAKE) -C build/pyqt -j 4
	$(MAKE) -C build/pyqt install || sudo $(MAKE) -C build/pyqt install

frozen-tahoe:
	# Use git since magic-folder has not yet landed (1.12?)
	# Requires libssl-dev libffi-dev
	mkdir -p dist
	rm -rf build/tahoe-lafs
	#git clone https://github.com/tahoe-lafs/tahoe-lafs.git build/tahoe-lafs
	git clone -b 1432.osx-watchdog-stable.9 \
        https://github.com/david415/tahoe-lafs.git build/tahoe-lafs
	virtualenv --clear --python=python2 build/venv-tahoe
	source build/venv-tahoe/bin/activate && \
	cp misc/tahoe.spec build/tahoe-lafs && \
	pushd build/tahoe-lafs && \
	python setup.py update_version && \
	pip install --find-links=https://tahoe-lafs.org/deps/ . && \
	pip install git+https://github.com/pyinstaller/pyinstaller.git && \
	pip install 'zope.interface==4.3.2'  # XXX: 4.3.3 broke frozen binaries..
	export PYTHONHASHSEED=1 && \
	pyinstaller tahoe.spec && \
	popd && \
	mv build/tahoe-lafs/dist/Tahoe-LAFS dist && \
	python -m zipfile -c dist/Tahoe-LAFS.zip dist/Tahoe-LAFS

app:
	# OS X only
	if [ -f dist/Tahoe-LAFS.zip ] ; then \
		python -m zipfile -e dist/Tahoe-LAFS.zip dist ; \
	else  \
		make frozen-tahoe ; \
	fi;
	virtualenv --clear --python=python3 build/venv-gui
	source build/venv-gui/bin/activate && \
	pip install --upgrade pip && \
	pip install . git+https://github.com/pyinstaller/pyinstaller.git && \
	export PYTHONHASHSEED=1 && \
	pyinstaller misc/tahoe-gui.spec
	cp misc/Info.plist dist/Tahoe-GUI.app/Contents
	mv dist/Tahoe-LAFS dist/Tahoe-GUI.app/Contents/MacOS
	chmod +x dist/Tahoe-GUI.app/Contents/MacOS/Tahoe-LAFS/tahoe

dmg: app
	virtualenv --clear --python=python2 build/venv-dmg
	source build/venv-dmg/bin/activate && \
	pip install dmgbuild && \
	dmgbuild -s misc/dmgbuild_settings.py Tahoe-GUI dist/Tahoe-GUI.dmg

all: dmg
