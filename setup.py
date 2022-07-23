from setuptools import setup

setup(
   name='quadrature-encoder-code-challenge',
   version='0.1.0',
   author='cryptic-wizard',
   packages=['quadrature_encoder_code_challenge'],
   url='https://github.com/cryptic-wizard/quadrature-encoder-code-challenge',
   license='LICENSE.md',
   description='A command line tool to determine if quadrature encoder sensor data is valid',
   long_description=open('README.md').read(),
   install_requires=[
      "inkpot",
      "behave",
   ],
)