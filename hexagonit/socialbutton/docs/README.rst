======================
hexagonit.socialbutton
======================

This package provides viewlet to embed social button to Plone site.
The viewlet can be assigned to wherever viewlet managers through the web.
Since restrictions for the embedded code are not set,
you need to be cautious about the security risk with the embedding code.

Further Documentation URL
-------------------------

`http://packages.python.org/hexagonit.socialbutton/
<http://packages.python.org/hexagonit.socialbutton/>`_

Repository URL
--------------

`https://github.com/hexagonit/hexagonit.socialbutton/
<https://github.com/hexagonit/hexagonit.socialbutton/>`_

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

Example to set values from file system code::

    registry = getUtility(IRegistry)
    registry['hexagonit.socialbutton.codes'] = {
        u'facebook': {
            u'code_text': u'<FACEBOOK>${title} <img src="${portal_url}/++resource++hexagonit.socialbutton/facebook.gif" /></FACEBOOK>',
        }
    }

Example to register through registry.xml::

    <record name="hexagonit.socialbutton.codes">
      <field type="plone.registry.field.Dict">
        <title>Codes for Social Buttons</title>
        <key_type type="plone.registry.field.TextLine" />
        <value_type type="plone.registry.field.Dict">
          <title>Value list</title>
          <key_type type="plone.registry.field.TextLine" />
          <value_type type="plone.registry.field.Text">
            <title>Values</title>
          </value_type>
        </value_type>
      </field>
      <value>
        <element key="facebook">
          <element key="code_text">&lt;FACEBOOK&gt;${title} &lt;img src="${portal_url}/++resource++hexagonit.socialbutton/facebook.gif" /&gt;&lt;/FACEBOOK&gt;s</element>
        </element>
      </value>
    </record>

Code variables
==============

${title}
    Title of the context.

${description}
    Description of the context.

${url}
    URL for the context

${lang}
    Language in use like en.

${lang_country}
    Locales including country code such as en_US.

${portal_url}
    Plone site root URL.

Once **Social Button Code Setting** is set, you can go to **Social Button Configuration** for the farther configuration.

Social Button Configuration
===========================

ID
    The ID set at **Social Button Code Setting**.

Content Types
    The content types where the viewlet will be applied.

Viewlet Manager
    Add the names of viewlet managers line by line where the viewlet will be applied.

View Models
    Add the names of views where the viewlet will be applied.
    For all the views, use ``*``.

View permission only
    If checked, the viewlet is only available at view which are available to anonymous users,
    like in most cases for published contents.

Enabled
    Uncheck this option, when disabling the code from the viewlet.

Example to set values from file system code::

    registry = getUtility(IRegistry)
    registry['hexagonit.socialbutton.config'] = {
        u'facebook': {
            u'content_types': u'Page,News Item',
            u'viewlet_manager': u'plone.abovecontent\nplone.belowcontent',
            u'view_models': u'*',
            u'view_permission_only': 'True',
            u'enabled': 'True',
        }
    }

Example to register through registry.xml::

    <record name="hexagonit.socialbutton.config">
      <field type="plone.registry.field.Dict">
        <title>Configuration for Social Buttons</title>
        <key_type type="plone.registry.field.TextLine" />
        <value_type type="plone.registry.field.Dict">
          <title>Value list</title>
          <key_type type="plone.registry.field.TextLine" />
          <value_type type="plone.registry.field.Text">
            <title>Values</title>
          </value_type>
        </value_type>
      </field>
      <value>
        <element key="facebook">
          <element key="content_types">Page,News Item</element>
          <element key="viewlet_manager">plone.abovecontent
  plone.belowcontent</element>
          <element key="view_models">*</element>
          <element key="view_permission_only">True</element>
          <element key="enabled">True</element>
        </element>
      </value>
    </record>
