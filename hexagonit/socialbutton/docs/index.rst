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

The locales are constructed with ``hexagonit.socialbutton.adapter.mapping.LanguageCountry`` adapter.

.. code-block:: python

    ILanguageCountry(self.context)(lang)


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
