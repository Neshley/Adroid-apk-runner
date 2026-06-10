# Makefile for File Organizer Pro

.PHONY: run build clean test diagnostic

run:
	python src/file_organizer_pro.py

apk:
	python apk_runner.py

diagnostic:
	python apk_diagnostic.py

build:
	python -m PyInstaller --onefile --windowed --name=FileOrganizerPro src/file_organizer_pro.py

build-apk:
	python -m PyInstaller --onefile --windowed --name=APKRunner apk_runner.py

clean:
	rmdir /S /Q build dist 2>nul
	del *.spec 2>nul

test:
	python -m pytest tests/

lint:
	pylint src/*.py

format:
	black src/*.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

all: clean build