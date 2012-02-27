from gilt import __version__
from setuptools import setup, find_packages

setup(
    name = "gilt",
    version = __version__,
    description = "Gilt API client",
    author = "Gilt Groupe",
    author_email = "python-tech@gilt.com",
    url = "http://github.com/gilt/gilt-python/",
    keywords = ["gilt"],
    install_requires = [
        "httplib2 >= 0.7.2", 
        "iso8601 >= 0.1.4",
        ],
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
    Python Gilt API
    ---------------

    DESCRIPTION
    The Gilt API allows developers access to sale and product information from gilt.com.
    and much more.  See http://www.github.com/twilio/twilio-python for more information.

    LICENSE 
    The Python Gilt API distributed under the Apache Softare License.
    """ )
