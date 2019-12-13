from setuptools import setup

setup(
   name='OSRSBytes',
   version='1.0',
   description='A more up to date version of OSRSBytes',
   author='The-Sky',
   author_email='N/A',
   packages=['OSRSBytes'],  #same as name
   install_requires=['pymysql', 'loguru'], #external packages as dependencies
)
