from five import grok
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from plone.i18n.locales.interfaces import ICountryAvailability


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
def available_country_codes(context):
    items = getUtility(ICountryAvailability).getAvailableCountries()
    terms = []
    if items:
        for item in items:
            item = item.upper()
            terms.append(SimpleVocabulary.createTerm(item, str(item), item))
    return SimpleVocabulary(terms)
