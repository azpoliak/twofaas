from setuptools import setup

setup(name='pytwofaas',
      version='0.2',
      description='Two Factor Authentication in Two Seconds',
      url='https://github.com/azpoliak/twofaas',
      author='Gil Chen-Zion',
      author_email='gil.chenzion@gmail.com',
      license='MIT',
      packages=['pytwofaas'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)