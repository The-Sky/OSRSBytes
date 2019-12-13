from setuptools import setup

setup(
   name='OSRSScraper',
   version='1.0',
   description='A more up to date version of OSRSBytes',
   author='The-Sky',
   author_email='N/A',
   packages=['OSRSScraper'],  #same as name
   install_requires=['pymysql', 'loguru'], #external packages as dependencies
)
