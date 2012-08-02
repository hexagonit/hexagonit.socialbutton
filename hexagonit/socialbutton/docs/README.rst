======================
hexagonit.socialbutton
======================

This package provides viewlet to embed social button to Plone site.
The viewlet can be assigned to wherever viewlet managers through the web.
Since restrictions for the embedded code are not set,
you need to be cautious about the security risk with the embedding code.

Configuration
-------------

Once the package is installed through **Site Setup** **Add-ons**, there appears **Social Button Code Setting** and **Social Button Configuration** links within the **Add-on Configuration** section.

To start the configuration, go to **Social Button Code Setting** first to set the embedding code.

Social Button Code Setting
==========================

ID
    The ID will be used for farther configuration and styling.

Code
    The code to be embedded to viewlet.

Icon
    The icon expression such as ``++resource++hexagonit.socialbutton/facebook.gif``
    This icon can be used in the code as ``{ICON}`` variable.

Code variables
==============

TITLE
    Title of the context.

DESCRIPTION
    Description of the context.

URL
    Current base URL for the context

LANG
    Language in use like en.

LANG_COUNTRY
    Locales including country code such as en_US.

ICON
    Icon expression from field **Icon**.

PORTAL_URL
    Plone site root URL.

* Since the code will be formated with python's string ``format`` method with those variables above, the variables need to be closed with curly bracket.

* To escape the curly bracket, use double curly bracket like ``{{Some thing}}``.

Example of Code::

    <script type="text/javascript">
        (function () {{if
        ...
        }})();
    </script>
    <a href="facebook_url" link="{URL}" language="{LANG}">
      <img src="{PORTAL_URL}/{ICON}" />
    </a>

Once **Social Button Code Setting** is set, you can go to **Social Button Configuration** for the farther configuration.

Social Button Configuration
===========================

ID
    The ID set at **Social Button Code Setting**.

Content Types
    The content types where the viewlet will be applied.
    If not selected, the viewlet will be applied to all the content types.

Viewlet Manager
    Add the names of viewlet managers line by line where the viewlet will be applied.

View Models
    Add the names of views where the viewlet will be applied.
    If empty, the viewlet will be applied to all the views.

View permisson only
    If checked, the vielwet is only available at view which are available to anonymous users,
    like in most cases for published contents.

Enabled
    Uncheck this option, when disabling the code from the viewlet.


Further Documentation URL
-------------------------

`http://packages.python.org/hexagonit.socialbutton/
<http://packages.python.org/hexagonit.socialbutton/>`_

Repository URL
--------------

`https://github.com/hexagonit/hexagonit.socialbutton/
<https://github.com/hexagonit/hexagonit.socialbutton/>`_
