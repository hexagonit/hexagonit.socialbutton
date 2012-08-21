from five import grok
from hexagonit.socialbutton import _
from hexagonit.socialbutton.config import LANGUAGE_COUNTRY
from plone.stringinterp.adapters import BaseSubstitution
from plone.stringinterp.interfaces import IStringSubstitution
from zope.component import getAdapter
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface


class AllContent(BaseSubstitution, grok.Adapter):
    grok.baseclass()
    grok.context(Interface)
    grok.provides(IStringSubstitution)

    catagory = MessageFactory('plone')(u'All Content')


class Lang(AllContent):
    grok.name('lang')
    description = _(u'Language code for the site.')

    def safe_call(self):
        portal_state = getMultiAdapter(
            (self.context, self.context.REQUEST), name='plone_portal_state')
        return portal_state.language()


class LangCountry(AllContent):
    grok.name('lang_country')
    description = _(u'Locales such as fi_FI.')

    def safe_call(self):
        lang = getAdapter(self.context, IStringSubstitution, name="lang")()
        return '{0}_{1}'.format(lang, LANGUAGE_COUNTRY[lang])


class PortalURL(AllContent):
    grok.name('portal_url')
    description = _(u'Portal URL.')

    def safe_call(self):
        portal_state = getMultiAdapter(
            (self.context, self.context.REQUEST), name='plone_portal_state')
        return portal_state.portal_url()
