.. include:: README.rst

Mapping languages and countries
===============================

Country mapping against language resides in hexagonit.socialbutton.config module.

.. code-block:: python

    LANGUAGE_COUNTRY = {
        'en': 'US',
        'fi': 'FI',
        'ja': 'JP',
        'ru': 'RU',
        'sv': 'SE',
    }

The locales are constructed with ``hexagonit.socialbutton.adapter.dollar.LangCountry`` adapter.

.. code-block:: python

    from plone.stringinterp.interfaces import IStringSubstitution
    from zope.component import getAdapter

    getAdapter(self.context, IStringSubstitution, name="lang_country")()


Contents:

.. toctree::
    :maxdepth: 2

    INSTALL.rst
    HISTORY.rst
    CONTRIBUTORS.rst
    LICENSE.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
