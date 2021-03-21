#!/bin/sh

pip install virtualenv

rm -rf venv || echo 'No venv folder'

virtualenv venv

source venv/Scripts/activate

pip install -r requirements.txt
pyinstaller --clean png2photon.spec