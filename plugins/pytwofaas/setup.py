from setuptools import setup

setup(name='pytwofaas',
      version='0.18',
      description='Two Factor Authentication in Two Minutes',
      url='https://github.com/azpoliak/twofaas',
      author='Gil Chen-Zion',
      author_email='gil.chenzion@gmail.com',
      license='MIT',
      packages=['pytwofaas'],
      install_requires=[
          'requests',
          'pycrypto'
      ],
      zip_safe=False)