import os
import subprocess

from setuptools import setup, find_packages

#subprocess.call(['make','-C','simpletrack'])

setup(
        name='simpletrack',
        version='0.0.0',
        description='6D Tracking Library',
        author='Riccardo De Maria',
        author_email='riccardo.de.maria@cern.ch',
        url='https://github.com/rdemaria/simpletrack',
        packages=find_packages(),
        package_dir={'simpletrack': 'simpletrack'},
        install_requires=['numpy','cobjects'],
#        package_data={'simpletrack': ['block.so']},
        include_package_data=True
)
