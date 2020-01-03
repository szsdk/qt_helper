import setuptools
# from setuptools import setup
# or
# from distutils.core import setup  

setuptools.setup(
        name='qt_helper',
        version='0.1',
        description='This is a test of the setup',
        author='szsdk',
        author_email='shenz34206@hotmail.com',
        packages=setuptools.find_packages(exclude=["test*"]),
        install_requires=[
            'PyQt5>=5.2'
            ]
)
