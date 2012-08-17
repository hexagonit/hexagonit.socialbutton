from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from five import grok
from hexagonit.socialbutton import _
from hexagonit.socialbutton.utility import IBadTypes
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite


@grok.provider(IContextSourceBinder)
def social_button_code_ids(context):
    registry = getUtility(IRegistry)
    items = registry['hexagonit.socialbutton.codes']
    terms = []
    if items:
        for item in items:
            terms.append(SimpleVocabulary.createTerm(item, str(item), item))
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def social_button_content_types(context):
    site = getSite()
    ttool = getToolByName(site, 'portal_types')
    request = aq_get(ttool, 'REQUEST', None)
    items = [
        (translate(ttool[t].Title(), context=request), t) for t in ttool.listContentTypes(
            ) if t not in getUtility(IBadTypes)()]
    items.append((_(u'All Types'), u'*'))
    items.sort()
    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
