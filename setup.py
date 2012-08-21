from setuptools import find_packages
from setuptools import setup

import os


long_description = (
    open(os.path.join("hexagonit", "socialbutton", "docs", "README.rst")).read() + "\n" +
    open(os.path.join("hexagonit", "socialbutton", "docs", "HISTORY.rst")).read() + "\n" +
    open(os.path.join("hexagonit", "socialbutton", "docs", "CONTRIBUTORS.rst")).read())


setup(
    name='hexagonit.socialbutton',
    version='0.6',
    description="Adds social button to viewlets.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Hexagon IT',
    author_email='oss@hexagonit.fi',
    url='http://www.hexagonit.fi',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['hexagonit'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone>=4.1',
        'five.grok',
        'hexagonit.testing',
        'plone.browserlayer',
        'plone.directives.form',
        'plone.stringinterp>=1.0.7',
        'setuptools',
        'zope.i18nmessageid'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
