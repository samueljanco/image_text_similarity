from setuptools import setup

APP = ['app.py']
DATA_FILES = [
    ('similarity_model', ['similarity_model/fingerprint.pb', 'similarity_model/keras_metadata.pb', 'similarity_model/saved_model.pb']),
    ('similarity_model/variables', ['similarity_model/variables/variables.data-00000-of-00001', 'similarity_model/variables/variables.index'])
]
OPTIONS = {
    'packages': []
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
