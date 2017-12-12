## How to enable Google Vision API

In order to use Google Vision API you have to obtain an API Key.
Follow the instructions on https://cloud.google.com/vision/docs/how-to.
After obtaining the key, set the environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to the key file.

## How to run application:

* install Python 3.6
* git clone https://github.com/tpiwonski/ImageVision.git
* cd ImageVision
* python -m venv env
* env\Scripts\activate.bat
* pip install -r requirements.txt
* cd src\imagevision\
* pip install -e .
* cd imagevision
* set FLASK_APP=imagevision
* flask create_db
* flask run

## How to run tests:

* cd tests
* python -m unittest test_functional.py
