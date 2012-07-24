from hexagonit.socialbutton import _
from plone.directives import form
from zope import schema
from zope.interface import Interface


class ISocialSiteRoot(Interface):
    """Site root marker."""


class ISocialCodesView(Interface):
    """SocialCodesView view"""

    def codes(*args, **kwargs):
        """Get social html codes"""


class IData(form.Schema):

    code_id = schema.TextLine(
        title=_(u'ID'))

    code_text = schema.Text(
        title=_(u'Code'))


class ISocialButtonConfig(form.Schema):

    code_id = schema.TextLine(
        title=_(u'ID'))

    content_types = schema.Set(
        title=_(u'Content Types'))

    view_models = schema.TextLine(
        title=_(u'View Models'),
        description=_(u'List names of view model line by line.'))

    enabled = schema.Bool(
        title=_(u'Enabled'))
