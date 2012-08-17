from hexagonit.socialbutton import _
from hexagonit.socialbutton.vocabulary import social_button_code_ids
from hexagonit.socialbutton.vocabulary import social_button_content_types
from plone.directives import form
from zope import schema
from zope.interface import Interface


class ISocialSiteRoot(Interface):
    """Site root marker."""


class ISocialCodesView(Interface):
    """SocialCodesView view"""

    def codes(*args, **kwargs):  # pragma: no cover
        """Get social html codes"""


class IAddSocialButtonCode(form.Schema):

    code_id = schema.TextLine(
        title=_(u'ID'))

    code_text = schema.Text(
        title=_(u'Code'))


class ISocialButtonCode(IAddSocialButtonCode):
    """"""

    code_id = schema.TextLine(
        title=_(u'ID'),
        readonly=True)


class IAddSocialButtonConfig(form.Schema):

    code_id = schema.Choice(
        title=_(u'ID'),
        source=social_button_code_ids)

    content_types = schema.Set(
        title=_(u'Content Types'),
        default=set(u'*'),
        value_type=schema.Choice(
            source=social_button_content_types))

    viewlet_manager = schema.Text(
        title=_(u'Viewlet Manager'),
        description=_(u'List names of viewlet manager line by line.'),
        default=u'plone.belowcontent')

    view_models = schema.Text(
        title=_(u'View Models'),
        description=_(u"List names of view model line by line. For all the views, use '*'"),
        default=u'*')

    view_permission_only = schema.Bool(
        title=_(u'View permission only'),
        description=_(u'Display button only for views which has View permission.'),
        default=True)

    enabled = schema.Bool(
        title=_(u'Enabled'),
        default=True)


class ISocialButtonConfig(IAddSocialButtonConfig):

    code_id = schema.TextLine(
        title=_(u'ID'),
        readonly=True)


class ILanguageCountry(Interface):
    """Interface for language country mapping."""

    def __call__(lang, **kwargs):  # pragma: no cover
        """Returns lang_country based on lang."""


class ISocialButtonHidden(Interface):
    """Marker interface to mark content type to hide social buttons viewlet."""
