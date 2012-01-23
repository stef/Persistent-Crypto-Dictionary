import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "persistent_crypto_dict",
    version = "0.4",
    author = "Stefan Marsiske",
    author_email = "stefan.marsiske@gmail.com",
    summary = ("An encrypted persistent dictionary"),
    license = "AGPLv3+",
    keywords = "crypto collections container persistency cache",
    url = "http://packages.python.org/persistent_crypto_dict",
    packages=['pcd' ],
    long_description=read('README.rst'),
    classifiers=["Classifier: Development Status :: 4 - Beta",
                 "Classifier: License :: OSI Approved :: BSD License",
                 "Classifier: Topic :: Security :: Cryptography",
                 ],
)
