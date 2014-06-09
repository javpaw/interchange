import os
from setuptools import setup


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='interchange',
    version='0.0.1',
    license='Apache 2.0',
    description='Strategy pattern implementation',
    author='Javier',
    author_email='yourname@example.com',
    packages:['interchange']
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=[
        'nose >= 1.3.1'
    ]

)