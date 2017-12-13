from setuptools import setup

setup(
    name='imagevision',
    packages=['imagevision'],
    include_package_data=True,
    install_requires=[
        'flask', 'sqlalchemy', 'google-cloud-vision'
    ],
)